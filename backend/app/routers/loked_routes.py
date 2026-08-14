from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.dependecies import pegar_sessao, verificar_admin, verificar_token
from backend.app.models import Bloqueio,Cliente
from backend.app.schemas import BloqueioSchema
from backend.app.utils.validadores import validar_dados_bloqueio


loked_router = APIRouter(prefix="/loked", tags=['roteador_loked'],dependencies=[Depends(verificar_admin)])


@loked_router.post("/bloqueio/adicionar_bloqueio")
async def adicionar_bloqueio(bloquio_schema:BloqueioSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    validar_dados_bloqueio(bloquio_schema.dia_inteiro, bloquio_schema.hora_inicio, bloquio_schema.hora_fim)
    
    novo_bloqueio= Bloqueio(data=bloquio_schema.data,dia_inteiro=bloquio_schema.dia_inteiro,
                            hora_inicio=bloquio_schema.hora_inicio,hora_fim=bloquio_schema.hora_fim,motivo=bloquio_schema.motivo)
   
    session.add(novo_bloqueio)
    session.commit()
    
    return {"mensagem": f"Bloquio novo cadastrado com sucesso, {novo_bloqueio.data}"}

@loked_router.get('/bloqueio/listar_bloqueio')
async def listar_bloqueio(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
    else:                     
        todos_bloquios= session.query(Bloqueio).all()
        return {
            'Bloqueios':todos_bloquios
        }

@loked_router.post('/bloqueio/apagar_bloqueio/{id_bloqueio}') 

async def deletar_bloqueio(id_bloqueio:int, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    #busco o item aonde os ids batem entre relação do pedido e do item
    Broke=session.query(Bloqueio).filter(id_bloqueio==Bloqueio.id).first()
        
    if not Broke:
        raise HTTPException(status_code=400,detail="Serviço não encontrado")

    session.delete(Broke)

    session.commit()
    return{
        "mensagem":"Cor desativado com sucesso"
    }
    
    
    