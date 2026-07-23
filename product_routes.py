#CRUD de produtos: criar, editar, listar, deletar, exigem admin.
from fastapi import APIRouter,Depends,HTTPException
from dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from models import Cliente, Servico,Cor
from schemas import ServicoSchema,EditServicoSchema,CorSchema,EditCorSchema


#sempre que quiser pegar alguma infromação do banco para verificar e tals, sempre usar o session.query("tabela").filter("tabela".coluna == ....)

product_router = APIRouter(prefix="/product", tags=['roteador_product']) 


@product_router.get("/")
async def product():
    return {"mensagem": "Roteador de produtos funcionando!"}


#serviços ------------------------------------------------------------------------------------------------------------------------------------------------
@product_router.post("/criar_servico")
async def adicionar_servico(servico_schema:ServicoSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    novo_servico= Servico(servico_schema.titulo,servico_schema.preco,servico_schema.duracao_min,servico_schema.descricao)
   
    session.add(novo_servico)
    session.commit()
    return {"mensagem": f"Serviço novo cadastrado com sucesso, {novo_servico.titulo}"}

@product_router.get('/listar_servicos')
async def listar_servicos(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
    else:                     
        todos_servicos= session.query(Servico).all()
        return {
            'servicos':todos_servicos
        }

@product_router.post('/servico/desativar_servico/{id_servico}') 

async def desativar_servico(id_servico:int, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    #busco o item aonde os ids batem entre relação do pedido e do item
    item_servico=session.query(Servico).filter(id_servico==Servico.id).first()
    
    print(item_servico)
    
    if not item_servico:
        raise HTTPException(status_code=400,detail="Serviço não encontrado")

    
    if not usuario.admin :
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
        
    item_servico.ativo=False

    session.commit()
    return{
        "mensagem":"Serviço desativado com sucesso"
    }
    
    
@product_router.patch("/edit_servico/{id_servico}")
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

    # 3. Salva no banco
    session.commit()
    session.refresh(servico_editar)

    return {"mensagem": f"O serviço '{servico_editar.titulo}' foi atualizado parcialmente com sucesso!"}
    
    
    
    
    
    

#cor ------------------------------------------------------------------------------------------------------------------------------------------------


@product_router.post("/adicionar_cor")
async def adicionar_cor(cor_schema:CorSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    nova_cor= Cor(cor_schema.nome,cor_schema.categora,cor_schema.codigo_hex,cor_schema.disponivel)
   
    session.add(nova_cor)
    session.commit()
    
    return {"mensagem": f"Cor novo cadastrado com sucesso, {nova_cor.nome}"}

@product_router.get('/listar_cor')
async def listar_cor(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False: 
        raise HTTPException(status_code=401,detail="Função apenas para Admin")
    else:                     
        todas_cores= session.query(Cor).all()
        return {
            'servicos':todas_cores
        }

@product_router.post('/servico/desativar_cor/{id_cor}') 

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
    
    
    
@product_router.patch("/edit_cor/{id_cor}")
async def editar_cor(id_cor:int, atualizar_cor:EditCorSchema, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
        raise HTTPException(status_code=400, detail="Função apenas para Admin") 
    
    cor_editar=session.query(Cor).filter(Cor.id == id_cor).first()
    
    if not cor_editar:
        raise HTTPException(status_code=400,detail="Cor não encontrado")
                                                        #usei o exclude_unset=True para quando ele ver que o campo ficou None, ele ignora e n escreve none no banco, assim n mudando as informações que ja tem no bd
    dados_para_atualizar = atualizar_cor.model_dump(exclude_unset=True)

    for chave, valor in dados_para_atualizar.items():
        setattr(cor_editar, chave, valor)

    # 3. Salva no banco
    session.commit()
    session.refresh(cor_editar)

    return {"mensagem": f"O serviço '{cor_editar.nome}' foi atualizado parcialmente com sucesso!"}

"""
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