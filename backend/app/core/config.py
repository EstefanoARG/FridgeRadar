
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FridgeRadar"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "fridgeradar_db"
    DB_USER: str = "root"
    DB_PASSWORD: str = "admin"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # JWT
    SECRET_KEY: str = "cambia-esto-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Semáforo (días)
    SEMAFORO_AMARILLO_DIAS: int = 7
    SEMAFORO_ROJO_DIAS: int = 2

    # Scheduler
    SCHEDULER_TIMEZONE: str = "America/Lima"

    class Config:
        env_file = ".env"


settings = Settings()
