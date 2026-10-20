import pytest
from app.validators import (ValidationError, validate_amount,
                            validate_category, validate_date)


def test_amount_valid():
    assert validate_amount("15000") == 15000

@pytest.mark.parametrize("bad", ["abc", 0, -5, None, 10**9])
def test_amount_invalid(bad):
    with pytest.raises(ValidationError):
        validate_amount(bad)

def test_category_normalized():
    assert validate_category("  Makan ") == "makan"

def test_category_invalid():
    with pytest.raises(ValidationError):
        validate_category("judi")

def test_date_valid():
    assert validate_date("2026-10-16").day == 16

def test_date_invalid():
    with pytest.raises(ValidationError):
        validate_date("16-10-2026")
