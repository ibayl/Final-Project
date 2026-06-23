import csv
import os

from model import Kendaraan
from struktur_data import HashMap

FOLDER_DATA = os.path.join(os.path.dirname(__file__), "data")
FILE_KENDARAAN = os.path.join(FOLDER_DATA, "kendaraan.csv")


def _pastikan_folder():
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)


def muat_kendaraan():
    # Membaca kendaraan.csv ke HashMap (key = plat nomor)
    _pastikan_folder()
    peta = HashMap()
    if not os.path.exists(FILE_KENDARAAN):
        return peta
    with open(FILE_KENDARAAN, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            k = Kendaraan.from_row(row)
            peta.put(k.plat, k)
    return peta


def simpan_kendaraan(peta):
    # Menulis seluruh isi HashMap ke kendaraan.csv
    _pastikan_folder()
    with open(FILE_KENDARAAN, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(Kendaraan.header())
        for k in peta.values():
            writer.writerow(k.to_row())


def seed_data_awal():
    #Membuat data contoh bila kendaraan.csv belum ada
    _pastikan_folder()
    if os.path.exists(FILE_KENDARAAN):
        return
    contoh = [
        Kendaraan("B1234ABC", "Mobil", "Andi"),
        Kendaraan("D5678XYZ", "Motor", "Budi"),
        Kendaraan("F9012JKL", "Mobil", "Citra"),
        Kendaraan("B3456MNO", "Motor", "Dewi"),
    ]
    peta = HashMap()
    for k in contoh:
        peta.put(k.plat, k)
    simpan_kendaraan(peta)
