"""Antarmuka CLI aplikasi UangKu."""
import argparse
import sys
from datetime import date

from app.report import export_csv, format_rupiah, text_report
from app.services import ExpenseService
from app.storage import JsonStorage
from app.validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="uangku", description="Pencatat keuangan mahasiswa")
    p.add_argument("--data", default="data/expenses.json", help="lokasi file data")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="tambah pengeluaran")
    add.add_argument("--tanggal", default=date.today().isoformat())
    add.add_argument("--kategori", required=True)
    add.add_argument("--jumlah", required=True)
    add.add_argument("--ket", default="")

    sub.add_parser("list", help="tampilkan laporan")
    sub.add_parser("total", help="total pengeluaran")

    exp = sub.add_parser("export", help="ekspor ke CSV")
    exp.add_argument("--out", default="pengeluaran.csv")

    bud = sub.add_parser("budget", help="cek anggaran bulanan")
    bud.add_argument("--tahun", type=int, required=True)
    bud.add_argument("--bulan", type=int, required=True)
    bud.add_argument("--anggaran", required=True)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = ExpenseService(JsonStorage(args.data))
    try:
        if args.cmd == "add":
            e = service.add(args.tanggal, args.kategori, args.jumlah, args.ket)
            print(f"Tersimpan: {e.kategori} {format_rupiah(e.jumlah)}")
        elif args.cmd == "list":
            print(text_report(service.list_all(), service.total_by_category()))
        elif args.cmd == "total":
            print(format_rupiah(service.total()))
        elif args.cmd == "export":
            export_csv(service.list_all(), args.out)
            print(f"Diekspor ke {args.out}")
        elif args.cmd == "budget":
            lewat = service.over_budget(args.tahun, args.bulan, args.anggaran)
            print("MELEBIHI anggaran!" if lewat else "Masih dalam anggaran.")
    except ValidationError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
