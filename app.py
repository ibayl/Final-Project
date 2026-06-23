from flask import Flask, render_template
from database import muat_kendaraan

app = Flask(
    __name__,
    template_folder="frontend"
)

@app.route("/")
def dashboard():
    peta = muat_kendaraan()
    kendaraan = peta.values()

    return render_template(
        "dashboard.html",
        total_kendaraan=len(kendaraan),
        sedang_parkir = len([
            k for k in kendaraan
            if k.status == "Terparkir"
        ])
    )


if __name__ == "__main__":
    app.run(debug=True)