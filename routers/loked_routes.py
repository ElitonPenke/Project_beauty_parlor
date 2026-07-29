from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import pegar_sessao, verificar_admin, verificar_token
from models import Bloqueio,Cliente
from schemas import BloqueioSchema


loked_router = APIRouter(prefix="/loked", tags=['roteador_loked'],dependencies=[Depends(verificar_admin)])


@loked_router.post("/bloqueio/adicionar_bloqueio")
async def adicionar_bloqueio(bloquio_schema:BloqueioSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    novo_bloquio= Bloqueio(data=)
   
    session.add(novo_bloquio)
    session.commit()
    
    return {"mensagem": f"Cor novo cadastrado com sucesso, {nova_cor.nome}"}
"""
@product_router.get('/bloqueio/listar_bloqueio')
async def listar_bloqueio(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
    else:                     
        todas_cores= session.query(Cor).all()
        return {
            'servicos':todas_cores
        }

@product_router.post('/bloqueio/desativar_bloqueio/{id_bloqueio}') 

async def desativar_bloqueio(id_cor:int, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    #busco o item aonde os ids batem entre relação do pedido e do item
    core=session.query(Cor).filter(id_cor==Cor.id).first()
    
    print(core)
    
    if not core:
        raise HTTPException(status_code=400,detail="Serviço não encontrado")

    
    if not usuario.admin :
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
        
    core.disponivel=False

    session.commit()
    return{
        "mensagem":"Cor desativado com sucesso"
    }
    
    
    
@product_router.patch("/bloqueio/edit_bloqueio/{id_bloqueio}")
async def editar_bloqueio(id_cor:int, atualizar_cor:EditCorSchema, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
        raise HTTPException(status_code=400, detail="Função apenas para Admin") 
    
    cor_editar=session.query(Cor).filter(Cor.id == id_cor).first()
    
    if not cor_editar:
        raise HTTPException(status_code=400,detail="Cor não encontrado")
    dados_para_atualizar = atualizar_cor.model_dump(exclude_unset=True)

    for chave, valor in dados_para_atualizar.items():
        setattr(cor_editar, chave, valor)

    # 3. Salva no banco
    session.commit()
    session.refresh(cor_editar)

    return {"mensagem": f"O serviço '{cor_editar.nome}' foi atualizado parcialmente com sucesso!"}
"""