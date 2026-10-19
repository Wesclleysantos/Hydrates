from fastapi import HTTPException, status
from app.usuarios import service
from app.auth import criar_token_acesso

def cadastrar_usuario(
        nome: str,
        email: str,
        senha: str,
        peso: float | None = None,
        idade: int | None = None,
):
    try:
        return service.cadastrar_usuario(
            nome = nome,
            email = email,
            senha = senha,
            peso = peso,
            idade = idade,
        )

    except ValueError as error:
        mensagem = str(error)

        if mensagem == "Este e-mail já está cadastrado.":
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = mensagem,
            ) from error

        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = mensagem,
        ) from error

def login_usuario(email: str, senha: str):
    usuario = service.autenticar_usuario(email, senha)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_token_acesso(usuario["id"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "pontos": usuario["pontos"],
        },
    }
