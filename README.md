# integracion-continua


 Proyecto de Integración Continua: Frontend + Backend + base de datos con Docker
Este proyecto demuestra la integración entre una API Flask (backend) y una interfaz web (frontend con HTML, CSS y JavaScript), ejecutadas en contenedores separados mediante Docker Compose.

Estructura del proyecto
integracion-continua/
├── api-tareas/     # Backend con Flask
├── ui-tareas/      # Frontend con HTML, CSS y JS
└── docker-compose.yml

ejecución

Clona el repositorio.

Desde la carpeta raíz, ejecuta:
docker-compose up --build


Abre en tu navegador:

Frontend: http://localhost:8080

Backend (API): http://localhost:5000/tasks


Estado actual

El frontend y backend se comunican correctamente entre contenedores.

Se manejaron y resolvieron errores de CORS, conexión entre servicios y conflictos de nombres.


