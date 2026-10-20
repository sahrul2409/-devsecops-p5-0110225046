# UangKu – Pencatat Keuangan Mahasiswa

[![DevSecOps Pipeline](../../actions/workflows/devsecops.yml/badge.svg)](../../actions/workflows/devsecops.yml)

## 1. Nama Aplikasi & Fungsi
**UangKu** adalah aplikasi command-line untuk mencatat pengeluaran harian mahasiswa.
Fitur: tambah pengeluaran, laporan per kategori, total bulanan, cek anggaran bulanan,
dan ekspor ke CSV. Input divalidasi (jumlah, kategori, format tanggal).

## 2. Bahasa / Framework
- Python 3.11 (library standar saja untuk aplikasi)
- pytest + pytest-cov (unit test & coverage)
- Bandit (SAST)

Struktur kode: `app/models.py`, `app/validators.py`, `app/storage.py`,
`app/services.py`, `app/report.py`, `main.py`.

## 3. Cara Menjalankan
```bash
git clone https://github.com/<username>/devsecops-p5-<nim>.git
cd devsecops-p5-<nim>
pip install -r requirements.txt

python main.py add --kategori makan --jumlah 15000 --ket "nasi ayam"
python main.py list
python main.py total
python main.py budget --tahun 2026 --bulan 10 --anggaran 1000000
python main.py export --out pengeluaran.csv

pytest --cov=app          # menjalankan unit test
```

## 4. Overview Pipeline CI/CD
File: `.github/workflows/devsecops.yml` — terpicu pada **push** dan **pull_request** ke `main`,
berjalan di `ubuntu-latest`.

| Job | Fungsi |
|-----|--------|
| `build` | Install dependencies, jalankan unit test, wajib coverage ≥ 80% |
| `sast-scan` (`needs: build`) | Jalankan **Bandit**, simpan laporan JSON sebagai artifact, lalu **Quality Gate** |

**Quality Gate** (`scripts/quality_gate.py`): pipeline GAGAL jika Bandit menemukan
severity HIGH > 0 atau MEDIUM > 0 (ambang dapat diubah lewat env `MAX_HIGH`, `MAX_MEDIUM`).
