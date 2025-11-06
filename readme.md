# Plataforma para Gestión de Proyectos - SAP

## Circuit Breaker & Retry Pattern en Service B (Proyectos)

Se implementaron los patrones Circuit Breaker y Retry Pattern en el microservicio Service B (Proyectos), encargado de coordinar la comunicación con los microservicios Service A (Empresas) y Service C (Programación y Seguimiento de Proyecto).

## Objetivo

Evitar que el sistema falle en cadena cuando:

* Un servicio dependiente (A o C) está lento, 
* o está temporalmente fuera de servicio.

Esto se logra mediante:

* Reintentos inteligentes para respuestas temporales. 
* Apertura del circuito cuando las fallas son constantes, protegiendo Service B y el sistema completo.

## Flujo de Resiliencia: Retry + Circuit Breaker

(Aplicado al microservicio de Proyectos — Service Proyectos (B))

### Contexto del dominio

En el sistema Administración de Proyectos - SAP:

* Service Empresas (A) administra información institucional de la empresa ejecutora. 
* Service Proyectos (B) gestiona datos de los proyectos de inversión.
* Service Programación/Seguimiento (C) contiene el seguimiento físico y financiero del proyecto.

El servicio B necesita consultar a A y C para devolver información completa cuando el usuario consulta un proyecto.

### Flujo Detallado
#### 1. El usuario solicita información de un proyecto

Ejemplo de endpoint:
```bash
GET /proyectos/detalle/15/ 
```

El Service B recibe la solicitud y procede a:

| Acción                                  | Servicio consultado |
| --------------------------------------- | ------------------- |
| Obtener datos de la empresa relacionada | Service A           |
| Obtener avance físico/financiero        | Service C           |

#### 2. Service B realiza la llamada externa
```bash
empresa = call_service("http://service_empresas/empresas/10/")
programacion = call_service("http://service_programacion/programacion/15/")
```
Estas llamadas pasan por call_service() que tiene incorporado Retry + Circuit Breaker.

#### 3. Si la llamada falló una vez, se considera temporal

Ejemplos de fallas temporales:
* La base del Service A se está reiniciando 
* Latencia momentánea en el contenedor 
* Sobrecarga de red en el cluster

En este caso, se activa el Retry Pattern, que:
 * Vuelve a intentar la llamada 
 * Espera antes de intentar nuevamente 
 * Incrementa el tiempo de espera en cada intento (ej. 1s → 2s → 4s, con variación para evitar saturación).

Se permiten hasta 3 reintentos.
```bash
Intento 1 → falla → esperar 1s  
Intento 2 → falla → esperar 2-3s  
Intento 3 → falla → esperar 4-6s  
```
> Si alguno de los intentos responde con éxito → flujo continúa normalmente.

#### 4. ¿Qué pasa si después de los 3 reintentos sigue fallando?
Service B considera que el servicio dependiente no está disponible.
Entonces entra el Circuit Breaker:

| Estado del Circuito          | Significado                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| **Closed (Normal)**          | Las llamadas se hacen sin restricciones                              |
| **Open (Protección Activa)** | Service B **bloquea** llamadas a A y C temporalmente                 |
| **Half-Open (Prueba)**       | Después de un tiempo, reintenta para verificar si el servicio volvió |

#### Activación del Circuit Breaker

El circuito pasa a Open cuando:
* El número de fallas acumuladas supera 4 intentos consecutivos.

Esto:
* Evita que Service B siga intentando y colapse 
* Evita spam o DoS accidental sobre Service A o C 
* Mantiene el servicio funcionando sin dependencia externa

#### 5. ¿Qué devuelve Service B cuando el circuito está abierto?
Devuelve una respuesta degradada, por ejemplo:
```bash
{
  "proyecto": {
    "id": 15,
    "nombre": "Construcción Nuevo Centro de Salud"
  },
  "empresa": "No disponible temporalmente",
  "programacion": "No disponible temporalmente",
  "mensaje": "Parte de la información no puede mostrarse en este momento."
}
```

## Librerias utilizadas

| Patrón          | Librería    | Descripción                                              |
| --------------- | ----------- | -------------------------------------------------------- |
| Retry Pattern   | `tenacity`  | Controla reintentos con espera progresiva.               |
| Circuit Breaker | `pybreaker` | Evita llamar servicios que están fallando repetidamente. |
| Cliente HTTP    | `httpx`     | Manejo de solicitudes HTTP con soporte para timeouts.    |

puede instalarse por separa o también ya esta dentro del archivo de requirements.txt
```bash
pip install pybreaker tenacity httpx
pip install -r requirements.txt
```
## Estructura del proyecto
```bash
sap/
├─ docker-compose.yml
├─ nginx/
│   └─ nginx.conf
├─ service_auth/
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ service_auth/
│   │   ├─ settings.py
│   │   ├─ urls.py
│   │   └─ wsgi.py
│   └─ auth_app/
│       └─ views.py
├─ service_empresas/          # Service A
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ manage.py
│   ├─ service_empresas(service_a_api)/
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
│   ├─ service_proyectos(service_b_api)/
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
│   ├─ service_programacion(service_c_api)/
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
3. Registrar usuario y obtener token

```bash
# registrar
POST http://localhost:8000/auth/register/
{ "username": "edwin", "password": "pass123" }
ó
curl -X POST -H "Content-Type: application/json" -d '{"username": "edwin", "password": "pass123", "email": "edwin@example.com"}' http://localhost:8000/auth/register/ 

# obtener token
POST http://localhost:8000/auth/token/
{ "username": "edwin", "password": "pass123" }
ó
curl -X POST -H "Content-Type: application/json" -d '{"username": "edwin", "password": "pass123"}' http://localhost:8000/auth/token/ 
```
