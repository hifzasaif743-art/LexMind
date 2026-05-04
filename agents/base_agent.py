import os
from typing import Optional

from langchain_groq import ChatGroq


class BaseAgent:
    def __init__(self, name: str = "Base", model: Optional[str] = None, temperature: float = 0.2):
        self.name = name
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.temperature = temperature

    def _call_llm(self, prompt: str) -> str:
        api_key = (os.getenv("GROQ_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("Missing GROQ_API_KEY in environment (.env).")

        llm = ChatGroq(
            api_key=api_key,
            model=self.model,
            temperature=self.temperature,
        )
        result = llm.invoke(prompt)
        return getattr(result, "content", str(result))