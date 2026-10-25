from datetime import date, timedelta
from app.consumos import repository
from app.bebidas import repository as bebidas_repository
from app.conquistas import service as conquistas_service

PERIODO_MAXIMO_RESUMO_DIAS = 366

def registrar_consumo(
    usuario_id: int,
    bebida_id: int,
    quantidade_ml: int,
):
    if quantidade_ml <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    bebida = bebidas_repository.buscar_por_id(
            bebida_id=bebida_id,
            usuario_id=usuario_id,
        )

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

    try:
        conquistas_desbloqueadas = conquistas_service.verificar_conquistas(
            usuario_id
        )
    except Exception:
        # O consumo já foi salvo; falhas nas conquistas não desfazem o registro.
        conquistas_desbloqueadas = []

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

def resumir_consumos(
    usuario_id: int,
    data_inicio: date | None = None,
    data_fim: date | None = None,
):
    return resumir_consumos_diario_por_bebida(
        usuario_id=usuario_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


def resumir_consumos_diario_por_bebida(
    usuario_id: int,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    bebida_id: int | None = None,
):
    if data_inicio is None and data_fim is None:
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=29)
    elif data_inicio is None or data_fim is None:
        raise ValueError("Informe as datas inicial e final juntas.")

    if data_inicio > data_fim:
        raise ValueError("A data inicial deve ser anterior ou igual à final.")

    quantidade_dias = (data_fim - data_inicio).days + 1
    if quantidade_dias > PERIODO_MAXIMO_RESUMO_DIAS:
        raise ValueError("O período do resumo não pode exceder 366 dias.")

    bebida_selecionada = None
    if bebida_id is not None:
        bebida_selecionada = bebidas_repository.buscar_por_id(
            bebida_id=bebida_id,
            usuario_id=usuario_id,
        )
        if not bebida_selecionada:
            raise LookupError("Bebida não encontrada para este usuário.")

    registros = repository.resumir_consumos_diario_por_bebida(
        usuario_id=usuario_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        bebida_id=bebida_id,
    )

    datas = [
        data_inicio + timedelta(days=deslocamento)
        for deslocamento in range(quantidade_dias)
    ]
    dados_por_bebida = {}

    if bebida_selecionada:
        dados_por_bebida[bebida_id] = {
            "bebida_id": bebida_id,
            "bebida": bebida_selecionada["nome"],
            "por_data": {},
        }

    for registro in registros:
        bebida_registro_id = int(registro["bebida_id"])
        if bebida_registro_id not in dados_por_bebida:
            dados_por_bebida[bebida_registro_id] = {
                "bebida_id": bebida_registro_id,
                "bebida": registro["bebida"],
                "por_data": {},
            }

        dados_por_bebida[bebida_registro_id]["por_data"][
            registro["data_consumo"]
        ] = registro

    bebidas = []
    total_quantidade_ml = 0.0
    total_hidratacao_ml = 0.0
    total_registros = 0

    for dados_bebida in dados_por_bebida.values():
        dias = []
        quantidade_total_bebida = 0.0
        hidratacao_total_bebida = 0.0
        registros_total_bebida = 0

        for dia in datas:
            registro = dados_bebida["por_data"].get(dia, {})
            quantidade_ml = float(registro.get("quantidade_ml", 0) or 0)
            hidratacao_ml = float(registro.get("hidratacao_ml", 0) or 0)
            quantidade_registros = int(registro.get("registros", 0) or 0)

            quantidade_total_bebida += quantidade_ml
            hidratacao_total_bebida += hidratacao_ml
            registros_total_bebida += quantidade_registros

            dias.append({
                "data": dia.isoformat(),
                "quantidade_ml": round(quantidade_ml, 2),
                "hidratacao_ml": round(hidratacao_ml, 2),
                "registros": quantidade_registros,
            })

        total_quantidade_ml += quantidade_total_bebida
        total_hidratacao_ml += hidratacao_total_bebida
        total_registros += registros_total_bebida

        bebidas.append({
            "bebida_id": dados_bebida["bebida_id"],
            "bebida": dados_bebida["bebida"],
            "dias": dias,
            "total_quantidade_ml": round(quantidade_total_bebida, 2),
            "total_hidratacao_ml": round(hidratacao_total_bebida, 2),
            "total_registros": registros_total_bebida,
        })

    return {
        "usuario_id": usuario_id,
        "data_inicio": data_inicio.isoformat(),
        "data_fim": data_fim.isoformat(),
        "datas": [dia.isoformat() for dia in datas],
        "bebidas": bebidas,
        "total_quantidade_ml": round(total_quantidade_ml, 2),
        "total_hidratacao_ml": round(total_hidratacao_ml, 2),
        "total_registros": total_registros,
    }