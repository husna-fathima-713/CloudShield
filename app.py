from flask import Flask, render_template, request
import os

from src.parser import read_log_file
from src.detector import analyze_logs

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

    alerts = analyze_logs(log_lines)

    result = "<h1>CloudShield Analysis Report</h1>"

    if alerts:

        result += """
        <table border='1' cellpadding='10'>
            <tr>
                <th>IP Address</th>
                <th>Threat Type</th>
                <th>Risk Level</th>
                <th>Occurrences</th>
            </tr>
        """

        for alert in alerts:

            result += f"""
            <tr>
                <td>{alert['ip']}</td>
                <td>{alert['type']}</td>
                <td>{alert['risk']}</td>
                <td>{alert['count']}</td>
            </tr>
            """

        result += "</table>"

    else:
        result += "<h2>No suspicious activity detected.</h2>"

    return result


if __name__ == "__main__":
    app.run(debug=True)