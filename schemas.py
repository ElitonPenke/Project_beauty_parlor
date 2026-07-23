#no python em si n é preciso fixar o tipo de dados, porem é melhor dizer para melhor a velocidade e integridade

from datetime import date
from pydantic import BaseModel,EmailStr
from typing import Optional, List




#PADRÕES DE INSERVAÇÃO DE DADOS ---------------------------------------
class UsuarioSchema(BaseModel):
    nome:str
    email:EmailStr
    telefone:str
    senha:str
    sexo:str
    dataNascimento:date
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
        
        
class EditServicoSchema(BaseModel):
    titulo:Optional[str]= None
    descricao:Optional[str]= None
    preco:Optional[float]= None
    duracao_min:Optional[int]= None
    
    class Config:
        from_attributes=True
    
    
    
class CorSchema(BaseModel):
    nome:str
    codigo_hex:str
    disponivel:Optional[bool]
    categora:str
    
    class Config:
        from_attributes=True
    
class EditCorSchema (BaseModel):
    nome:Optional[str]= None
    codigo_hex:Optional[str]= None
    disponivel:Optional[bool] = None
    categora:Optional[str]= None
    
    class Config:
        from_attributes=True
    
#PADRÕES DE RESPOSTA DE DADOS ---------------------------------------
