from flask import Flask, render_template, jsonify # type: ignore
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/open_gui", methods=["POST"])
def open_gui():
    # Open the Tkinter GUI from file1.py
    try:
        subprocess.Popen(["python", "file1.py"])
        return jsonify({"status": "success", "message": "Circuit GUI opened"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
