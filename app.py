from flask import Flask, render_template, request
from src.parser import read_log_file
from src.detector import detect_failed_logins
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "logfile" not in request.files:
        return "No file uploaded"

    file = request.files["logfile"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    log_lines = read_log_file(filepath)

    suspicious_ips = detect_failed_logins(log_lines)

    result = ""

    if suspicious_ips:

        result += "<h2>Suspicious Activity Detected</h2>"

        for ip, count in suspicious_ips:
            result += f"<p>{ip} → Failed Attempts: {count}</p>"

    else:
        result = "<h2>No suspicious activity detected.</h2>"

    return result