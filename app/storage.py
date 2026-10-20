"""Penyimpanan data ke file JSON."""
import json
import os
from typing import List

from app.models import Expense


class JsonStorage:
    def __init__(self, path: str = "data/expenses.json"):
        self.path = path

    def load(self) -> List[Expense]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Expense.from_dict(item) for item in raw]

    def save(self, items: List[Expense]) -> None:
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in items], f, indent=2, ensure_ascii=False)
