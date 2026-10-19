from app.metas import repository

def definir_meta(usuario_id: int, quantidade_ml: int):
    if quantidade_ml <= 0:
        raise ValueError("A meta deve ser maior que zero.")

    return repository.definir_meta_do_dia(
        usuario_id=usuario_id,
        quantidade_ml=quantidade_ml,
    )

def consultar_progresso(usuario_id: int):
    meta = repository.buscar_meta_do_dia(usuario_id)

    if not meta:
        return {
            "usuario_id": usuario_id,
            "meta_ml": None,
            "consumido_ml": repository.calcular_consumo_do_dia(usuario_id),
            "restante_ml": None,
            "progresso_percentual": None,
            "mensagem": "Nenhuma meta definida para hoje.",
        }

    consumido_ml = repository.calcular_consumo_do_dia(usuario_id)
    meta_ml = meta["quantidade_ml"]
    restante_ml = max(meta_ml - consumido_ml, 0)
    progresso_percentual = round((consumido_ml / meta_ml) * 100, 2)

    return {
        "usuario_id": usuario_id,
        "meta_ml": meta_ml,
        "consumido_ml": round(consumido_ml, 2),
        "restante_ml": round(restante_ml, 2),
        "progresso_percentual": progresso_percentual,
        "meta_atingida": consumido_ml >= meta_ml,
    }
