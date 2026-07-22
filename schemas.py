#no python em si n é preciso fixar o tipo de dados, porem é melhor dizer para melhor a velocidade e integridade

from pydantic import BaseModel,EmailStr
from typing import Optional, List




#PADRÕES DE INSERVAÇÃO DE DADOS ---------------------------------------
class UsuarioSchema(BaseModel):
    nome:str
    email:EmailStr
    telefone:str
    senha:str
    endereco:str

    ativo:Optional[bool]
    admin:Optional[bool]
    
    #crio um subclass para linkar com o meu models do db(vai ser interpretado para tranformar para SQL)
    class Config:
        from_attributes=True
 
class LoginSchema(BaseModel):
    email:str
    senha:str
    
    class Config:
        from_attributes=True
        
class ServicoSchema(BaseModel):
    titulo:str
    descricao:str
    preco:float
    duracao_min:int
    
    class Config:
        from_attributes=True
    
#PADRÕES DE RESPOSTA DE DADOS ---------------------------------------
