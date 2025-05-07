

from google.generativeai import types
from google import genai
_client: genai.Client


# ─── Module-level client placeholder ─────────────────────
_client: genai.Client

def setKey(api_key: str):
    if not api_key or api_key.startswith("YOUR_"):
        raise RuntimeError("Please call dep_laiser.setKey(<your_real_key>)")
    # create the NEW HTTP/JSON client
    global _client
    _client = genai.Client(api_key=api_key)



_config = types.GenerationConfig(
    temperature=0.0,
    top_k=1,
    top_p=1.0,
    candidate_count=1
)




_prompt_template = """<start_of_turn>user
**Objective:** Given a {input_desc}, complete the following tasks with structured outputs.

### Tasks:
1. **Skills Extraction:** Identify {num_key_skills} key skills mentioned in the {input_desc}.
  -The skill (≤ 3 words) must appear in the text *or* be an obvious synonym of a word/phrase that appears.
  -The skill must be a noun phrase describing a **competence**, **method**, **tool**, or **domain knowledge**.  
    -Reject values/traits such as “social responsibility”, “team spirit”, “motivation” *unless the text names them explicitly.*
  -For each skill also return a short “Evidence” field - 3-7 words copied *verbatim* from the input that justify the choice.
2. **Skill Level Assignment:** Assign a proficiency level to each extracted skill based on the SCQF Level Descriptors (see below).

3. **Knowledge Required:** For each skill, list {num_key_kr} broad areas of understanding or expertise necessary to develop the skill.

4. **Task Abilities:** For each skill, list {num_key_tas} general tasks or capabilities enabled by the skill.

5. **Skill Description:** For each skill, write 1-2 sentences **using a standard template** (start with an action verb like “Applies,” “Demonstrates,” or “Uses”) that define the skill **in general terms**—avoid course-specific examples or jargon.

### Guidelines:
- **Skill Extraction:** Identify skills explicitly stated or implied through {input_desc}.
- **Skill Level Assignment:** Use the SCQF Level Descriptors to classify proficiency:
  - 1: Basic awareness of simple concepts.
  - 2: Limited operational understanding, guided application.
  - 3: Moderate knowledge, supervised application of techniques.
  - 4: Clear understanding, independent work in familiar contexts.
  - 5: Advanced knowledge, autonomous problem-solving.
  - 6: Specialized knowledge, critical analysis within defined areas.
  - 7: Advanced specialization, leadership in problem-solving.
  - 8: Expert knowledge, innovation in complex contexts.
  - 9: Highly specialized expertise, contributing original thought.
  - 10: Sustained mastery, influential in areas of specialization.
  - 11: Groundbreaking innovation, professional or academic mastery.
  - 12: Global expertise, leading advancements at the highest level.

- **Knowledge and Task Abilities:**
  - **Knowledge Required:** Broad areas, e.g., "data visualization techniques."
  - **Task Abilities:** General tasks or capabilities, e.g., "data analysis."
  - Each item in these two lists should be no more than three words.
  - Avoid overly specific or vague terms.

- ** Skill Description
  - **Standard phrasing:** Begin descriptions with a clear verb (“Applies statistical methods…”, “Demonstrates critical thinking…”).
  - **General definition:** Describe the skill itself, not a specific use case (e.g. “Applies statistical methods to summarize data,” not “Applies statistical methods to analyze film trends”).
  - **Brevity & clarity:** Keep each description under 20 words, focus on the core capability.

### Answer Format:
Return **only** a JSON array of objects, each with these keys:
- **Skill** (string)
- **Level** (integer)
- **Knowledge Required** (array of strings)
- **Task Abilities** (array of strings)
- **Skill Description** (string)

**Example**:
```json
[
  {{
    "Skill":"Film analysis",
    "Level":4,
    "Knowledge Required":["film theory","genre study","visual rhetoric"],
    "Task Abilities":["interpret films","critique themes","compare genres"],
    "Skill Description":"Applies critical frameworks to analyze cinematic techniques and themes.",
    "Evidence":"analysis of cinema"
  }},
  {{
    "Skill":"Communication",
    "Level":3,
    "Knowledge Required":["oral skills","written skills","visual media"],
    "Task Abilities":["write reports","present ideas","collaborate"],
    "Skill Description":"Demonstrates clear written and spoken communication across contexts.",
    "Evidence":"effective writing and speaking"
  }}
]

{input_text}

**Response:** Provide only the requested structured information without additional explanations.

<end_of_turn>
<start_of_turn>model
"""
# build the prompt
def create_prompt(query: dict, input_type: str,
                  num_key_skills: int, num_key_kr: str, num_key_tas: str) -> str:
    input_desc = "job description" if input_type == "syllabi" else "course syllabus description and its learning outcomes"
    if input_type == "syllabi":
        input_text = (
            f"### Input:\n"
            f"**Course Description:** {query['description']}\n"
            f"**Learning Outcomes:** {query['learning_outcomes']}"
        )
    else:
        input_text = f"### Input:\n{query['description']}"

    return _prompt_template.format(
        input_desc=input_desc,
        num_key_skills=num_key_skills,
        num_key_kr=num_key_kr,
        num_key_tas=num_key_tas,
        input_text=input_text
    )
prompts = []
async def generate_structured_skills(
    query: dict,
    input_type: str = "syllabi",
    num_key_skills: int = 5,
    num_key_kr: str = "3-5",
    num_key_tas: str = "3-5"
) -> str:
    """
    Given one row dict, build prompt + call Gemini deterministically,
    return the raw JSON text.
    """

    
    prompt = create_prompt(
        query, input_type, num_key_skills, num_key_kr, num_key_tas
    )
    if _client is None:
        raise RuntimeError(
            "Gemini key not set—please call dep_laiser.setKey(<your_key>) first."
        )
    response = await _client.aio.models.generate_content(
    model="gemini-1.5-pro",
    contents=prompt      
    )
    return response.text.strip()
