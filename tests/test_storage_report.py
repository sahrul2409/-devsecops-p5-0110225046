from datetime import date
from app.models import Expense
from app.report import export_csv, format_rupiah, text_report
from app.storage import JsonStorage


def test_storage_roundtrip(tmp_path):
    st = JsonStorage(str(tmp_path / "x" / "e.json"))
    st.save([Expense(date(2026, 10, 1), "makan", 9000, "nasi")])
    assert st.load()[0].keterangan == "nasi"

def test_storage_empty(tmp_path):
    assert JsonStorage(str(tmp_path / "none.json")).load() == []

def test_format_rupiah():
    assert format_rupiah(1500000) == "Rp1.500.000"

def test_text_report():
    items = [Expense(date(2026, 10, 1), "makan", 9000, "nasi")]
    out = text_report(items, {"makan": 9000})
    assert "TOTAL" in out and "Rp9.000" in out

def test_export_csv(tmp_path):
    f = tmp_path / "o.csv"
    export_csv([Expense(date(2026, 10, 1), "makan", 9000)], str(f))
    assert "tanggal,kategori" in f.read_text()
