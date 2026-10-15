from app.consumos import repository
from app.bebidas import repository as bebidas_repository


def registrar_consumo(
    usuario_id: int,
    bebida_id: int,
    quantidade_ml: int,
):
    if quantidade_ml <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    bebida = bebidas_repository.buscar_por_id(bebida_id)

    if not bebida:
        raise ValueError("Bebida não encontrada.")

    if not bebida["activo"]:
        raise ValueError("Esta bebida está inativa.")

    fator = float(bebida["fator_hidratacao"])
    hidratacao_ml = round(quantidade_ml * fator, 2)

    consumo_id = repository.criar_consumo(
        usuario_id = usuario_id,
        bebida_id = bebida_id,
        quantidade_ml = quantidade_ml,
        hidratacao_ml = hidratacao_ml,
    )

    return {
        "id": consumo_id,
        "usuario_id": usuario_id,
        "bebida_id": bebida_id,
        "bebida": bebida["nome"],
        "quantidade_ml": quantidade_ml,
        "hidratacao_ml": hidratacao_ml,
    }


def listar_consumos(usuario_id: int):
    return repository.listar_consumos(usuario_id)

