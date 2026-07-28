from fastapi import APIRouter

loked_router = APIRouter(prefix="/loked", tags=['roteador_loked'])

"""
@product_router.post("/bloqueio/adicionar_bloqueio")
async def adicionar_bloqueio(cor_schema:CorSchema, session: Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Função apenas para Admin") 
        
    nova_cor= Cor(cor_schema.nome,cor_schema.categora,cor_schema.codigo_hex,cor_schema.disponivel)
   
    session.add(nova_cor)
    session.commit()
    
    return {"mensagem": f"Cor novo cadastrado com sucesso, {nova_cor.nome}"}

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