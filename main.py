#cd c:\users\elito\Project_beauty_parlor
#python -m venv venv

#ativar venv venv\Scripts\activate
#venv\Scripts\activate
#deactivate

#liga o servidor FastAPI uvicorn main:app --reload
# pip install -r requirements.txt

import bcrypt #criptografar as senhas
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


#parte de criptografia
import os
load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALG=os.getenv("ALG")
ACCESS_TOKEN_EXPERIUS_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPERIUS_MINUTES"))

oauth2_schema=OAuth2PasswordBearer(tokenUrl='autenticacao/login_pelo_form')

app= FastAPI()

from auth_routes import auth_router
from requisition_routes import requisition_router
from product_routes import product_router

app.include_router(auth_router)
app.include_router(requisition_router)
app.include_router(product_router)
