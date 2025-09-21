from flask_cors import CORS
from flask import Flask, request, jsonify
print(">>> Script is running")


app = Flask(__name__)
CORS(app)


@app.route("/ingest", methods=["POST"])
def ingest():
    print("Got documents:", request.json)
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question", "")
    return jsonify({"answer": f"You asked: '{q}'. This is a demo answer."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
