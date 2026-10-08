import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import desc
from analyzer import analyze_code
from database import Analysis, SessionLocal, init_db

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
init_db()

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    try:
        result = analyze_code(payload.get("code", ""))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    db = SessionLocal()
    try:
        db.add(Analysis(score=result["score"], complexity=result["complexity"], issues=json.dumps(result["issues"])))
        db.commit()
    finally:
        db.close()
    return jsonify(result)

@app.get("/api/history")
def history():
    db = SessionLocal()
    try:
        rows = db.query(Analysis).order_by(desc(Analysis.created_at)).limit(10).all()
        return jsonify([{"id": r.id, "score": r.score, "complexity": r.complexity, "created_at": r.created_at.isoformat()} for r in rows])
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
