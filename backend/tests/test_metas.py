from datetime import date as date_real
from unittest.mock import patch
from app.metas import service

class HojeFixa(date_real):
    @classmethod
    def today(cls):
        return cls(2026, 10, 19)

def test_sequencia_conta_dias_anteriores_quando_hoje_nao_foi_atingido():
    dias = [
        {"data_meta": date_real(2026, 10, 18)},
        {"data_meta": date_real(2026, 10, 17)},
    ]
    with (
        patch("app.metas.service.repository.listar_dias_com_meta_atingida", return_value=dias),
        patch("app.metas.service.date", HojeFixa),
    ):
        resultado = service.verificar_sequencia(7)

    assert resultado["sequencia_atual"] == 2
    assert resultado["meta_3_dias"] is False
    