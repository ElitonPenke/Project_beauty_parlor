from fastapi import Depends,HTTPException
from sqlalchemy.orm import sessionmaker,Session # aqui faz uma seção para n ter paraleelismo de compretividade de requisições no meu banco de dados
from models import db, cliente #importar para fazer pesquisa no meu bd
import jwt
from main import SECRET_KEY,ALG,oauth2_schema

#ao inves de colocar para abrie e fechar um sessao em cada lugar do codigo aonde tem rotas ao meu banco e dados, vamos fazer uma def para reutlizar em todo o codigo

def pegar_sessao():
    
    try:
        Session=sessionmaker(bind=db)#faz a 'fabrica' de seções
        session=Session() # aqui eu abro uma seção, porem tenho que fechar ele
        yield session #retorna um valor, porem n encerra a def
    
    finally: #para que independete se deu certo,errado, ele fecha a session para n sobrecarregar o banco e dados
        session.close()

#interresante utilizar aqui para utilizar em varias rotas
def verificar_token(token: str = Depends(oauth2_schema),session = Depends(pegar_sessao)):
    try:
        dic_info=jwt.decode(token,SECRET_KEY,ALG)
        id_usuario=dic_info.get("sub")
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail='Acesso negado(acess token n confirma)')
        
    
    #qual user é o dono do token
    usuario=session.query(user).filter(user.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401,detail='acesso invalido(user n existe)')
    return usuario