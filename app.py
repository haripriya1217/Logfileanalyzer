from flask import Flask, render_template, request, send_file
import os

from analyzer import analyze_log
from report import generate_pdf
from csv_report import generate_csv

app = Flask(__name__)

UPLOAD_FOLDER = "logs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Store latest analysis
latest_result = None
latest_filename = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global latest_result, latest_filename

    file = request.files["logfile"]

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    result = analyze_log(filepath)

    latest_result = result
    latest_filename = file.filename

    generate_pdf(result, file.filename)

    return render_template(
        "index.html",
        result=result,
        filename=file.filename
    )


@app.route("/download")
def download():
    return send_file(
        "reports/report.pdf",
        as_attachment=True
    )


@app.route("/download_csv")
def download_csv():
    global latest_result, latest_filename

    csv_file = generate_csv(latest_result, latest_filename)

    return send_file(
        csv_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)