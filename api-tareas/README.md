# 🧩 Trabajo Colaborativo Integracion Continua API (Flask + SQLite + Docker)

Backend básico para gestionar tareas (To-Do List) con **Python + Flask + SQLAlchemy**, usando **SQLite** como base de datos y empaquetado en **Docker**.

---

## 🚀 Características

- API REST construida con **Flask**
- Persistencia con **SQLite**
- Servidor de producción con **Gunicorn**
- Imagen Docker ligera basada en `python:3.12-slim`

---

## 📁 Estructura del proyecto

```
tareas-api/
│
├── app.py                # Código principal de la API Flask
├── requirements.txt      # Dependencias del proyecto
├── Dockerfile            # Imagen Docker para producción
```

---

## ⚙️ Endpoints principales

| Método | Endpoint          | Descripción                          |
|---------|-------------------|--------------------------------------|
| `GET`   | `/tasks`          | Lista todas las tareas               |
| `POST`  | `/tasks`          | Crea una nueva tarea                 |

### 🧾 Ejemplo de creación (`POST /tasks`)
```json
{
  "title": "Comprar pan"
}
```

---

## 🧰 Requisitos

- [Docker](https://www.docker.com/) instalado (v20+)
- Opcionalmente [Python 3.12+](https://www.python.org/) si deseas ejecutarlo sin Docker

---

## 🐋 Ejecución con Docker

### 1️⃣ Construir la imagen
```bash
docker build -t tareas-api-sqlite .
```

### 2️⃣ Ejecutar el contenedor
```bash
docker run --name tareas-api -p 5000:5000 tareas-api-sqlite
```

La API estará disponible en  
👉 http://localhost:5000

---

## 💾 Persistir la base de datos SQLite

Por defecto, la base de datos se guarda dentro del contenedor (`/app/data/tasks.db`).  
Para mantener los datos incluso si el contenedor se elimina, monta un volumen local:

```bash
mkdir -p ./data
docker run --name tareas-api   -p 5000:5000   -v $(pwd)/data:/app/data   tareas-api-sqlite
```

---

## 🧩 Variables de entorno

| Variable        | Descripción                                  | Valor por defecto                  |
|-----------------|----------------------------------------------|------------------------------------|
| `PORT`          | Puerto donde se ejecuta la API               | `5000`                             |
| `DATABASE_URL`  | Cadena de conexión SQLAlchemy                | `sqlite:////app/data/tasks.db`     |
| `FLASK_ENV`     | Entorno (`development` o `production`)       | `production`                       |

Ejemplo de `.env`:

```bash
DATABASE_URL=sqlite:////app/data/tasks.db
PORT=5000
FLASK_ENV=production
```

---

## 💻 Ejecución local (sin Docker)

1. Crea un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   ```

2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la app:
   ```bash
   python app.py
   ```

4. API disponible en [http://localhost:5000](http://localhost:5000)

---


## 🧾 Licencia

Proyecto educativo del Politecnico Grancolombiano para para integración Flask + Docker + SQLite
