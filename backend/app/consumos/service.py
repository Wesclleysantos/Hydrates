from app.consumos import repository
from app.bebidas import repository as bebidas_repository
from app.conquistas import service as conquistas_service

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
        usuario_id=usuario_id,
        bebida_id=bebida_id,
        quantidade_ml=quantidade_ml,
        hidratacao_ml=hidratacao_ml,
    )

    conquistas_desbloqueadas = []

    try:
        conquistas_desbloqueadas = conquistas_service.verificar_conquistas(
            usuario_id
        )
    except Exception:
        # O consumo já foi salvo; uma falha nas conquistas
        # não deve impedir sua confirmação.
        pass

    return {
        "id": consumo_id,
        "usuario_id": usuario_id,
        "bebida_id": bebida_id,
        "bebida": bebida["nome"],
        "quantidade_ml": quantidade_ml,
        "hidratacao_ml": hidratacao_ml,
        "conquistas_desbloqueadas": conquistas_desbloqueadas,
    }

def listar_consumos(usuario_id: int):
    return repository.listar_consumos(usuario_id)

