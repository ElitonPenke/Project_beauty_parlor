#CRUD de produtos: criar, editar, listar, deletar. Normalmente rotas de escrita (criar/editar/deletar) exigem admin.

from fastapi import APIRouter,Depends,HTTPException # roteador que vai fazer o modelo, o caminho para abri e fechar o banco e a questão de 
from dependecies import pegar_sessao,verificar_token


from sqlalchemy.orm import Session


#sempre que quiser pegar alguma infromação do banco para verificar e tals, sempre usar o session.query("tabela").filter("tabela".coluna == ....)

product_router = APIRouter(prefix="/product", tags=['roteador_product']) 