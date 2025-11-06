# Plataforma para Gestión de Proyectos - SAP
## Estructura del proyecto
```bash
sap/
├─ docker-compose.yml
├─ nginx/
│   └─ nginx.conf
├─ auth-service/
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ auth_api/
│   │   ├─ settings.py
│   │   ├─ urls.py
│   │   └─ wsgi.py
│   └─ auth_app/
│       └─ views.py
├─ service_empresas/          # Service A
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ service_a_api/
│   │   ├─ settings.py
│   │   ├─ urls.py
│   │   └─ wsgi.py
│   └─ app_a/
│       ├─ models.py
│       └─ views.py
├─ service_proyectos/         # Service B
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ service_b_api/
│   │   ├─ settings.py
│   │   ├─ urls.py
│   │   └─ wsgi.py
│   └─ app_b/
│       ├─ models.py
│       ├─ views.py
│       └─ clients.py
├─ service_programacion/      # Service C
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ service_c_api/
│   │   ├─ settings.py
│   │   ├─ urls.py
│   │   └─ wsgi.py
│   └─ app_c/
│       ├─ models.py
│       └─ views.py
```

## Levantar el proyecto
1. Desde la raíz del proyecto
```bash
docker-compose up --build
```
2. Ejecutar las migraciones por servicio
```bash
docker-compose exec service_auth python manage.py migrate
docker-compose exec service_empresas python manage.py migrate
docker-compose exec service_proyectos python manage.py migrate
docker-compose exec service_programacion python manage.py migrate
```
3. Probando la authenticacion con JWT: `http://localhost:8000/auth/token/`
```bash
{"username": "edwin"}
```
