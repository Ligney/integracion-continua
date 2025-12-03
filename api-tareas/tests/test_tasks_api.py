import pytest
import sys
import os

# === Importación corregida para api-tareas ===
# Agregamos la ruta de la carpeta api-tareas, que es donde está app.py
CURRENT_DIR = os.path.dirname(__file__)
API_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(API_DIR)

from app import app, tareas


@pytest.fixture(autouse=True)
def limpiar_tareas():
    """Antes de cada prueba se limpia la lista de tareas."""
    tareas.clear()


@pytest.fixture
def client():
    return app.test_client()


# ======================
# PRUEBAS GET /tasks
# ======================

def test_list_tasks_empty(client):
    """Debe devolver lista vacía si no hay tareas."""
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.get_json() == []


def test_list_tasks_with_items(client):
    """Debe listar tareas creadas."""
    tareas.append({"id": 1, "title": "Estudiar", "done": False})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_list_tasks_filter(client):
    """Debe filtrar tareas por query en ?q="""
    tareas.append({"id": 1, "title": "Comprar pan", "done": False})
    tareas.append({"id": 2, "title": "Ir al banco", "done": False})

    res = client.get("/tasks?q=pan")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Comprar pan"


# ======================
# PRUEBAS POST /tasks
# ======================

def test_create_task_success(client):
    """Debe crear correctamente una tarea."""
    nuevo = {"title": "Estudiar Flask", "done": False}

    res = client.post("/tasks", json=nuevo)
    assert res.status_code == 201

    data = res.get_json()
    assert data["id"] == 1
    assert data["title"] == "Estudiar Flask"
    assert data["done"] is False
    assert "created_at" in data


def test_create_task_missing_title(client):
    """Debe fallar si falta el campo title."""
    res = client.post("/tasks", json={"done": True})
    assert res.status_code == 400
    assert "required" in res.get_data(as_text=True)


def test_create_task_empty_title(client):
    """Debe fallar si title está vacío."""
    res = client.post("/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_create_task_invalid_json(client):
    """Debe fallar si el JSON no es válido (sin application/json)."""
    res = client.post("/tasks", data="texto sin json", headers={"Content-Type": "text/plain"})
    assert res.status_code == 400
