// =========================
// CONFIGURACIÓN DE LA API
// =========================
// Cuando pruebas desde tu PC, usa localhost:5000
// (El navegador NO puede ver el contenedor tareas-api directamente)
const API_URL = "http://localhost:5000/tasks";

// =========================
// REFERENCIAS DEL DOM
// =========================
const taskInput = document.getElementById("taskInput");
const addBtn = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");

// =========================
// CARGAR TAREAS AL INICIO
// =========================
window.addEventListener("DOMContentLoaded", loadTasks);

// =========================
// FUNCIONES
// =========================

// Obtener todas las tareas
async function loadTasks() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);
    const tasks = await res.json();

    taskList.innerHTML = "";
    tasks.forEach(task => {
      const li = document.createElement("li");
      li.textContent = task.title;
      if (task.done) li.classList.add("done");
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error("⚠️ Error cargando tareas:", error);
  }
}

// Agregar nueva tarea
addBtn.addEventListener("click", async () => {
  const title = taskInput.value.trim();
  if (!title) return alert("Por favor escribe una tarea 😅");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);

    taskInput.value = "";
    loadTasks();
  } catch (error) {
    console.error("⚠️ Error agregando tarea:", error);
  }
});
