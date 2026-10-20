from main import main


def test_cli_add_and_total(tmp_path, capsys):
    d = str(tmp_path / "c.json")
    assert main(["--data", d, "add", "--kategori", "makan", "--jumlah", "12000"]) == 0
    assert main(["--data", d, "total"]) == 0
    assert "Rp12.000" in capsys.readouterr().out

def test_cli_invalid(tmp_path):
    d = str(tmp_path / "c.json")
    assert main(["--data", d, "add", "--kategori", "xx", "--jumlah", "1"]) == 1
