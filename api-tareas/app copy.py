import os
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv

# ===== Config =====
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tasks.db")

# Para SQLite con paths relativos en SQLAlchemy 2.x
if DATABASE_URL.startswith("sqlite:///"):
    db_url = DATABASE_URL.replace("sqlite:///", "sqlite+pysqlite:///")
elif DATABASE_URL.startswith("sqlite://"):
    db_url = DATABASE_URL.replace("sqlite://", "sqlite+pysqlite://")
else:
    db_url = DATABASE_URL

engine = create_engine(db_url, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False))
Base = declarative_base()

# ===== Modelo =====
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    done = Column(Boolean, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at.isoformat() + "Z",
        }

# Crear tablas si no existen
#Base.metadata.create_all(bind=engine)
# Solo crea las tablas si no existen
Base.metadata.create_all(bind=engine, checkfirst=True)

# ===== App =====
app = Flask(__name__)
CORS(app, resources={r"/tasks*": {"origins": "*"}})  # habilita CORS para frontend

# ===== Helpers =====
def get_json():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    return request.get_json()

# ===== Rutas =====
@app.get("/tasks")
def list_tasks():
    """Lista tareas (opcional: ?q=texto para filtrar)"""
    q = request.args.get("q", "").strip()
    with SessionLocal() as db:
        query = db.query(Task)
        if q:
            query = query.filter(Task.title.ilike(f"%{q}%"))
        tasks = query.order_by(Task.id.desc()).all()
        return jsonify([t.to_dict() for t in tasks])

@app.post("/tasks")
def create_task():
    """Crea una tarea: { "title": "Comprar pan" }"""
    data = get_json()
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, description="Field 'title' is required")

    with SessionLocal() as db:
        task = Task(title=title, done=bool(data.get("done", False)))
        db.add(task)
        db.commit()
        db.refresh(task)
        return jsonify(task.to_dict()), 201

if __name__ == "__main__":
    # FLASK_ENV=development para auto-reload
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
