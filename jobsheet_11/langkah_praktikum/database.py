# database.py

import sqlite3
import pandas as pd
from konfigurasi import DB_PATH  # Menggunakan path dari konfigurasi


def get_db_connection() -> sqlite3.Connection | None:
    """Membuka dan mengembalikan koneksi baru ke database SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row  # Memungkinkan akses kolom dengan nama
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Koneksi DB gagal: {e}")
        return None


def execute_query(query: str, params: tuple = None):
    """
    Menjalankan query non-SELECT (INSERT, UPDATE, DELETE).
    Jika query adalah INSERT, mengembalikan lastrowid.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query gagal: {e} | Query: {query[:60]}")
        conn.rollback()
        return None
    finally:
        conn.close()


def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    """
    Menjalankan query SELECT dan mengembalikan hasil.
    fetch_all=True untuk mengambil semua hasil, False untuk satu baris saja.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e} | Query: {query[:60]}")
        return None
    finally:
        conn.close()


def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    """
    Menjalankan query SELECT dan mengembalikan hasil sebagai DataFrame Pandas.
    """
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()

    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"ERROR [database.py] Gagal baca ke DataFrame: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def setup_database_initial() -> bool:
    """
    Membuat tabel 'transaksi' jika belum ada. 
    Dipanggil saat inisialisasi aplikasi pertama kali.
    """
    print(f"Memeriksa/membuat tabel di database (via database.py): {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            jumlah REAL NOT NULL CHECK(jumlah > 0),
            kategori TEXT,
            tanggal DATE NOT NULL
        );
        """
        cursor.execute(sql_create_table)
        conn.commit()
        print(" -> Tabel 'transaksi' siap.")
        return True
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Setup tabel gagal: {e}")
        return False
    finally:
        conn.close()
