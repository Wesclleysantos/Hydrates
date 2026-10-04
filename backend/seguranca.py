import os
import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

hash_senhas = PasswordHash.recommended()

def gerar_hash(senha: str) -> str:
    return hash_senhas.hash(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return hash_senhas.verify(senha, senha_hash)

CHAVE_JWT = os.getenv("JWT_SECRET")
ALGORITMO_JWT = "HS256"
TEMPO_EXPIRACAO = 30

def criar_token(dados: dict) -> str:
    conteudo = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO)
    conteudo.update({"exp": expiracao})
    token = jwt.encode(conteudo, CHAVE_JWT, algorithm=ALGORITMO_JWT)
    return token

def verificar_token(token: str) -> dict:
    return jwt.decode(token, CHAVE_JWT, algorithms=[ALGORITMO_JWT])

def obter_usuario_id(token: str) -> int:
    try:
        dados = verificar_token(token)
        return int(dados.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado."
        )