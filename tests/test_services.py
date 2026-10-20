import pytest
from app.services import ExpenseService
from app.storage import JsonStorage
from app.validators import ValidationError


@pytest.fixture
def svc(tmp_path):
    return ExpenseService(JsonStorage(str(tmp_path / "d.json")))

def test_add_and_total(svc):
    svc.add("2026-10-01", "makan", 20000)
    svc.add("2026-10-02", "transport", 10000)
    assert svc.total() == 30000

def test_total_by_category(svc):
    svc.add("2026-10-01", "makan", 20000)
    svc.add("2026-10-03", "makan", 5000)
    assert svc.total_by_category() == {"makan": 25000}

def test_monthly_total(svc):
    svc.add("2026-09-30", "makan", 1000)
    svc.add("2026-10-01", "makan", 2000)
    assert svc.monthly_total(2026, 10) == 2000

def test_over_budget(svc):
    svc.add("2026-10-01", "hiburan", 500000)
    assert svc.over_budget(2026, 10, 300000)
    assert not svc.over_budget(2026, 10, 600000)

def test_add_invalid(svc):
    with pytest.raises(ValidationError):
        svc.add("2026-10-01", "makan", -1)

def test_list_sorted(svc):
    svc.add("2026-10-05", "makan", 1000)
    svc.add("2026-10-01", "makan", 1000)
    assert svc.list_all()[0].tanggal.day == 1
