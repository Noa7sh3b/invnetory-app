from flask import Flask
import subprocess
import threading

app = Flask(__name__)

# شغل Streamlit في Thread منفصل
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])

threading.Thread(target=run_streamlit).start()

@app.route("/")
def home():
    return "OK", 200  # Health check ينجح فورًا

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
