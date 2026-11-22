from flask import Flask, render_template, request, redirect, url_for, jsonify
import database as db

# Coba impor modul reminder.py dari Anggota 3.
# Jika belum ada (belum di-merge), pakai fungsi sementara agar backend tetap jalan.
try:
    import reminder
except ImportError:
    reminder = None

app = Flask(__name__)

# Pastikan tabel database sudah siap saat server dinyalakan
db.init_db()


@app.route("/")
def index():
    """Halaman utama: menampilkan semua daftar langganan & ringkasan biaya."""
    subscriptions = db.get_all_subscriptions()

    # Jika modul reminder.py sudah tersedia, proses data untuk status H-3 & total biaya
    if reminder:
        subscriptions = reminder.process_subscriptions(subscriptions)
        total_monthly = reminder.calculate_monthly_total(subscriptions)
    else:
        total_monthly = sum(sub["price"] for sub in subscriptions)

    return render_template(
        "index.html",
        subscriptions=subscriptions,
        total_monthly=total_monthly,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    """Halaman & proses tambah langganan baru."""
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        category = request.form["category"]
        billing_cycle = request.form["billing_cycle"]
        next_billing_date = request.form["next_billing_date"]

        db.add_subscription(name, price, category, billing_cycle, next_billing_date)
        return redirect(url_for("index"))

    # Jika GET, tampilkan halaman form kosong
    return render_template("form.html", subscription=None)


@app.route("/edit/<int:sub_id>", methods=["GET", "POST"])
def edit(sub_id):
    """Halaman & proses edit langganan berdasarkan ID."""
    subscription = db.get_subscription_by_id(sub_id)
    if not subscription:
        return "Langganan tidak ditemukan", 404

    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        category = request.form["category"]
        billing_cycle = request.form["billing_cycle"]
        next_billing_date = request.form["next_billing_date"]

        db.update_subscription(
            sub_id, name, price, category, billing_cycle, next_billing_date
        )
        return redirect(url_for("index"))

    # Jika GET, tampilkan form yang sudah terisi data lama
    return render_template("form.html", subscription=subscription)


@app.route("/delete/<int:sub_id>", methods=["POST"])
def delete(sub_id):
    """Proses hapus langganan berdasarkan ID."""
    db.delete_subscription(sub_id)
    return redirect(url_for("index"))


@app.route("/api/subscriptions", methods=["GET"])
def api_get_subscriptions():
    """Endpoint JSON untuk tes mandiri backend & kebutuhan JavaScript (Anggota 3)."""
    subscriptions = db.get_all_subscriptions()
    return jsonify(subscriptions)


if __name__ == "__main__":
    # debug=True agar server otomatis restart setiap kali kode diubah
    app.run(debug=True)