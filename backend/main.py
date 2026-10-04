from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import UsuarioCadastro, UsuarioLogin
from mysql.connector import Error
from database import conectar
from seguranca import gerar_hash, verificar_senha, criar_token, obter_usuario_id

app = FastAPI(title="Hydrates API")

bearer_scheme = HTTPBearer()

def usuario_autenticado(
        credenciais: HTTPAuthorizationCredentials = Depends(bearer_scheme)
        ) -> int:
    return obter_usuario_id(credenciais.credentials)

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
def login_usuario(dados: UsuarioLogin):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT id, nome, email, senha_hash FROM usuario WHERE email = %s
        """
        cursor.execute(sql, (dados.email,))
        usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(
                status_code=401,
                detail="Email ou senha incorretos."
            )
        senha_correta = verificar_senha(
            dados.senha,
            usuario["senha_hash"]
        )
        if not senha_correta:
            raise HTTPException(
                status_code=401,
                detail="Email ou senha incorretos."
            )
        token = criar_token({
            "sub": str(usuario["id"])
            })
        return {
            "mensagem": "Login realizado com sucesso!",
            "access_token": token,
            "token_type": "bearer",
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"]
        }
    except HTTPException:
        raise

    except Error as erro:
        print("ERRO MYSQL NO LOGIN:", erro)
        raise HTTPException(
            status_code=500,
            detail="Erro ao realizar login."
        )
    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()

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