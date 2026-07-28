from fastapi import APIRouter

notification_router = APIRouter(prefix="/notification", tags=['roteador_notification'])

"""

Notificações
GET /notificacoes/ ➔ def listar_notificacoes()

POST /notificacoes/ ➔ def adicionar_notificacao()

PUT /notificacoes/{notificacao_id} ➔ def editar_notificacao()

DELETE /notificacoes/{notificacao_id} ➔ def apagar_notificacao()"""