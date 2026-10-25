from app.bebidas import service
from fastapi import HTTPException, status

def listar_bebidas(usuario_id: int):
    return service.listar_bebidas(usuario_id=usuario_id)

def cadastrar_bebida(
    usuario_id: int,
    nome: str,
    fator_hidratacao: float,
):
    bebida_id = service.cadastrar_bebida(
        usuario_id=usuario_id,
        nome=nome,
        fator_hidratacao=fator_hidratacao,
    )

    return {
        "mensagem": "Bebida cadastrada com sucesso.",
        "id": bebida_id,
    }

def atualizar_bebida(
    usuario_id: int,
    bebida_id: int,
    nome: str,
    fator_hidratacao: float,
):
    service.atualizar_bebida(
        usuario_id=usuario_id,
        bebida_id=bebida_id,
        nome=nome,
        fator_hidratacao=fator_hidratacao,
    )

    return {
        "mensagem": "Bebida atualizada com sucesso.",
        "id": bebida_id,
    }