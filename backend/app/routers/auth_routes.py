from fastapi import APIRouter,Depends,HTTPException 
from fastapi.security import OAuth2PasswordRequestForm 
from backend.app.models import Cliente
from backend.app.dependecies import pegar_sessao,verificar_token
from backend.app.schemas import EditUsuarioSchema, UsuarioSchema,LoginSchema 
from backend.app.main import bcrypt,ACCESS_TOKEN_EXPERIUS_MINUTES,ALG,SECRET_KEY
import jwt
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone

from backend.app.utils.validadores import validar_telefone

auth_router = APIRouter(prefix="/authentication", tags=['roteador_authentication'])

#----------------------------------------------------------------------------------------------------------------
#jwt (json web token)
def criar_token(id_usuario,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPERIUS_MINUTES)):
    data_experacao=datetime.now(timezone.utc) + duracao_token
    
    dic_info={"sub":str(id_usuario),"exp":data_experacao}
    
    jwt_cript=jwt.encode(dic_info,SECRET_KEY,ALG)
    
    return jwt_cript

#----------------------------------------------------------------------------------------------------------------
def autenticar_usuario(email,senha,session):
    usuario = session.query(Cliente).filter(Cliente.email==email).first()
    
    if not usuario:
        return False
    elif not bcrypt.checkpw(senha.encode('utf-8'),usuario.senha.encode('utf-8')):
        return False
    return usuario

#----------------------------------------------------------------------------------------------------------------

@auth_router.post("/criar_conta")                
async def criar_conta(cliente_Schema:UsuarioSchema,session:Session = Depends(pegar_sessao)): 
    
    try:
        telefone_validado = validar_telefone(cliente_Schema.telefone)
    except ValueError:
        raise HTTPException(status_code=400, detail="numero de telefone invalido")
    
    usuario= session.query(Cliente).filter(Cliente.email==cliente_Schema.email).first()
    celular=session.query(Cliente).filter(Cliente.telefone==cliente_Schema.telefone).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail="ja existe um usuario com esse email")
    if celular:
        raise HTTPException(status_code=400, detail="ja existe um usuario com esse telefone")
   
    senha_criptgrafada=bcrypt.hashpw(cliente_Schema.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    novo_usuario= Cliente(
        nome=cliente_Schema.nome,
        email=cliente_Schema.email,
        telefone=cliente_Schema.telefone,
        senha=senha_criptgrafada, 
        sexo=cliente_Schema.sexo,
        dataNascimento=cliente_Schema.dataNascimento,
        endereco=cliente_Schema.endereco,
        ativo=cliente_Schema.ativo,  
        admin=cliente_Schema.admin
        )
    
    session.add(novo_usuario)
    session.commit() 
    
    return {"mensagem": f"Usuario cadastrado com sucesso meu chapa, bem vindo {cliente_Schema.nome}"}
    
#----------------------------------------------------------------------------------------------------------------

@auth_router.post("/criar_conta_admin")                     
async def criar_conta_admin(cliente_Schema:UsuarioSchema,session:Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)): 
    
    Usuario= session.query(Cliente).filter(Cliente.email==cliente_Schema.email).first() 
    
    if Usuario:
        raise HTTPException(status_code=400, detail="ja existe um usuario com esse email")
    else:
        if usuario.admin==False:
            raise HTTPException(status_code=400, detail="Você não possui autorização")
    
        senha_criptgrafada=bcrypt.hashpw(cliente_Schema.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        novo_usuario= Cliente(cliente_Schema.nome,cliente_Schema.email,cliente_Schema.telefone,senha_criptgrafada,cliente_Schema.sexo,cliente_Schema.dataNascimento,cliente_Schema.endereco,cliente_Schema.ativo,cliente_Schema.admin)
        
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuario ADMIN cadastrado com sucesso {cliente_Schema.nome}"}
    
#----------------------------------------------------------------------------------------------------------------
#login ->email e senha - > token JWT
@auth_router.post("/login")
async def login(login_schema:LoginSchema,session:Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(login_schema.email, login_schema.senha,session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="cliente ñ encontrado ou senha incorreta")
    else:
        #cria um token para o cliente
        access_token = criar_token(usuario.id)
        refresh_token=criar_token(usuario.id,duracao_token=timedelta(days=15))
        return {
            'access_token':access_token,
            'refresh_token':refresh_token,
            'token_type': "Bearer"
                }

#----------------------------------------------------------------------------------------------------------------
#utilizar o token refresh, verifica a entrada token verificado e atualiza
@auth_router.get("/refresh")
async def use_refresh_token(usuario:Cliente = Depends(verificar_token)):
    
    access_token=criar_token(Cliente.id)
    return {
            'access_token':access_token,
            'token_type': "Bearer"
            }


#editar perfil
@auth_router.patch("/editar_perfil/{id_conta}")
async def editar_servico(id_conta:int, atualizar_perfil:EditUsuarioSchema, session: Session = Depends(pegar_sessao), usuario:Cliente = Depends(verificar_token)):
    
    if usuario.id != id_conta and not usuario.admin:
        raise HTTPException(status_code=400, detail="Função apenas para Admin") 

    perfil_editar=session.query(Cliente).filter(Cliente.id == id_conta).first()
    
    if not perfil_editar:
        raise HTTPException(status_code=400,detail="Usuario não encontrado")
    
    dados_para_atualizar = atualizar_perfil.model_dump(exclude_unset=True)

    for chave, valor in dados_para_atualizar.items():
        setattr(perfil_editar, chave, valor)

    session.commit()
    session.refresh(perfil_editar)

    return {"mensagem": f"Seu perfil '{perfil_editar.nome}' foi atualizado parcialmente com sucesso!"}
    
    
    
    
    
#----------------------------------------------------------------------------------------------------------------
#para testar na documentação o login por meio no oauth2 
@auth_router.post("/login_pelo_form")
async def login_pelo_form(dados_formulario:OAuth2PasswordRequestForm=Depends() ,session: Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password,session)
    
    if not usuario:
        print("n achou")
        raise HTTPException(status_code=400, detail="cliente ñ encontrado ou senha incorreta")
    else:
        #cria um token para o cliente
        access_token = criar_token(usuario.id)

        return {
            'access_token':access_token,
            'token_type': "Bearer"
                }