# 🅿️ Sistem Parkir (CLI + CSV)

Final Project mata kuliah Struktur Data. Aplikasi manajemen parkir berbasis
**command-line (CLI)** dengan **file .CSV** sebagai basis datanya (flat file).

## 📋 Menu

```
===== SISTEM PARKIR =====

1. Tambah Kendaraan
2. Lihat Kendaraan
3. Update Kendaraan
4. Hapus Kendaraan
5. Kendaraan Masuk
6. Kendaraan Keluar
7. Cari Kendaraan
8. Urutkan Data
9. Keluar
```

## 🧩 Struktur Data & Algoritma

| Struktur Data / Algoritma | Penerapan |
|---------------------------|-----------|
| **Hash Map** (separate chaining) | Akses data kendaraan berdasarkan plat nomor, O(1) rata-rata |
| **Stack** (LIFO) | Tumpukan slot parkir (garasi 1 jalur). Saat keluar, kendaraan di atasnya dipindahkan sementara |
| **Queue** (FIFO) | Antrian kendaraan ketika parkir penuh |
| **Merge Sort** (O(n log n)) | Mengurutkan data (plat/jenis/pemilik) |
| **Binary Search** (O(log n)) | Mencari kendaraan berdasarkan plat pada data terurut |
| **Linear Search** (O(n)) | Mencari kendaraan berdasarkan kata kunci |

## ⚙️ Fitur Tambahan

- Kapasitas slot terbatas (default 5) + **antrian otomatis** saat penuh.
- Perhitungan **biaya parkir** berdasarkan durasi & jenis kendaraan (Motor Rp2.000/jam, Mobil Rp5.000/jam, minimal 1 jam).
- Status & slot kendaraan tersimpan persisten di CSV.

## 📁 Struktur Folder

```
parkir/
├── main.py            # Menu utama & alur aplikasi (CLI)
├── struktur_data.py   # HashMap, Stack, Queue, Merge Sort, Searching
├── model.py           # Entitas Kendaraan + konversi CSV
├── database.py        # Baca/tulis file CSV (flat file database)
├── flowchart.png      # Gambar flowchart aplikasi
├── README.md
└── data/
    └── kendaraan.csv  # Database kendaraan (dibuat otomatis)
```

## ▶️ Cara Menjalankan

```bash
cd parkir
python3 main.py
```

Saat pertama dijalankan, aplikasi membuat data contoh otomatis di `data/kendaraan.csv`.

## 🗃️ Format Data (kendaraan.csv)

```csv
plat,jenis,pemilik,status,slot,waktu_masuk
B1234ABC,Mobil,Andi,Di Luar,0,
D5678XYZ,Motor,Budi,Terparkir,2,2026-06-17 13:56:15
```
