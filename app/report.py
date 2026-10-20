"""Pembuatan laporan teks dan ekspor CSV."""
import csv
from typing import Dict, List

from app.models import Expense


def format_rupiah(nilai: int) -> str:
    return "Rp" + f"{nilai:,}".replace(",", ".")


def text_report(items: List[Expense], per_kategori: Dict[str, int]) -> str:
    baris = ["LAPORAN PENGELUARAN", "=" * 40]
    for e in items:
        baris.append(
            f"{e.tanggal} | {e.kategori:<10} | {format_rupiah(e.jumlah):>12} | {e.keterangan}"
        )
    baris.append("-" * 40)
    for kategori, total in sorted(per_kategori.items()):
        baris.append(f"{kategori:<12}: {format_rupiah(total)}")
    baris.append(f"{'TOTAL':<12}: {format_rupiah(sum(per_kategori.values()))}")
    return "\n".join(baris)


def export_csv(items: List[Expense], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tanggal", "kategori", "jumlah", "keterangan"])
        for e in items:
            writer.writerow([e.tanggal.isoformat(), e.kategori, e.jumlah, e.keterangan])
