#Entitas Kendaraan untuk Sistem Parkir + konversi ke/dari baris CSV
class Kendaraan:
    #Merepresentasikan satu kendaraan yang terdaftar di sistem parkir
    def __init__(self, plat, jenis, pemilik,
                 status="Tidak Parkir", slot=0, waktu_masuk=""):
        self.plat = plat.upper()
        self.jenis = jenis          # Motor / Mobil
        self.pemilik = pemilik
        self.status = status        # "Tidak Parkir" / "Terparkir"
        self.slot = int(slot)       # nomor slot (0 = tidak parkir)
        self.waktu_masuk = waktu_masuk

    @staticmethod
    def header():
        return ["plat", "jenis", "pemilik", "status", "slot", "waktu_masuk"]

    def to_row(self):
        return [self.plat, self.jenis, self.pemilik,
                self.status, self.slot, self.waktu_masuk]

    @staticmethod
    def from_row(row):
        return Kendaraan(
            plat=row["plat"],
            jenis=row["jenis"],
            pemilik=row["pemilik"],
            status=row.get("status", "Tidak Parkir"),
            slot=row.get("slot", 0) or 0,
            waktu_masuk=row.get("waktu_masuk", ""),
        )

    def __repr__(self):
        return f"Kendaraan({self.plat} - {self.jenis})"
