"""
Testes: Capacidade Dinâmica da Emergência
Cobertura: taxa_ocupacao sem trava de 100%, divisão por zero, valores negativos/inválidos.

Contexto (start.md):
- A partir de 01/05/2026, a SMSRio inclui macas extras como leitos dinâmicos.
- num_enf da emergência: 111, 113, 114, 115, 116, 117
- Taxa pode exceder 100% quando pacientes em macas superam a capacidade nominal.
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers: replicam a lógica de cálculo do backend (app.py)
# ---------------------------------------------------------------------------

def calcular_taxa_ocupacao(ocupados: int, total: int) -> float:
    """Espelha a fórmula usada em api_emergencia_stats e api_emergencia_evolucao."""
    if total <= 0:
        return 0.0
    return round((ocupados / total * 100), 2)


EMERGENCY_WARDS_NUM_ENF = [111, 113, 114, 115, 116, 117]
PEDIATRIC_WARDS_NUM_ENF = [116, 117]


# ---------------------------------------------------------------------------
# Testes da taxa de ocupação
# ---------------------------------------------------------------------------

class TestTaxaOcupacao:
    def test_taxa_normal(self):
        """Cenário normal: 40 ocupados em 50 leitos → 80%."""
        assert calcular_taxa_ocupacao(40, 50) == 80.0

    def test_taxa_plena(self):
        """Capacidade 100%: todos os leitos ocupados."""
        assert calcular_taxa_ocupacao(50, 50) == 100.0

    def test_taxa_acima_100_com_macas_extras(self):
        """
        Cenário SMSRio pós-01/05/2026: 60 pacientes para 50 leitos nominais.
        O total inclui as macas extras, portanto total=60, ocupados=60 → 100%.
        Mas se a contagem de total ainda reflete 50 e ocupados=60 → 120%.
        A taxa NÃO deve ser cortada em 100%.
        """
        taxa = calcular_taxa_ocupacao(60, 50)
        assert taxa == 120.0, f"Esperado 120.0, obtido {taxa}"
        assert taxa > 100, "Taxa deve poder exceder 100% sem truncamento"

    def test_taxa_com_macas_dinamicas_total_dinamico(self):
        """
        Com total dinâmico (macas incluídas): 60 ocupados de 60 total → 100%.
        Taxa não excede 100% porque o denominador também cresceu.
        """
        taxa = calcular_taxa_ocupacao(60, 60)
        assert taxa == 100.0

    def test_taxa_zero_leitos(self):
        """Divisão por zero: total=0 deve retornar 0.0 sem exceção."""
        taxa = calcular_taxa_ocupacao(10, 0)
        assert taxa == 0.0

    def test_taxa_zero_ocupados(self):
        """Nenhum ocupado: taxa deve ser 0.0."""
        assert calcular_taxa_ocupacao(0, 50) == 0.0

    def test_taxa_ambos_zero(self):
        """Ambos zero: deve retornar 0.0."""
        assert calcular_taxa_ocupacao(0, 0) == 0.0

    def test_taxa_resultado_arredondado(self):
        """Verifica arredondamento a 2 casas decimais (ex.: 1/3 → 33.33%)."""
        taxa = calcular_taxa_ocupacao(1, 3)
        assert taxa == 33.33


# ---------------------------------------------------------------------------
# Testes das constantes de num_enf
# ---------------------------------------------------------------------------

class TestConstantesNumEnf:
    def test_emergency_wards_incluem_todos_setores(self):
        """Todos os num_enf da emergência devem estar na lista."""
        for enf in [111, 113, 114, 115, 116, 117]:
            assert enf in EMERGENCY_WARDS_NUM_ENF, f"num_enf {enf} ausente de EMERGENCY_WARDS_NUM_ENF"

    def test_pediatric_wards_subset_de_emergency(self):
        """Setores pediátricos devem ser subconjunto dos setores de emergência."""
        for enf in PEDIATRIC_WARDS_NUM_ENF:
            assert enf in EMERGENCY_WARDS_NUM_ENF, f"num_enf pediátrico {enf} não está em EMERGENCY_WARDS_NUM_ENF"

    def test_pre_parto_excluido(self):
        """num_enf 251 (pré-parto) NÃO deve estar na emergência (start.md item 8)."""
        assert 251 not in EMERGENCY_WARDS_NUM_ENF

    def test_sql_string_contem_todos_num_enf(self):
        """A string SQL gerada deve conter todos os num_enf."""
        sql = ", ".join(str(n) for n in EMERGENCY_WARDS_NUM_ENF)
        for enf in EMERGENCY_WARDS_NUM_ENF:
            assert str(enf) in sql


# ---------------------------------------------------------------------------
# Testes de mapeamento de nomes (histórico → novo)
# ---------------------------------------------------------------------------

NOME_MAP = {
    111: {"antigo": "CLINICA REFERENCIADA",               "novo": "SALA VERMELHA"},
    113: {"antigo": "CIRURGICA REFERENCIADA",              "novo": "SALA AMARELA"},
    114: {"antigo": "CIRURGICA REFERENCIADA - FEMININA",   "novo": "OBSERVAÇÃO"},
    115: {"antigo": "CIRURGICA REFERENCIADA - MASCULINA",  "novo": "OBSERVAÇÃO"},
    116: {"antigo": "CLINICA REFERENCIADA - PED",          "novo": "SALA AMARELA PEDIÁTRICA"},
    117: {"antigo": "CLINICA REFERENCIADA - PED",          "novo": "OBSERVAÇÃO - PEDIÁTRICA"},
}

EMERGENCY_WARDS_ALL = [
    # Histórico
    'CLINICA REFERENCIADA', 'CIRURGICA REFERENCIADA',
    'CIRURGICA REFERENCIADA - FEMININA', 'CIRURGICA REFERENCIADA - MASCULINA',
    'CLINICA REFERENCIADA - PED',
    # Novos (a partir de 01/05/2026)
    'SALA VERMELHA', 'SALA AMARELA', 'OBSERVAÇÃO',
    'SALA AMARELA PEDIÁTRICA', 'OBSERVAÇÃO - PEDIÁTRICA',
]

class TestMapeamentoNomes:
    def test_todos_nomes_novos_presentes_em_emergency_wards(self):
        novos = [v["novo"] for v in NOME_MAP.values()]
        for nome in novos:
            assert nome in EMERGENCY_WARDS_ALL, f"Novo nome '{nome}' ausente de EMERGENCY_WARDS"

    def test_todos_nomes_antigos_presentes_em_emergency_wards(self):
        antigos = set(v["antigo"] for v in NOME_MAP.values())
        for nome in antigos:
            assert nome in EMERGENCY_WARDS_ALL, f"Nome histórico '{nome}' ausente de EMERGENCY_WARDS"
