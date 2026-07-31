from fastapi import APIRouter,Depends,HTTPException
from dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from models import Cliente, Servico
from schemas import ServicoSchema,EditServicoSchema

services_router = APIRouter(prefix="/services", tags=['roteador_services']) 

#criar novo serviço 
@services_router.post("/servico/criar_servico")
async def adicionar_servico(servico_schema:ServicoSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
            raise HTTPException(status_code=401,detail="Função apenas para Admin")
        
    novo_servico = Servico(
    titulo=servico_schema.titulo,
    preco=servico_schema.preco,
    ativo=servico_schema.ativo,
    duracao_min=servico_schema.duracao_min,
    descricao=servico_schema.descricao,
)

    session.add(novo_servico)
    session.commit()
    return {"mensagem": f"Serviço novo cadastrado com sucesso, {novo_servico.titulo}"}

#listar serviços existentes
@services_router.get("/servicos/listar_servicos")
async def listar_servicos(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
    else:                     
        todos_servicos= session.query(Servico).all()
        return {
            'servicos':todos_servicos
        }

#desativar algum serviço
@services_router.post('/servicos/{id_servico}/desativar') 
async def desativar_servico(id_servico:int, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    #busco o item aonde os ids batem entre relação do pedido e do item
    item_servico=session.query(Servico).filter(id_servico==Servico.id).first()
        
    if not usuario.admin :
            raise HTTPException(status_code=401,detail="Função apenas para Admin")
    
    if not item_servico:
        raise HTTPException(status_code=400,detail="Serviço não encontrado")

    item_servico.ativo=False

    session.commit()
    return{
        "mensagem":"Serviço desativado com sucesso"
    }
    
    
#editar algum serviço
@services_router.patch("/servico/editar_servico/{id_servico}")
async def editar_servico(id_servico:int, atualizar_servico:EditServicoSchema, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
        raise HTTPException(status_code=400, detail="Função apenas para Admin") 
    
    servico_editar=session.query(Servico).filter(Servico.id == id_servico).first()
    
    if not servico_editar:
        raise HTTPException(status_code=400,detail="Serviço não encontrado")
                                                        #usei o exclude_unset=True para quando ele ver que o campo ficou None, ele ignora e n escreve none no banco, assim n mudando as informações que ja tem no bd
    dados_para_atualizar = atualizar_servico.model_dump(exclude_unset=True)

    for chave, valor in dados_para_atualizar.items():
        setattr(servico_editar, chave, valor)

    session.commit()
    session.refresh(servico_editar)

    return {"mensagem": f"O serviço '{servico_editar.titulo}' foi atualizado parcialmente com sucesso!"}
    
    
    
    
    
