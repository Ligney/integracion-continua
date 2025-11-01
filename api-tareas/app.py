import os
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

# ===== App =====
app = Flask(__name__)
#CORS(app, resources={r"/tasks*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



# ===== Datos temporales =====
tareas = []

# ===== Helpers =====
def get_json():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    return request.get_json()

# ===== Rutas =====
@app.get("/tasks")
def list_tasks():
    """Lista tareas (desde la memoria, sin BD)"""
    q = request.args.get("q", "").strip().lower()
    if q:
        filtradas = [t for t in tareas if q in t["title"].lower()]
        return jsonify(filtradas)
    return jsonify(tareas)

@app.post("/tasks")
def create_task():
    """Crea una tarea (sin BD)"""
    data = get_json()
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, description="Field 'title' is required")

    nueva = {
        "id": len(tareas) + 1,
        "title": title,
        "done": bool(data.get("done", False)),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    tareas.append(nueva)
    return jsonify(nueva), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
