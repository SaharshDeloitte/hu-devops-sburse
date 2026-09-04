from flask import Flask

app = Flask(__name__)


@app.get("/")
def health():
    return {"status": "ok", "message": "HU Jenkins CI/CD sample app is running."}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
