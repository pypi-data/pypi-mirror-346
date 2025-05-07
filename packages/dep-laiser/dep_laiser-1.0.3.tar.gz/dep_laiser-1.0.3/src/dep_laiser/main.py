import re
import json
import ast
import asyncio
try:
    import nest_asyncio          # pip install nest_asyncio  (tiny, pure-py)
    nest_asyncio.apply()         # allow nested loops if one exists
except ImportError:
    nest_asyncio = None   
import pandas as pd
from dep_laiser.run_gemini import generate_structured_skills
from dep_laiser.matching import run_esco_mapping,run_esco_mapping_st_encoder_hybrid
import time
pd.set_option('display.max_colwidth', None)
import json

def load_syllabi_data() -> pd.DataFrame:
    """
    Load your syllabi data. Modify this function to read from CSV, database, etc.
    """
    syllabi_data = pd.read_csv("https://raw.githubusercontent.com/LAiSER-Software/datasets/refs/heads/master/syllabi-data/preprocessed_50_opensyllabus_syllabi_data.csv")
    return syllabi_data


def generate_results(df: pd.DataFrame) -> list[str]:
    """
    Fires all Gemini requests concurrently and returns the same
    list[str] as before.  No other code needs to change.
    """
    # throttle so we never exceed your rate-limit
    MAX_CONCURRENT = 50
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def _worker(row_dict):
        async with sem:
            return await generate_structured_skills(
                query=row_dict,
                input_type="syllabi",
                num_key_skills=5,
                num_key_kr="3-5",
                num_key_tas="3-5"
            )

    async def _runner():
        tasks = [_worker(r) for r in df.to_dict("records")]
        return await asyncio.gather(*tasks)

    return asyncio.run(_runner())        # ← same return type as before

def parse_results(raws: list[str], df: pd.DataFrame) -> pd.DataFrame:
    """
    Parses LLM outputs and attaches metadata.
    """
    records = []
    for i, raw in enumerate(raws):
        text = raw.strip()
        start = text.find('[')
        end = text.rfind(']') + 1
        snippet = re.sub(r',\s*([\]\}])', r'\1', text[start:end])
        try:
            parsed = json.loads(snippet)
        except json.JSONDecodeError:
            parsed = ast.literal_eval(snippet)

        meta = df.iloc[i]
        for entry in parsed:
            entry.update({
                "Research ID": meta["id"],
                "Title": meta["title"],
                "Description": meta["description"],
                "Learning Outcomes": meta["learning_outcomes"]
            })
            records.append(entry)

    # Desired column order
    columns = [
        "Research ID",
        "Title",
        "Description",
        "Learning Outcomes",
        "Skill",
        "Level",
        "Knowledge Required",
        "Task Abilities",
        "Skill Description"
    ]
    return pd.DataFrame(records, columns=columns)

def load_extracted(path="extracted_anket_df.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # turn those string‐lists back into real lists
    for col in ["Knowledge Required", "Task Abilities"]:
        df[col] = df[col].apply(ast.literal_eval)
    return df
def extract_skills(
    df: pd.DataFrame,
    title: str = "title",
    description: str = "description",
    learning_outcomes: str = "learning_outcomes",
    matcher: str = "st",  # new: either "st" or "hybrid"
) -> pd.DataFrame:
    """
    df: user's DataFrame
    title: name of the column with the course title
    description: name of the column with the course description
    learning_outcomes: name of the column with learning outcomes
    matcher: "st" to use run_esco_mapping, "hybrid" to use run_esco_mapping_st_encoder_hybrid
    """
    print("Let's Begin")


    start = time.time()
    # 1) Rename user’s columns to what generate_results & parse_results expect
    mapping = {
        title: "title",
        description: "description",
        learning_outcomes: "learning_outcomes"
    }
    df_renamed = df.rename(columns=mapping)
    
    temp_start = time.time()
    # 2) Generate LLM raw outputs
    raw_jsons = generate_results(df_renamed)

    llm_elapsed = time.time() - temp_start

    print(f"→ LLM Call took {llm_elapsed:.2f}s")

    # 3) Parse into a DataFrame
    extracted_df = parse_results(raw_jsons, df_renamed)

    # 4) Choose and run the mapping pipeline
    temp_start = time.time()
    if matcher == "st":
        best_df = run_esco_mapping(extracted_df)
    elif matcher == "hybrid":
        best_df = run_esco_mapping_st_encoder_hybrid(extracted_df)
    else:
        raise ValueError(f"Unknown matcher '{matcher}'; choose 'st' or 'hybrid'")
    
    matching = time.time() - temp_start
    total_api_time = time.time() - start
 
    print(f"→ Matching Call took {matching:.2f}s")
    print(f"→ Total Call took {total_api_time:.2f}s")


    return best_df

if __name__ == "__main__":
     extract_skills()
