from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend to talk to backend

# Store ingested docs in memory
knowledge_base = []


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "JSON must be a list of objects"}), 400
    knowledge_base.extend(data)
    return jsonify({"message": "Documents ingested", "count": len(knowledge_base)})


@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query", "").lower()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Simple keyword search
    results = [doc for doc in knowledge_base if query.split()[0]
               in doc["text"].lower()]
    if not results:
        return jsonify({"answer": "Sorry, I couldn’t find an answer."})
    return jsonify({"answer": results[0]["text"]})


@app.route("/export", methods=["GET"])
def export():
    return jsonify(knowledge_base)


if __name__ == "__main__":
    app.run(debug=True)
