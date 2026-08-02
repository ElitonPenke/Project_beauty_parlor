from fastapi import APIRouter,Depends,HTTPException 
from backend.app.dependecies import pegar_sessao,verificar_token,verificar_admin
from sqlalchemy.orm import Session
from backend.app.models import Cliente, AgendamentoServico,Agendamento,Servico,Cor
from backend.app.schemas import AgendamentoSchema

requisition_router = APIRouter(prefix="/requisition", tags=['roteador_requisition'])

#cria um agendamento
@requisition_router.post("/agendamento/criar_agendamento")
async def criar_agendamento(
    agendamento_schema:AgendamentoSchema, 
    session: Session = Depends(pegar_sessao),
    usuario:Cliente = Depends(verificar_token)
    ):
    novo_agendamento= Agendamento(
            id_cliente=usuario.id,
            data=agendamento_schema.data,
            horario_inicio=agendamento_schema.horario_inicio,
            observacao=agendamento_schema.observacao
            )
    
    session.add(novo_agendamento)
    session.flush()


    #para cada serviço em si dentro de serviços de novo_agendamento
    for item in agendamento_schema.servicos:
        #pega o id do serviço
        servico = session.query(Servico).filter(Servico.id == item.id_servico).first()

        if not servico:
            raise HTTPException(status_code=404,detail=f"Serviço {item.id_servico} não encontrado."
            )

        if item.id_cor is not None:
            #vai pegar o id da cor, ou tentar
            cor = session.query(Cor).filter(Cor.id == item.id_cor).first()

            #validação basico de ter ou n no sistema
            if not cor:
                raise HTTPException(status_code=404,detail=f"Cor {item.id_cor} não encontrada.")
        print(item)

        #novo registro na tabela de ligação N:N
        item_agendamento = AgendamentoServico(
            id_agendamento=novo_agendamento.id, #pega o id do item adicionado (novo_agendamento)
            id_servico=servico.id, #a variavel momentanea do loop
            id_cor=item.id_cor, #a variavel momentanea do loop
            preco_momento=servico.preco, #a variavel momentanea do loop
            duracao_total_momento=servico.duracao_min #a variavel momentanea do loop
        )
        
        novo_agendamento.servicos.append(item_agendamento)
        
    session.flush()

    #calcula e escreve no bd
    novo_agendamento.calcular_termino()
    
    
    conflito = session.query(Agendamento).filter(
        Agendamento.id != novo_agendamento.id,
        Agendamento.data == novo_agendamento.data,
        Agendamento.status!="CALCELADO",
        Agendamento.horario_inicio < novo_agendamento.horario_termino,
        Agendamento.horario_termino > novo_agendamento.horario_inicio
    ).first()

    
    if conflito:
        raise HTTPException(status_code=400,detail="Já existe um agendamento nesse horário.")


    preco_total = novo_agendamento.calcular_preco()

    session.commit()

    session.refresh(novo_agendamento)
    return {
        "mensagem": "Agendamento criado com sucesso.",

        "agendamento": {
            "id": novo_agendamento.id,
            "cliente": usuario.nome,
            "data": novo_agendamento.data,
            "inicio": novo_agendamento.horario_inicio,
            "termino": novo_agendamento.horario_termino,
            "status": novo_agendamento.status,
            "observacao": novo_agendamento.observacao,
            "preco_total": preco_total
        }
    }


#cancelar agendamento
@requisition_router.post("/agendamento/cancelar/{id_agendamento}") 
async def cancelar_pedido (id_agendamento: int,session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    agendamento=session.query(Agendamento).filter(Agendamento.id==id_agendamento).first() 
    
    if not agendamento:
        raise HTTPException(status_code=400, detail='Agendamento não encontrado !')
    
    if not usuario.admin and usuario.id != agendamento.id_cliente:
        raise HTTPException(status_code=401,detail='"Função apenas para Admin')


    agendamento.status="CALCELADO"
    session.commit()
    
    return {    
        "mensagem":f' Deu certo o cancelamento do agendamento {agendamento.id}',
        "agendamento":agendamento
    }
    
    
#listar todos agendamentos
@requisition_router.get('/agendamento/listar_agendamento')
async def listar_pedidos(session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    if usuario.admin ==False:
        raise HTTPException(status_code=401,detail='vc n tem autorização para listar os pedidos')
    else:                           
        todos_agendamentos= session.query(Agendamento).all()
        return {
            'agendamentos':todos_agendamentos
        }
        
        
#o usuario pode ver o seu agendamento     
@requisition_router.get("/agendamento/{id_agendamento}")
async def visualizar_pedido (id_agendamento: int,session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    agendamento=session.query(Agendamento).filter(Agendamento.id==id_agendamento).first() 
    if not agendamento:
        raise HTTPException(status_code=400, detail='Agendamento não encontrado!')
    
    if not usuario.admin and usuario.id != agendamento.id_cliente:
        raise HTTPException(status_code=401,detail='"Função apenas para Admin')
    
    return {
        'quantidade_servicos_agendamento': len(Agendamento.servicos),
        'agendamento':agendamento
    }
    
    

#confirmar agendamento
@requisition_router.post("/agendamento/confirmar/{id_agendamento}") 
async def confrimar_agendamento (id_agendamento: int,session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    agendamento=session.query(Agendamento).filter(Agendamento.id==id_agendamento).first() 
    
    if not agendamento:
        raise HTTPException(status_code=400, detail='Agendamento não encontrado !')
    
    agendamento.status="confirmado_agendamento"
    agendamento.presenca_confirmada=True
    
    session.commit()
    
    return {    
        "mensagem":f' Agendamento confirmado {agendamento.id}',
        "agendamento":agendamento
    }

#finalizar/concluir agendamento
@requisition_router.post("/agendamento/finalizar/{id_agendamento}") 
async def confrimar_agendamento (id_agendamento: int,session:Session = Depends(pegar_sessao),usuario:Cliente = Depends(verificar_token)):
    
    agendamento=session.query(Agendamento).filter(Agendamento.id==id_agendamento).first() 
    
    if not agendamento:
        raise HTTPException(status_code=400, detail='Agendamento não encontrado !')
    
    agendamento.status="Agendamento/serviço concluído"
        
    session.commit()
    
    return {    
        "mensagem":f' Agendamento concluído {agendamento.id}',
        "agendamento":agendamento
    }
    