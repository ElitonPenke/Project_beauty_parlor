import re
from fastapi import HTTPException
from models import Servico, Cor, Agendamento, Bloqueio, AgendamentoServico


padrao_telefone = re.compile(r"([0-9]{2,3}?)?([1-9]{2})([6-9])?([0-9]{4})([0-9]{4})")

def validar_telefone(telefone: str) -> str:
    numero = re.sub(r"\D", "", telefone)
    if not (10 <= len(numero) <= 14) or not padrao_telefone.fullmatch(numero):
        raise ValueError("numero de telefone invalido")
    return numero

def montar_itens_servico(session, id_agendamento, servicos_schema):
    """Valida cada serviço/cor do schema e monta os registros de ligação N:N."""
    
    itens = []
    
    for item in servicos_schema:
        servico = session.query(Servico).filter(Servico.id == item.id_servico).first()
        if not servico:
            raise HTTPException(status_code=404, detail=f"Serviço {item.id_servico} não encontrado.")

        if item.id_cor is not None:
            cor = session.query(Cor).filter(Cor.id == item.id_cor).first()
            if not cor:
                raise HTTPException(status_code=404, detail=f"Cor {item.id_cor} não encontrada.")

        itens.append(AgendamentoServico(
            id_agendamento=id_agendamento,
            id_servico=servico.id,
            id_cor=item.id_cor,
            preco_momento=servico.preco,
            duracao_total_momento=servico.duracao_min
        ))
    return itens


def verificar_conflito_horario(session, agendamento):
    conflito = session.query(Agendamento).filter(
        Agendamento.id != agendamento.id,
        Agendamento.data == agendamento.data,
        Agendamento.status != "CANCELADO",
        Agendamento.horario_inicio < agendamento.horario_termino,
        Agendamento.horario_termino > agendamento.horario_inicio
    ).first()

    if conflito:
        raise HTTPException(status_code=400, detail="Já existe um agendamento nesse horário.")


def verificar_bloqueio(session, agendamento):
    bloqueios_do_dia = session.query(Bloqueio).filter(Bloqueio.data == agendamento.data).all()

    for bloqueio in bloqueios_do_dia:
        if bloqueio.dia_inteiro:
            raise HTTPException(status_code=400, detail="Esse dia está bloqueado para agendamentos.")

        # bloqueio parcial: mesma lógica de sobreposição usada no conflito de horário
        if bloqueio.hora_inicio < agendamento.horario_termino and bloqueio.hora_fim > agendamento.horario_inicio:
            raise HTTPException(status_code=400, detail=f"Horário bloqueado: {bloqueio.motivo}")
        
def validar_dados_bloqueio(dia_inteiro: bool, hora_inicio, hora_fim):
    """Garante a regra: dia inteiro sem horas, OU horas preenchidas sem dia inteiro."""
    if dia_inteiro:
        if hora_inicio is not None or hora_fim is not None:
            raise HTTPException(status_code=400, detail="Bloqueio de dia inteiro não deve ter hora_inicio/hora_fim preenchidos.")
    else:
        if hora_inicio is None or hora_fim is None:
            raise HTTPException(status_code=400, detail="Bloqueio parcial precisa de hora_inicio e hora_fim preenchidos.")
        if hora_inicio >= hora_fim:
            raise HTTPException(status_code=400, detail="hora_inicio deve ser anterior a hora_fim.")