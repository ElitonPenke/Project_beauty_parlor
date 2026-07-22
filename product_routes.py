#CRUD de produtos: criar, editar, listar, deletar, exigem admin.
from fastapi import APIRouter,Depends,HTTPException
from dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from models import Cliente, Servico
from schemas import ServicoSchema


#sempre que quiser pegar alguma infromação do banco para verificar e tals, sempre usar o session.query("tabela").filter("tabela".coluna == ....)

product_router = APIRouter(prefix="/product", tags=['roteador_product']) 


@product_router.get("/")
async def product():
    return {"mensagem": "Roteador de produtos funcionando!"}
"""
Serviços
GET /servicos/ ➔ def listar_servicos()

PUT /servicos/{servico_id} ➔ def editar_servico()

DELETE /servicos/{servico_id} ➔ def apagar_servico()
"""
@product_router.post("/servicos")
async def adicionar_servico(servico_schema:ServicoSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    novo_servico= Servico(servico_schema.titulo,servico_schema.preco,servico_schema.duracao_min,servico_schema.descricao)
   
    session.add(novo_servico)
    session.commit()
    return {"mensagem": f"Serviço novo cadastrado com sucesso {novo_servico.titulo}"}




"""
 Cores
GET /cores/ ➔ def listar_cores()

POST /cores/ ➔ def adicionar_cor()

PUT /cores/{cor_id} ➔ def editar_cor()

DELETE /cores/{cor_id} ➔ def apagar_cor()

Bloqueios de Agenda
GET /bloqueios/ ➔ def listar_bloqueios()

POST /bloqueios/ ➔ def adicionar_bloqueio()

PUT /bloqueios/{bloqueio_id} ➔ def editar_bloqueio()

DELETE /bloqueios/{bloqueio_id} ➔ def apagar_bloqueio()

Notificações
GET /notificacoes/ ➔ def listar_notificacoes()

POST /notificacoes/ ➔ def adicionar_notificacao()

PUT /notificacoes/{notificacao_id} ➔ def editar_notificacao()

DELETE /notificacoes/{notificacao_id} ➔ def apagar_notificacao()"""