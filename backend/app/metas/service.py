from app.metas import repository
from datetime import date, timedelta

ML_POR_KG_PARA_META_ESTIMADA = 35
IDADE_MINIMA_META_AUTOMATICA = 18

def definir_meta(usuario_id: int, quantidade_ml: int):
    if quantidade_ml <= 0:
        raise ValueError("A meta deve ser maior que zero.")

    return repository.definir_meta_do_dia(
        usuario_id=usuario_id,
        quantidade_ml=quantidade_ml,
    )

def calcular_meta_automatica(usuario_id: int):
    usuario = repository.buscar_dados_usuario(usuario_id)

    if not usuario:
        raise ValueError("Usuário não encontrado.")

    idade = usuario["idade"]
    peso = usuario["peso"]

    if idade is None or idade < IDADE_MINIMA_META_AUTOMATICA:
        raise ValueError(
            "O cálculo automático está disponível apenas para adultos. "
            "Defina a meta manualmente."
        )

    if peso is None or float(peso) <= 0:
        raise ValueError(
            "Cadastre um peso válido para calcular a meta automaticamente."
        )

    quantidade_ml = round(float(peso) * ML_POR_KG_PARA_META_ESTIMADA)
    meta = repository.definir_meta_do_dia(usuario_id, quantidade_ml)

    return {
        **meta,
        "calculada_automaticamente": True,
        "criterio": f"estimativa geral de {ML_POR_KG_PARA_META_ESTIMADA} ml por kg de peso para adultos",
        "aviso": "Estimativa geral; necessidades individuais podem variar. Você pode ajustar a meta manualmente.",
    }

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

def verificar_sequencia(usuario_id: int) -> dict:
    dias_atingidos = repository.listar_dias_com_meta_atingida(
        usuario_id
    )

    datas = {
        dia["data_meta"]
        for dia in dias_atingidos
    }

    hoje = date.today()
    inicio = 0 if hoje in datas else 1
    sequencia = 0

    for i in range(inicio, inicio + 7):
        dia_verificado = hoje - timedelta(days=i)

        if dia_verificado in datas:
            sequencia += 1
        else:
            break

    return {
        "sequencia_atual": sequencia,
        "meta_3_dias": sequencia >= 3,
        "meta_7_dias": sequencia >= 7,
    }
