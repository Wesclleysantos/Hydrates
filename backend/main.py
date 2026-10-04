from fastapi import FastAPI
from schemas import UsuarioCadastro

app = FastAPI(title="Hydrates API")

@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo à API do Hydrates!"}

@app.post("/usuario")
def criar_usuario(usuario: UsuarioCadastro):
    return {"mensagem": "Dados recebidos com sucesso!",
            "nome": usuario.nome,
            "nickname": usuario.nickname,
            "email": usuario.email,
            "idade": usuario.idade,
            "peso": usuario.peso}

@app.post("/login")
def login_usuario():
    return {"mensagem": "Login realizado com sucesso!"}

@app.post("/consumos")
def registrar_consumo():
    return {"mensagem": "Consumo registrado com sucesso!"}  

@app.get("/consumos")
def listar_consumos():
    return {"mensagem": "Lista de consumos."}

@app.get("/bebidas")
def listar_bebidas():
    return {"mensagem": "Lista de bebidas."}

@app.post("/metas")
def criar_meta():
    return {"mensagem": "Meta criada com sucesso!"}

@app.get("/metas")
def listar_metas():
    return {"mensagem": "Lista de metas."}