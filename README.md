# FridgeRadar — Backend

API REST para control de alacena y desperdicio cero.

## Stack

- **Python 3.12** + **FastAPI**
- **SQLAlchemy 2.0** (asíncrono) + **aiomysql**
- **MySQL 8**
- **APScheduler** (tareas programadas)
- **JWT** + **bcrypt** (autenticación)
- **Pydantic v2** (validación)
- **pytest** + **pytest-cov** (tests)
- **ruff** + **mypy** (linting)

## Estructura

```
fridgeradar/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/       # 12 endpoints, uno por recurso
│   │   │   └── router.py        # Registro de rutas
│   │   ├── core/                # config, database, security, logging, exceptions
│   │   ├── middlewares/         # LoggingMiddleware
│   │   ├── models/              # 19 modelos SQLAlchemy ORM
│   │   ├── schemas/             # 12 schemas Pydantic (request/response)
│   │   ├── services/            # 13 servicios con lógica de negocio
│   │   ├── repositories/        # 7 repositorios (acceso a BD)
│   │   ├── tasks/               # semáforo, alertas, desperdicio (APScheduler)
│   │   ├── utils/               # semáforo, fechas, paginación, códigos de barras
│   │   └── main.py              # FastAPI app factory
│   ├── tests/
│   │   ├── unit/                # 4 archivos de tests unitarios
│   │   ├── integration/         # 3 archivos de tests de integración
│   │   └── conftest.py          # Fixtures async para tests
│   ├── .env.example
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── requirements-dev.txt
├── infra/
│   ├── mysql/
│   │   └── fridgeradar_db.sql   # Schema + triggers + events + views + procs + seeds
│   └── scripts/
│       └── start_dev.sh         # Script para iniciar el servidor
└── README.md
```

## Requisitos

- **Python 3.12+**
- **MySQL 8+**
- Acceso a una terminal (bash, PowerShell, cmd)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd fridgeradar
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
cd backend
pip install -r requirements-dev.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de MySQL:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DB_HOST` | Host de MySQL | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_NAME` | Nombre de la BD | `fridgeradar_db` |
| `DB_USER` | Usuario de MySQL | `root` |
| `DB_PASSWORD` | Contraseña de MySQL | `admin` |
| `SECRET_KEY` | Clave secreta para JWT | — |
| `ALLOWED_ORIGINS` | Orígenes CORS | `["http://localhost:5173"]` |

### 5. Crear la base de datos

Conecta a MySQL y ejecuta el script SQL completo:

```bash
mysql -u root -p < infra/mysql/fridgeradar_db.sql
```

Esto crea:
- 19 tablas con relaciones
- Índices de rendimiento
- Triggers para semáforo y movimientos
- Eventos programados (semáforo diario, alertas de vencimiento)
- Vistas útiles
- Stored procedures
- Datos semilla (categorías, tags de recetas)

## Ejecutar

### Servidor de desarrollo

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O usando el script:

```bash
bash infra/scripts/start_dev.sh
```

### Documentación interactiva

- **Swagger UI:** `http://localhost:8000/docs`
- **Redoc:** `http://localhost:8000/redoc`

### Health check

```bash
curl http://localhost:8000/health
# {"status":"ok","app":"FridgeRadar"}
```

## Tests

```bash
cd backend
pytest --cov=app tests/
```

### Tests unitarios

```bash
pytest tests/unit/ -v
```

### Tests de integración

```bash
pytest tests/integration/ -v
```

## Linting y tipo

```bash
# Linter
ruff check app/

# Type checker
mypy app/
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Login, devuelve JWT |
| POST | `/api/v1/auth/register` | Registro de usuario |
| GET/PUT/DELETE | `/api/v1/usuarios/{id}` | CRUD de usuarios |
| GET/POST | `/api/v1/hogares` | CRUD de hogares |
| GET/POST | `/api/v1/zonas` | Zonas de un hogar |
| GET/POST | `/api/v1/inventario/{id_hogar}` | Inventario con filtro `?estado=rojo` |
| GET/POST | `/api/v1/productos` | Catálogo de productos |
| GET | `/api/v1/recetas` | Recetas disponibles |
| GET | `/api/v1/alertas` | Alertas no leídas del usuario |
| GET/POST | `/api/v1/listas-compra` | Listas de compra |
| GET | `/api/v1/desperdicio` | Reporte de desperdicio |
| GET | `/api/v1/semaforo` | Estado del semáforo de alimentos |
| GET | `/api/v1/tengo-hambre` | Recetas con ingredientes próximos a vencer |
