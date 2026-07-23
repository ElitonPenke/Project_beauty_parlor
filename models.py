#para criar e fazer modificações do meu banco de dados 
#alembic init alembic
#alembic revision --autogenerate -m"fist migration"
#alembic upgrade head


from datetime import datetime,timedelta
from sqlalchemy import create_engine,Column,String,Integer,Boolean,Float,ForeignKey,DateTime,Text,Date
from sqlalchemy.orm import declarative_base,relationship

db=create_engine("sqlite:///banco.db")

base=declarative_base()


# cliente
class Cliente(base):
    __tablename__ = "clientes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    telefone = Column("telefone", String, unique=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    sexo = Column("sexo", String, nullable=True)
    dataNascimento = Column("dataNascimento", Date, nullable=True)
    endereco = Column("endereco", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)
    data_cadastro = Column("data_cadastro", DateTime, default=datetime.now)

    def __init__(self, nome, email,telefone,senha,sexo,dataNascimento,endereco,ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.sexo = sexo
        self.dataNascimento = dataNascimento
        self.endereco = endereco
        self.ativo = ativo
        self.admin = admin


# servico
class Servico(base):
    __tablename__ = "servicos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String, nullable=False)
    descricao = Column("descricao", Text, nullable=False)
    preco = Column("preco", Float, nullable=False)
    duracao_min = Column("duracao_min", Integer, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    data_cadastro = Column("data_cadastro", DateTime, default=datetime.now)

    def __init__(self, titulo, preco,ativo,duracao_min,descricao=None):
        self.titulo = titulo
        self.preco = preco
        self.ativo=ativo
        self.duracao_min = duracao_min
        self.descricao = descricao


# agendamento
class Agendamento(base):
    __tablename__ = "agendamentos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", Integer, ForeignKey("clientes.id"), nullable=False)
    data = Column("data", Date, nullable=False)
    horario_inicio = Column("horario_inicio", DateTime, nullable=False)
    horario_termino = Column("horario_termino", DateTime, nullable=True)
    status = Column("status", String, default="pendente")
    presenca_confirmada = Column("presenca_confirmada", Boolean, default=False)
    observacao = Column("observacao", Text, nullable=True)

    # deletar um agendamento, o SQLAlchemy deleta junto todas as linhas de agendamento_servico que apontam pra ele
    servicos = relationship("AgendamentoServico", back_populates="agendamento", cascade="all,delete")    
    #so para puxar quem junto de qm é
    cliente_relacionamento = relationship("Cliente")

    def __init__(self, id_cliente, data, horario_inicio,observacao ,status="pendente",horario_termino=None):
        self.id_cliente = id_cliente
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_termino = horario_termino
        self.status = status
        self.observacao = observacao

    def calcular_termino(self):
        #soma de todos os min dos items de serviços dentro do agendamento
        total_min = sum(item.duracao_total_momento for item in self.servicos)
        self.horario_termino = self.horario_inicio+ timedelta(minutes=total_min)
        
    def calcular_preco(self):
        #soma o preco dos itme em servico
        return sum(item.preco_momento for item in self.servicos)


# agendamento_servico (tabela de junção entre um agendamente e um serviço em si == N:N)
class AgendamentoServico(base):
    __tablename__ = "agendamento_servico"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_agendamento = Column("id_agendamento", Integer, ForeignKey("agendamentos.id"), nullable=False)
    id_servico = Column("id_servico", Integer, ForeignKey("servicos.id"), nullable=False)
    id_cor = Column("id_cor", Integer, ForeignKey("cores.id"), nullable=True)
    preco_momento = Column("preco_momento", Float, nullable=False)
    duracao_total_momento = Column("duracao_momento", Integer, nullable=False)

    #para ver direto,sem precisa de query manual
    servico = relationship("Servico")
    agendamento = relationship("Agendamento", back_populates="servicos")
    core=relationship("Cor")
    
    def __init__(self, id_agendamento, id_servico,id_cor, preco_momento, duracao_total_momento):
        self.id_agendamento = id_agendamento
        self.id_servico = id_servico
        self.id_cor=id_cor
        self.preco_momento = preco_momento
        self.duracao_total_momento = duracao_total_momento
            
class Cor(base):
    __tablename__ = "cores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    codigo_hex = Column("codigo_hex", String, nullable=True)
    disponivel = Column("disponivel", Boolean, default=True)
    categoria = Column("categoria",String,nullable=False)

    def __init__(self, nome,categoria,codigo_hex=None, disponivel=True):
        self.nome = nome
        self.codigo_hex = codigo_hex
        self.disponivel = disponivel
        self.categoria=categoria


# notificacao
class Notificacao(base):
    __tablename__ = "notificacoes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_agendamento = Column("id_agendamento", Integer, ForeignKey("agendamentos.id"), nullable=False)
    tipo = Column("tipo", String, nullable=False)   
    canal = Column("canal", String, nullable=False)   
    enviado_em = Column("enviado_em", DateTime, default=datetime.now)

    def __init__(self, id_agendamento, tipo, canal):
        self.id_agendamento = id_agendamento
        self.tipo = tipo
        self.canal = canal


class Bloqueio(base):
    __tablename__ = "bloqueios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    data = Column("data", Date, nullable=False)
    dia_inteiro=Column("dia_inteiro",Boolean,default=True)
    hora_inicio = Column("hora_inicio", DateTime, nullable=True) 
    hora_fim = Column("hora_fim", DateTime, nullable=True)
    motivo = Column("motivo", String, nullable=False)
    criado_em = Column("criado_em", DateTime, default=datetime.now)

    def __init__(self, data,dia_inteiro=True, hora_inicio=None, hora_fim=None, motivo=None):
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.motivo = motivo
        self.dia_inteiro=dia_inteiro