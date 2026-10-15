from app.bebidas import service
from fastapi import HTTPException, status

def listar_bebidas():
    return service.listar_bebidas()

def cadastrar_bebida(nome: str, fator_hidratacao: float):
    try:
        bebida_id = service.cadastrar_bebida(
            nome = nome,
            fator_hidratacao = fator_hidratacao,
        )

        return {
            "mensagem": "Bebida cadastrada com sucesso.",
            "id": bebida_id,
        }

    except ValueError as erro:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(erro),
        )
    