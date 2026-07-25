#criação de pedidos pelo cliente, listagem dos pedidos do próprio usuário, e rotas administrativas tipo mudar status do pedido (pendente → pago → enviado).

from fastapi import APIRouter,Depends,HTTPException 
from dependecies import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from models import Cliente, AgendamentoServico,Agendamento,Servico,Cor
from schemas import AgendamentoSchema

requisition_router = APIRouter(prefix="/requisition", tags=['roteador_requisition'])

@requisition_router.get("/")
async def listar_produtos():
    return {"mensagem": "Roteador de requisições funcionando!"}



@requisition_router.post("/criar_agendamento")
async def criar_agendamento(
    agendamento_schema:AgendamentoSchema, 
    session: Session = Depends(pegar_sessao),
    usuario:Cliente = Depends(verificar_token)
    ):
       
    try: 
        novo_agendamento= Agendamento(
                id_cliente=usuario.id,
                data=agendamento_schema.data,
                horario_inicio=agendamento_schema.horario_inicio,
                observacao=agendamento_schema.observacao
                )

        print(novo_agendamento)
        
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
            print(item_agendamento)
            
            session.add(item_agendamento)
            
        session.flush()

        #calcula e escreve no bd
        novo_agendamento.calcular_termino()
        
        hora_termino=novo_agendamento.calcular_termino()
        
        # conflito = session.query(Agendamento).filter(
        # Agendamento.data == novo_agendamento.data,
        # Agendamento.horario_inicio < hora_termino,
        # Agendamento.horario_termino > novo_agendamento.horario_inicio).first()

        # if conflito:
        #     raise HTTPException(status_code=400,detail="Já existe um agendamento nesse horário.")


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
    except:
        session.rollback()
        raise
