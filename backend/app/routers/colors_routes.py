from fastapi import APIRouter,Depends,HTTPException
from backend.app.dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from backend.app.models import Cliente,Cor
from backend.app.schemas import CorSchema,EditCorSchema

colors_router = APIRouter(prefix="/colors", tags=['roteador_colors']) 

@colors_router.post("/adicionar_cor")
async def adicionar_cor(cor_schema:CorSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    nova_cor= Cor(cor_schema.nome,cor_schema.categora,cor_schema.codigo_hex,cor_schema.disponivel)
   
    session.add(nova_cor)
    session.commit()
    
    return {"mensagem": f"Cor novo cadastrado com sucesso, {nova_cor.nome}"}

@colors_router.get('/listar_cor')
async def listar_cor(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
                
    todas_cores= session.query(Cor).all()
    return {
        'servicos':todas_cores
    }

@colors_router.post("/{id_cor}/desativar") 

async def desativar_cor(id_cor:int, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
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
    
    
    
@colors_router.patch("/editar_cor/{id_cor}")
async def editar_cor(id_cor:int, atualizar_cor:EditCorSchema, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
        raise HTTPException(status_code=400, detail="Função apenas para Admin") 
    
    cor_editar=session.query(Cor).filter(Cor.id == id_cor).first()
    
    if not cor_editar:
        raise HTTPException(status_code=400,detail="Cor não encontrado")
    dados_para_atualizar = atualizar_cor.model_dump(exclude_unset=True)

    for chave, valor in dados_para_atualizar.items():
        setattr(cor_editar, chave, valor)

    session.commit()
    session.refresh(cor_editar)

    return {"mensagem": f"O serviço '{cor_editar.nome}' foi atualizado parcialmente com sucesso!"}