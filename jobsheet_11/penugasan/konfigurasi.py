# konfigurasi.py
import os

# Lokasi dasar proyek (folder tempat file ini berada)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nama dan path file database
NAMA_DB = 'pengeluaran_harian.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Daftar kategori pengeluaran yang tersedia
KATEGORI_PENGELUARAN = [
    "Makanan",
    "Transportasi",
    "Hiburan",
    "Tagihan",
    "Belanja",
    "Kesehatan",
    "Pendidikan",
    "Lainnya"
]

# Kategori default jika tidak ditentukan
KATEGORI_DEFAULT = "Lainnya"
