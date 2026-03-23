"""
Savollar to'plami (UZ) — LABITI ISH BOT
Kategoriya: Stilist, Kolorit, Vizajist, Manikyur/Pedikyur, Kiprikchi, Depilatsiya, Administrator

Har bir savol quyidagi formatda:
{
    "text": "Savol matni",
    "type": "text" | "choice" | "video",
    "options": ["A", "B", "C"]  # faqat type == "choice" bo'lsa
}
"""
from typing import Dict, List, Any

Question = Dict[str, Any]

CATEGORIES = [
    "Stilist",
    "Kolorit",
    "Vizajist",
    "Manikyur/Pedikyur",
    "Kiprikchi",
    "Depilatsiya",
    "Administrator"
]
import json
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS: Dict[str, List[Question]] = json.load(f)

