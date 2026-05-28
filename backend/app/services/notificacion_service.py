from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.alerta import AlertaResponse


class NotificacionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def notificar_alerta(self, id_usuario: int, alerta: AlertaResponse) -> bool:
        return True

    async def notificar_recordatorio(self, id_usuario: int) -> int:
        return 0
