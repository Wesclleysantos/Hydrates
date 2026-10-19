from app.conquistas import repository
from app.consumos import repository as consumos_repository
from app.metas import service as metas_service

def listar_conquistas_ativas():
    return repository.listar_conquistas_ativas()

def listar_conquistas_usuario(usuario_id: int):
    return repository.listar_conquistas_usuario(
        usuario_id=usuario_id,
    )

def obter_criterios_cumpridos(usuario_id: int) -> set:
    criterios = set()

    if consumos_repository.usuario_tem_consumo(usuario_id):
        criterios.add("primeiro_consumo")

    progresso = metas_service.consultar_progresso(usuario_id)

    if progresso.get("meta_atingida", False):
        criterios.add("meta_atingida")

    sequencia = metas_service.verificar_sequencia(usuario_id)

    if sequencia["meta_3_dias"]:
        criterios.add("sequencia_3_dias")

    if sequencia["meta_7_dias"]:
        criterios.add("sequencia_7_dias")

    return criterios

def desbloquear_conquista(usuario_id: int, conquista_id: int):
    conquistas = repository.listar_conquistas_ativas()

    conquista = next(
        (
            item for item in conquistas
            if item["id"] == conquista_id
        ),
        None,
    )

    if not conquista:
        raise ValueError("Conquista não encontrada ou inativa.")

    criterios = obter_criterios_cumpridos(usuario_id)

    if conquista["criterio"] not in criterios:
        raise ValueError(
            "Você ainda não cumpriu os requisitos desta conquista."
        )

    return repository.desbloquear_conquista(
        usuario_id=usuario_id,
        conquista_id=conquista_id,
    )

def verificar_conquistas(usuario_id: int):
    conquistas = repository.listar_conquistas_ativas()
    criterios = obter_criterios_cumpridos(usuario_id)
    desbloqueadas = []

    for conquista in conquistas:
        if conquista["criterio"] not in criterios:
            continue

        resultado = repository.desbloquear_conquista(
            usuario_id=usuario_id,
            conquista_id=conquista["id"],
        )

        if resultado is not None:
            desbloqueadas.append({
                "id": conquista["id"],
                "nome": conquista["nome"],
                "descricao": conquista["descricao"],
                "pontos": conquista["pontos"],
                "criterio": conquista["criterio"],
            })

    return desbloqueadas
