from flask import Flask, render_template, request
import os

from src.parser import read_log_file
from src.detector import analyze_logs
from src.cloud_upload import upload_to_s3
from src.alerter import send_alert

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
S3_BUCKET = "cloudshield-log-storage-hf"

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

    # Save locally
    file.save(filepath)

    # Upload to AWS S3
    upload_to_s3(filepath, S3_BUCKET, file.filename)

    # Analyze log file
    log_lines = read_log_file(filepath)
    alerts = analyze_logs(log_lines)

    # Send email alert for HIGH risk events
    for alert in alerts:
        if alert["risk"] == "HIGH":
            message = f"""
CloudShield detected a HIGH risk event.

IP: {alert['ip']}
Threat: {alert['type']}
Occurrences: {alert['count']}
"""
            send_alert(message)
            break

    return render_template("result.html", alerts=alerts)


if __name__ == "__main__":
    app.run(debug=True)