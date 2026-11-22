import sqlite3

# Nama file database SQLite (otomatis dibuat saat kode dijalankan)
DB_NAME = "subscriptions.db"


def get_db_connection():
    """Membuka koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_NAME)
    # Mengubah hasil query agar bisa diakses seperti dictionary (misal: row['name'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Membuat tabel 'subscriptions' jika belum ada."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            billing_cycle TEXT NOT NULL,
            next_billing_date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_subscription(name, price, category, billing_cycle, next_billing_date):
    """CREATE: Menambahkan data langganan baru ke database."""
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO subscriptions (name, price, category, billing_cycle, next_billing_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, price, category, billing_cycle, next_billing_date),
    )
    conn.commit()
    conn.close()


def get_all_subscriptions():
    """READ: Mengambil semua data langganan dalam bentuk list of dictionary."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM subscriptions ORDER BY next_billing_date ASC"
    ).fetchall()
    conn.close()
    # Ubah setiap baris menjadi dictionary Python biasa agar mudah dipakai di app.py & reminder.py
    return [dict(row) for row in rows]


def get_subscription_by_id(sub_id):
    """READ (Single): Mengambil 1 data langganan berdasarkan ID (untuk fitur Edit)."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE id = ?", (sub_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_subscription(
    sub_id, name, price, category, billing_cycle, next_billing_date
):
    """UPDATE: Memperbarui data langganan yang sudah ada berdasarkan ID."""
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE subscriptions
        SET name = ?, price = ?, category = ?, billing_cycle = ?, next_billing_date = ?
        WHERE id = ?
        """,
        (name, price, category, billing_cycle, next_billing_date, sub_id),
    )
    conn.commit()
    conn.close()


def delete_subscription(sub_id):
    """DELETE: Menghapus data langganan berdasarkan ID."""
    conn = get_db_connection()
    conn.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()


# Blok ini hanya jalan kalau kamu mengetes file database.py secara langsung
if __name__ == "__main__":
    init_db()
    print("Database dan tabel 'subscriptions' berhasil dibuat!")