import pickle
import pandas as pd
import numpy as np
import ast
from sentence_transformers import SentenceTransformer,CrossEncoder, util
from pathlib import Path
ESCO_EMBEDS_PATH = Path(__file__).parent / "public" / "esco_embeds.pkl"


def raw_text(row):
    return f"{row['Skill']}. {row['Skill Description']}"     # concise & focused


def map_to_esco(
    extracted_df: pd.DataFrame,
    esco_df: pd.DataFrame,
    sims
) -> pd.DataFrame:
    
    records = []
    for i, row in extracted_df.iterrows():
        best_idx = sims[i].argmax()
        best_sim = sims[i][best_idx]
        records.append({
            "Research ID":            row["Research ID"],
            "Title"               : row['Title'],
            "Description":            row["Description"],
            "Raw Skill":              row["Skill"],
            "Raw Skill Description":  row["Skill Description"],
            "Level":                  row["Level"],
            "Best ESCO Skill":        esco_df.loc[best_idx, "preferredLabel"],
            "ESCO Skill Description": esco_df.loc[best_idx, "description"],
            "Skill Tag":              f"ESCO.{best_idx}",
            "Correlation":            round(float(best_sim), 4),
            "Knowledge Required":     row["Knowledge Required"],
            "Task Abilities":         row["Task Abilities"],
        })
    return pd.DataFrame(records)

# this file is src/my_package/matching.py


def run_esco_mapping(extracted_df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Load all resources, optionally limit to first `top_n` rows,
    then map to ESCO and return the result DataFrame.
    """
    # 1) Optionally trim
    df = extracted_df if top_n is None else extracted_df.head(top_n)

    # 2) Load ESCO lookup table & embeddings
    esco_df = pd.read_csv("https://raw.githubusercontent.com/LAiSER-Software/datasets/refs/heads/master/taxonomies/ESCO_skills_Taxonomy.csv")             # your ESCO labels+desc
    with ESCO_EMBEDS_PATH.open("rb") as f:
        esco_embeddings = pickle.load(f)

    # 3) Init encoder
    st_model = SentenceTransformer("all-mpnet-base-v2")
    raw_texts = extracted_df.apply(raw_text, axis=1).tolist()
    raw_texts = extracted_df.apply(raw_text, axis=1).tolist()
    raw_embeddings  = st_model.encode(
        raw_texts,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    sims = util.cos_sim(raw_embeddings, esco_embeddings).cpu().numpy()
    # 4) Perform mapping
    best_df = map_to_esco(df, esco_df,sims)

    # 5) Save & return
    best_df.to_csv("best_esco_matches.csv", index=False)
    return best_df



def map_to_esco_st_encoder_hybrid(
    extracted_df: pd.DataFrame,
    esco_df: pd.DataFrame,
    raw_texts,
    ce,
    sims
) -> pd.DataFrame:
    
    best_matches = []
    top_k        = 3
    gap_thresh   = 0.02          # ← change this to tighten/loosen the trigger

    for i, row in extracted_df.iterrows():
        sims_row = sims[i]

        # --- 1️⃣  bi-encoder recall -----------------------------------------
        candidate_idxs   = np.argsort(sims_row)[-top_k:][::-1]
        candidate_scores = sims_row[candidate_idxs]          # numpy array
        candidate_labels = esco_df.loc[candidate_idxs, 'preferredLabel'].tolist()

        # quick diagnostic gap
        gap = candidate_scores[0] - candidate_scores[1] if len(candidate_scores) > 1 else 1.0

        # ========== 2️⃣  decide whether to rerank ============================
        if gap < gap_thresh:
            # ---- build left & right texts for cross-encoder ----
            left_text = f"{row['Skill']}. {row['Skill Description']} Context: {row['Title'][:60]}."
            right_texts = [
                f"{esco_df.loc[j,'preferredLabel']}. "
                + " ".join(esco_df.loc[j,'description'].split()[:50])
                for j in candidate_idxs
            ]
            pairs          = [[left_text, rt] for rt in right_texts]
            rerank_scores  = ce.predict(pairs)
            rerank_best    = rerank_scores.argmax()
            best_idx       = candidate_idxs[rerank_best]
            rerank_score   = float(rerank_scores[rerank_best])
        else:
            # ---- trust cosine top hit ----
            best_idx      = candidate_idxs[0]
            rerank_score  = None               # skipped

        best_sim = float(sims_row[best_idx])

        # --- 3️⃣  build record ------------------------------------------------
        rec = {
            "Research ID"         : row['Research ID'],
            "Title"               : row['Title'],
            "Description"         : row['Description'],
            "Raw Skill"           : row['Skill'],
            "Raw Skill Description": row['Skill Description'],
            "Level"               : row['Level'],
            "Best ESCO Skill"    : esco_df.loc[best_idx,'preferredLabel'],
            "ESCO Skill Desc"    : esco_df.loc[best_idx,'description'],
            "Skill Tag":         f"ESCO.{best_idx}",
            "Cosine Score"       : round(best_sim,4),
            "Rerank Score"       : None if rerank_score is None else round(rerank_score,4),
            "Knowledge Required"  : row['Knowledge Required'],
            "Task Abilities"      : row['Task Abilities'],
        }
        # keep the top-3 cosine diagnostics
        for rank,(lbl,sc) in enumerate(zip(candidate_labels, candidate_scores), start=1):
            rec[f"Match{rank}"] = lbl
            rec[f"Score{rank}"] = round(float(sc),4)

        best_matches.append(rec)
    return pd.DataFrame(best_matches)


def run_esco_mapping_st_encoder_hybrid(extracted_df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Load all resources, optionally limit to first `top_n` rows,
    then map to ESCO and return the result DataFrame.
    """
    # 1) Optionally trim
    df = extracted_df if top_n is None else extracted_df.head(top_n)

    # 2) Load ESCO lookup table & embeddings
    esco_df = pd.read_csv("https://raw.githubusercontent.com/LAiSER-Software/datasets/refs/heads/master/taxonomies/ESCO_skills_Taxonomy.csv")             # your ESCO labels+desc
    with ESCO_EMBEDS_PATH.open("rb") as f:
        esco_embeddings = pickle.load(f)

    # 3) Init encoder
    st_model = SentenceTransformer("all-mpnet-base-v2")
    ce = CrossEncoder('cross-encoder/stsb-roberta-base')
    raw_texts = extracted_df.apply(raw_text, axis=1).tolist()
    raw_embeddings  = st_model.encode(
    raw_texts,
    batch_size=32,
    normalize_embeddings=True,
    show_progress_bar=True
    )
    sims = util.cos_sim(raw_embeddings, esco_embeddings).cpu().numpy()

    # 4) Perform mapping
    best_df = map_to_esco_st_encoder_hybrid(df, esco_df,raw_texts, ce,sims)

    # 5) Save & return
    best_df.to_csv("best_esco_matches_hybrid.csv", index=False)
    return best_df