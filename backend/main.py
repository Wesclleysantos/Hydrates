from fastapi import FastAPI, HTTPException
from schemas import UsuarioCadastro
from mysql.connector import Error
from database import conectar
from seguranca import gerar_hash

app = FastAPI(title="Hydrates API")

@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo à API do Hydrates!"}

@app.post("/usuario", status_code=201)
def criar_usuario(usuario: UsuarioCadastro):
    conexao =None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        senha_hash = gerar_hash(usuario.senha)
        sql = """
        INSERT INTO usuario (nome, nickname, email, senha_hash, idade, peso)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (usuario.nome, 
                   usuario.nickname, 
                   usuario.email, 
                   senha_hash,
                   usuario.idade, 
                   usuario.peso
        ) 
        cursor.execute(sql, valores)
        conexao.commit()
        
        return {"mensagem": "Dados recebidos com sucesso!",
                "nome": usuario.nome,
                "nickname": usuario.nickname,
                "email": usuario.email,
                "idade": usuario.idade,
                "peso": usuario.peso}
    except Error as erro:
        print("ERRO MYSQL:", erro)
        if conexao is not None:
            conexao.rollback()

        if erro.errno == 1062:
            raise HTTPException(status_code=409, detail="Email ou nickname já cadastrado.")
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário.")
    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()
    
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