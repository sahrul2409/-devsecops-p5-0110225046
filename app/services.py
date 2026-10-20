"""Logika bisnis pencatatan pengeluaran."""
from collections import defaultdict
from typing import Dict, List

from app.models import Expense
from app.storage import JsonStorage
from app.validators import validate_amount, validate_category, validate_date


class ExpenseService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def add(self, tanggal: str, kategori: str, jumlah, keterangan: str = "") -> Expense:
        expense = Expense(
            tanggal=validate_date(tanggal),
            kategori=validate_category(kategori),
            jumlah=validate_amount(jumlah),
            keterangan=keterangan.strip(),
        )
        items = self.storage.load()
        items.append(expense)
        self.storage.save(items)
        return expense

    def list_all(self) -> List[Expense]:
        return sorted(self.storage.load(), key=lambda e: e.tanggal)

    def total(self) -> int:
        return sum(e.jumlah for e in self.storage.load())

    def total_by_category(self) -> Dict[str, int]:
        hasil: Dict[str, int] = defaultdict(int)
        for e in self.storage.load():
            hasil[e.kategori] += e.jumlah
        return dict(hasil)

    def monthly_total(self, tahun: int, bulan: int) -> int:
        return sum(
            e.jumlah
            for e in self.storage.load()
            if e.tanggal.year == tahun and e.tanggal.month == bulan
        )

    def over_budget(self, tahun: int, bulan: int, anggaran: int) -> bool:
        return self.monthly_total(tahun, bulan) > validate_amount(anggaran)
