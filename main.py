from datetime import datetime
import math

import database as db
from model import Kendaraan
from struktur_data import (
    Stack, Queue, merge_sort, binary_search, linear_search,
)

KAPASITAS_SLOT = 10          # kapasitas garasi (slot parkir)
TARIF = {"Motor": 2000, "Mobil": 5000}   # tarif per jam


class SistemParkir:
    def __init__(self):
        db.seed_data_awal()
        self.kendaraan = db.muat_kendaraan()   # HashMap {plat: Kendaraan}
        self.slot_parkir = Stack()             # tumpukan plat yang sedang parkir
        self.antrian = Queue()                 # antrian saat penuh
        self._rekonstruksi_slot()

    # Util
    def _rekonstruksi_slot(self):
        """Mengisi ulang Stack slot dari data yang berstatus 'Terparkir'."""
        terparkir = [k for k in self.kendaraan.values() if k.status == "Terparkir"]
        terparkir = merge_sort(terparkir, key_func=lambda k: k.slot, menaik=True)
        for k in terparkir:
            self.slot_parkir.push(k.plat)

    def _simpan(self):
        db.simpan_kendaraan(self.kendaraan)

    @staticmethod
    def _cetak_tabel(daftar):
        if not daftar:
            print("   (tidak ada data)")
            return
        print("   +------------+--------+----------------+--------------+------+---------------------+")
        print("   | Plat       | Jenis  | Pemilik        | Status       | Slot | Waktu Masuk         |")
        print("   +------------+--------+----------------+--------------+------+---------------------+")
        for k in daftar:
            slot = k.slot if k.slot else "-"
            waktu = k.waktu_masuk if k.waktu_masuk else "-"
            print("   | {:<10} | {:<6} | {:<14} | {:<11} | {:<4} | {:<19} |".format(
                k.plat, k.jenis, k.pemilik[:14], k.status, str(slot), waktu))
        print("   +------------+--------+----------------+--------------+------+---------------------+")

    # 1. Create / Tambah Kendaraan
    def tambah_kendaraan(self):
        print("\n-- Tambah Kendaraan --")
        plat = input("   Plat nomor : ").strip().upper()
        if not plat:
            print("   ! Plat tidak boleh kosong."); return
        if self.kendaraan.contains(plat):
            print("   ! Plat sudah terdaftar."); return
        jenis = input("   Jenis (Motor/Mobil) : ").strip().capitalize()
        if jenis not in ("Motor", "Mobil"):
            print("   ! Jenis harus Motor atau Mobil."); return
        pemilik = input("   Nama pemilik : ").strip()
        if not pemilik:
            print("   ! Nama tidak boleh kosong."); return
        self.kendaraan.put(plat, Kendaraan(plat, jenis, pemilik))
        self._simpan()
        print(f"   + Kendaraan {plat} berhasil ditambahkan.")

    # 2. READ
    def lihat_kendaraan(self):
        print("\n-- Daftar Kendaraan --")
        daftar = merge_sort(self.kendaraan.values(), key_func=lambda k: k.plat)
        self._cetak_tabel(daftar)
        print(f"   Total: {len(self.kendaraan)} kendaraan | "
              f"Terisi: {len(self.slot_parkir)}/{KAPASITAS_SLOT} slot")

    # 3. UPDATE
    def update_kendaraan(self):
        print("\n-- Update Kendaraan --")
        plat = input("   Plat nomor : ").strip().upper()
        k = self.kendaraan.get(plat)
        if k is None:
            print("   ! Kendaraan tidak ditemukan."); return
        print("   (Kosongkan input untuk mempertahankan nilai lama)")
        jenis = input(f"   Jenis [{k.jenis}] : ").strip().capitalize()
        pemilik = input(f"   Pemilik [{k.pemilik}] : ").strip()
        if jenis in ("Motor", "Mobil"):
            k.jenis = jenis
        elif jenis:
            print("   ! Jenis diabaikan (harus Motor/Mobil).")
        if pemilik:
            k.pemilik = pemilik
        self._simpan()
        print("   * Data kendaraan diperbarui.")

    # 4. DELETE
    def hapus_kendaraan(self):
        print("\n-- Hapus Kendaraan --")
        plat = input("   Plat nomor : ").strip().upper()
        k = self.kendaraan.get(plat)
        if k is None:
            print("   ! Kendaraan tidak ditemukan."); return
        if k.status == "Terparkir":
            print("   ! Kendaraan sedang parkir. Keluarkan dulu sebelum dihapus."); return
        konf = input(f"   Yakin hapus {plat}? (y/n): ").strip().lower()
        if konf != "y":
            print("   Dibatalkan."); return
        self.kendaraan.remove(plat)
        self._simpan()
        print("   - Kendaraan dihapus.")

    # 5. KENDARAAN MASUK (Stack / Queue)
    def kendaraan_masuk(self):
        print("\n-- Kendaraan Masuk --")
        plat = input("   Plat nomor : ").strip().upper()
        k = self.kendaraan.get(plat)
        if k is None:
            print("   ! Kendaraan belum terdaftar. Tambahkan dulu (menu 1)."); return
        if k.status == "Terparkir":
            print("   ! Kendaraan sudah ada di dalam."); return
        if len(self.slot_parkir) >= KAPASITAS_SLOT:
            self.antrian.enqueue(plat)
            print(f"   ~ Parkir PENUH. {plat} masuk antrian ke-{len(self.antrian)}.")
            return
        self._parkirkan(k)

    def _parkirkan(self, k):
        self.slot_parkir.push(k.plat)
        k.status = "Terparkir"
        k.slot = len(self.slot_parkir)
        k.waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._simpan()
        print(f"   > {k.plat} parkir di slot {k.slot}. (terisi {len(self.slot_parkir)}/{KAPASITAS_SLOT})")

    # 6. KENDARAAN KELUAR (Stack)
    def kendaraan_keluar(self):
        print("\n-- Kendaraan Keluar --")
        plat = input("   Plat nomor : ").strip().upper()
        k = self.kendaraan.get(plat)
        if k is None:
            print("   ! Kendaraan tidak ditemukan."); return
        if k.status != "Terparkir":
            print("   ! Kendaraan tidak sedang parkir."); return

        # Garasi 1 jalur (LIFO): keluarkan mobil di atasnya dulu ke buffer
        buffer = Stack()
        dipindahkan = 0
        while not self.slot_parkir.is_empty() and self.slot_parkir.peek() != plat:
            buffer.push(self.slot_parkir.pop())
            dipindahkan += 1
        self.slot_parkir.pop()                  # keluarkan kendaraan target
        while not buffer.is_empty():             # kembalikan kendaraan lain
            self.slot_parkir.push(buffer.pop())
        if dipindahkan:
            print(f"   (i) {dipindahkan} kendaraan di atasnya dipindahkan sementara lalu dikembalikan.)")

        biaya = self._hitung_biaya(k)
        k.status = "Tidak Parkir"
        k.slot = 0
        k.waktu_masuk = ""
        self._simpan()
        print(f"   > {plat} keluar. Biaya parkir: Rp{biaya:,}".replace(",", "."))

        # bila ada antrian, masukkan kendaraan berikutnya
        if not self.antrian.is_empty() and len(self.slot_parkir) < KAPASITAS_SLOT:
            plat_berikut = self.antrian.dequeue()
            knext = self.kendaraan.get(plat_berikut)
            if knext:
                print(f"   ~ Antrian maju: {plat_berikut} dipersilakan masuk.")
                self._parkirkan(knext)

    def _hitung_biaya(self, k):
        try:
            masuk = datetime.strptime(k.waktu_masuk, "%Y-%m-%d %H:%M:%S")
            durasi_jam = (datetime.now() - masuk).total_seconds() / 3600
        except (ValueError, TypeError):
            durasi_jam = 0
        jam = max(1, math.ceil(durasi_jam))
        return jam * TARIF.get(k.jenis, 2000)

    # 7. Search
    def cari_kendaraan(self):
        print("\n-- Cari Kendaraan --")
        print("   1. Berdasarkan plat (Binary Search)")
        print("   2. Berdasarkan kata kunci (Linear Search)")
        pilih = input("   Pilih: ").strip()
        if pilih == "1":
            plat = input("   Plat nomor: ").strip().upper()
            terurut = merge_sort(self.kendaraan.values(), key_func=lambda k: k.plat)
            idx = binary_search(terurut, plat, key_func=lambda k: k.plat)
            if idx == -1:
                print("   ! Tidak ditemukan.")
            else:
                self._cetak_tabel([terurut[idx]])
        elif pilih == "2":
            kunci = input("   Kata kunci (plat/pemilik/jenis): ").strip()
            self._cetak_tabel(linear_search(self.kendaraan.values(), kunci))
        else:
            print("   ! Pilihan tidak valid.")

    # 8. Sort
    def urutkan_data(self):
        print("\n-- Urutkan Data (Merge Sort) --")
        print("   1. Plat (A-Z)")
        print("   2. Jenis (A-Z)")
        print("   3. Pemilik (A-Z)")
        pilih = input("   Pilih: ").strip()
        data = self.kendaraan.values()
        if pilih == "1":
            hasil = merge_sort(data, key_func=lambda k: k.plat)
        elif pilih == "2":
            hasil = merge_sort(data, key_func=lambda k: k.jenis.lower())
        elif pilih == "3":
            hasil = merge_sort(data, key_func=lambda k: k.pemilik.lower())
        else:
            print("   ! Pilihan tidak valid."); return
        self._cetak_tabel(hasil)

    # MENU
    def menu(self):
        aksi = {
            "1": self.tambah_kendaraan,
            "2": self.lihat_kendaraan,
            "3": self.update_kendaraan,
            "4": self.hapus_kendaraan,
            "5": self.kendaraan_masuk,
            "6": self.kendaraan_keluar,
            "7": self.cari_kendaraan,
            "8": self.urutkan_data,
        }
        while True:
            print("\n===== SISTEM PARKIR =====\n")
            print("   1. Tambah Kendaraan")
            print("   2. Lihat Kendaraan")
            print("   3. Update Kendaraan")
            print("   4. Hapus Kendaraan")
            print("   5. Kendaraan Masuk")
            print("   6. Kendaraan Keluar")
            print("   7. Cari Kendaraan")
            print("   8. Urutkan Data")
            print("   9. Keluar")
            pilih = input("   Pilih menu: ").strip()
            if pilih == "9":
                print("\n   Terima kasih. Sampai jumpa!")
                break
            fn = aksi.get(pilih)
            if fn is None:
                print("   ! Menu tidak valid.")
                continue
            fn()


if __name__ == "__main__":
    SistemParkir().menu()
