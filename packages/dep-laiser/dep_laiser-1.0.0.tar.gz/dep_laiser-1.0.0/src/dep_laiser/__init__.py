# Re-export a single public entry‐point if you like
from .main import extract_skills
from .run_gemini import setKey

__all__ = ["extract_skills","setKey"]