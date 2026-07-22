#criação de pedidos pelo cliente, listagem dos pedidos do próprio usuário, e rotas administrativas tipo mudar status do pedido (pendente → pago → enviado).

from fastapi import APIRouter,Depends,HTTPException 
from dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session

requisition_router = APIRouter(prefix="/requisition", tags=['roteador_requisition'])