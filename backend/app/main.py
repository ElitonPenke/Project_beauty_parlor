#ativar --  .\venv\Scripts\activate
#deactivate

#liga o servidor FastAPI uvicorn backend.app.main:app --reload
# pip install -r requirements.txt

import bcrypt #criptografar as senhas
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

#esse é para o meu react acessar o fast api 
from fastapi.middleware.cors import CORSMiddleware


#parte de criptografia
import os
load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALG=os.getenv("ALG")
ACCESS_TOKEN_EXPERIUS_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPERIUS_MINUTES"))

oauth2_schema=OAuth2PasswordBearer(tokenUrl='authentication/login_pelo_form')

app= FastAPI()

# Configurar CORS, o cara que ibnterliga tudo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  #o "servidor" react do meu front 
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos, tipo o get,post,delet ...
    allow_headers=["*"],  # permite enviar os tokens
)

from backend.app.routers.auth_routes import auth_router
from backend.app.routers.requisition_routes import requisition_router
from backend.app.routers.services_routes import services_router
from backend.app.routers.colors_routes import colors_router
from backend.app.routers.notification_routes import notification_router
from backend.app.routers.loked_routes import loked_router

app.include_router(auth_router)
app.include_router(requisition_router)
app.include_router(services_router)
app.include_router(colors_router)
app.include_router(loked_router)
app.include_router(notification_router)
