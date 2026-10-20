"""Model data untuk pengeluaran."""
from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Expense:
    """Satu catatan pengeluaran."""
    tanggal: date
    kategori: str
    jumlah: int
    keterangan: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        data["tanggal"] = self.tanggal.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            tanggal=date.fromisoformat(data["tanggal"]),
            kategori=data["kategori"],
            jumlah=int(data["jumlah"]),
            keterangan=data.get("keterangan", ""),
        )
