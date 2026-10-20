"""Validasi input pengguna."""
from datetime import date, datetime

KATEGORI_VALID = ("makan", "transport", "kuliah", "hiburan", "lainnya")


class ValidationError(ValueError):
    """Dilempar ketika input tidak valid."""


def validate_amount(jumlah) -> int:
    try:
        nilai = int(jumlah)
    except (TypeError, ValueError):
        raise ValidationError("Jumlah harus berupa angka bulat")
    if nilai <= 0:
        raise ValidationError("Jumlah harus lebih dari 0")
    if nilai > 100_000_000:
        raise ValidationError("Jumlah melebihi batas wajar")
    return nilai


def validate_category(kategori: str) -> str:
    kategori = (kategori or "").strip().lower()
    if kategori not in KATEGORI_VALID:
        raise ValidationError(
            "Kategori tidak dikenal. Pilih: " + ", ".join(KATEGORI_VALID)
        )
    return kategori


def validate_date(teks: str) -> date:
    try:
        return datetime.strptime(teks, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValidationError("Format tanggal harus YYYY-MM-DD")
