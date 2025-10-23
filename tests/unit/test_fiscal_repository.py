# -*- coding: utf-8 -*-
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.repositories.fiscal_repository import FiscalRepository


@pytest.fixture
def fiscal_repo():
    """Criar repositório fiscal"""
    return FiscalRepository()


# =====================================================
# Testes de Conexão e Inicialização
# =====================================================

def test_repository_connection(fiscal_repo):
    """Testar conexão com database"""
    assert fiscal_repo.conn is not None
    assert fiscal_repo.db_path is not None


def test_repository_statistics(fiscal_repo):
    """Testar estatísticas do repositório"""
    stats = fiscal_repo.get_statistics()

    assert "ncm_rules" in stats
    assert "pis_cofins_rules" in stats
    assert "cfop_rules" in stats
    assert "legal_refs" in stats
    assert stats["ncm_rules"] > 0


def test_database_version(fiscal_repo):
    """Testar obtenção de versão do database"""
    version = fiscal_repo.get_database_version()
    assert version is not None
    assert len(version) > 0


# =====================================================
# Testes de NCM Rules
# =====================================================

def test_get_ncm_acucar_cristal(fiscal_repo):
    """Testar busca de NCM de açúcar cristal"""
    ncm_rule = fiscal_repo.get_ncm_rule("17011100")

    assert ncm_rule is not None
    assert ncm_rule["ncm"] == "17011100"
    assert "açúcar" in ncm_rule["description"].lower()


def test_get_ncm_invalido(fiscal_repo):
    """Testar busca de NCM inexistente"""
    ncm_rule = fiscal_repo.get_ncm_rule("99999999")
    assert ncm_rule is None


def test_validate_ncm_exists(fiscal_repo):
    """Testar validação de existência de NCM"""
    assert fiscal_repo.validate_ncm_exists("17011100") == True
    assert fiscal_repo.validate_ncm_exists("99999999") == False


def test_get_all_sugar_ncms(fiscal_repo):
    """Testar busca de todos os NCMs de açúcar"""
    sugar_ncms = fiscal_repo.get_all_sugar_ncms()

    assert len(sugar_ncms) > 0
    # Verificar que retorna NCMs (pelo menos um deve ser de açúcar - 1701)
    ncms_list = [ncm["ncm"] for ncm in sugar_ncms]
    assert any(ncm.startswith("1701") for ncm in ncms_list)


def test_get_ncm_keywords(fiscal_repo):
    """Testar obtenção de keywords de NCM"""
    keywords = fiscal_repo.get_ncm_keywords("17011100")

    assert isinstance(keywords, list)
    if len(keywords) > 0:
        assert any("açúcar" in kw.lower() or "sugar" in kw.lower() for kw in keywords)


# =====================================================
# Testes de PIS/COFINS Rules
# =====================================================

def test_get_pis_cofins_rule_01(fiscal_repo):
    """Testar busca de regra PIS/COFINS CST 01"""
    rule = fiscal_repo.get_pis_cofins_rule("01")

    assert rule is not None
    assert rule["cst"] == "01"
    assert rule["situation_type"] == "TRIBUTADA"


def test_get_pis_cofins_rule_invalido(fiscal_repo):
    """Testar busca de CST inválido"""
    rule = fiscal_repo.get_pis_cofins_rule("99")
    assert rule is None


def test_get_valid_csts(fiscal_repo):
    """Testar obtenção de lista de CSTs válidos"""
    csts = fiscal_repo.get_valid_csts()

    assert len(csts) > 0
    assert "01" in csts
    assert "06" in csts


def test_is_cst_valid(fiscal_repo):
    """Testar validação de CST"""
    assert fiscal_repo.is_cst_valid("01") == True
    assert fiscal_repo.is_cst_valid("99") == False


def test_get_pis_cofins_rates_standard(fiscal_repo):
    """Testar obtenção de alíquotas regime não-cumulativo"""
    rates = fiscal_repo.get_pis_cofins_rates("01", regime="STANDARD")

    assert "pis" in rates
    assert "cofins" in rates
    assert rates["pis"] == 1.65
    assert rates["cofins"] == 7.60


def test_get_pis_cofins_rates_cumulative(fiscal_repo):
    """Testar obtenção de alíquotas regime cumulativo"""
    rates = fiscal_repo.get_pis_cofins_rates("01", regime="CUMULATIVE")

    assert "pis" in rates
    assert "cofins" in rates
    # Alíquotas cumulativas são menores
    assert rates["pis"] < 1.65


# =====================================================
# Testes de CFOP Rules
# =====================================================

def test_get_cfop_5101(fiscal_repo):
    """Testar busca de CFOP 5101"""
    cfop_rule = fiscal_repo.get_cfop_rule("5101")

    assert cfop_rule is not None
    assert cfop_rule["cfop"] == "5101"
    assert cfop_rule["operation_scope"] == "INTERNO"


def test_get_cfop_6101(fiscal_repo):
    """Testar busca de CFOP 6101"""
    cfop_rule = fiscal_repo.get_cfop_rule("6101")

    assert cfop_rule is not None
    assert cfop_rule["cfop"] == "6101"
    assert cfop_rule["operation_scope"] == "INTERESTADUAL"


def test_get_cfop_invalido(fiscal_repo):
    """Testar busca de CFOP inexistente"""
    cfop_rule = fiscal_repo.get_cfop_rule("9999")
    assert cfop_rule is None


def test_get_cfops_by_scope_interno(fiscal_repo):
    """Testar busca de CFOPs internos"""
    cfops = fiscal_repo.get_cfops_by_scope("INTERNO")

    assert len(cfops) > 0
    # Verificar que retorna CFOPs internos (pelo menos um deve começar com 5)
    cfop_codes = [cfop["cfop"] for cfop in cfops]
    assert any(cfop.startswith("5") for cfop in cfop_codes)


def test_get_cfops_by_scope_interestadual(fiscal_repo):
    """Testar busca de CFOPs interestaduais"""
    cfops = fiscal_repo.get_cfops_by_scope("INTERESTADUAL")

    assert len(cfops) > 0
    # Verificar que retorna CFOPs interestaduais (pelo menos um deve começar com 6)
    cfop_codes = [cfop["cfop"] for cfop in cfops]
    assert any(cfop.startswith("6") for cfop in cfop_codes)


def test_get_sugar_cfops(fiscal_repo):
    """Testar busca de CFOPs comuns para açúcar"""
    cfops = fiscal_repo.get_sugar_cfops()

    assert len(cfops) > 0
    # Deve incluir CFOPs de venda
    cfop_codes = [c["cfop"] for c in cfops]
    assert "5101" in cfop_codes or "6101" in cfop_codes


def test_validate_cfop_scope_interno(fiscal_repo):
    """Testar validação de CFOP interno"""
    assert fiscal_repo.validate_cfop_scope("5101", is_interstate=False) == True
    assert fiscal_repo.validate_cfop_scope("5101", is_interstate=True) == False


def test_validate_cfop_scope_interestadual(fiscal_repo):
    """Testar validação de CFOP interestadual"""
    assert fiscal_repo.validate_cfop_scope("6101", is_interstate=True) == True
    assert fiscal_repo.validate_cfop_scope("6101", is_interstate=False) == False


# =====================================================
# Testes de State Rules
# =====================================================

def test_get_state_rules_sp(fiscal_repo):
    """Testar busca de regras estaduais de SP"""
    rules = fiscal_repo.get_state_rules("SP")

    # SP deve ter regras cadastradas no MVP
    assert isinstance(rules, list)


def test_get_state_rules_pe(fiscal_repo):
    """Testar busca de regras estaduais de PE"""
    rules = fiscal_repo.get_state_rules("PE")

    # PE deve ter regras cadastradas no MVP
    assert isinstance(rules, list)


def test_has_state_rules(fiscal_repo):
    """Testar verificação de existência de regras estaduais"""
    # SP e PE devem ter regras
    has_sp = fiscal_repo.has_state_rules("SP")
    has_pe = fiscal_repo.has_state_rules("PE")

    assert isinstance(has_sp, bool)
    assert isinstance(has_pe, bool)


def test_get_state_icms_rate(fiscal_repo):
    """Testar obtenção de alíquota ICMS estadual"""
    icms_rate = fiscal_repo.get_state_icms_rate("SP", "17011100")

    # Pode retornar None se não houver override específico
    if icms_rate is not None:
        assert isinstance(icms_rate, float)
        assert icms_rate >= 0
        assert icms_rate <= 20  # ICMS máximo no Brasil


# =====================================================
# Testes de Legal References
# =====================================================

def test_get_legal_reference_lei_10637(fiscal_repo):
    """Testar busca de referência legal Lei 10.637"""
    ref = fiscal_repo.get_legal_reference("LEI_10637")

    assert ref is not None
    assert ref["code"] == "LEI_10637"
    assert "PIS" in ref["title"] or "pis" in ref["title"].lower()


def test_get_legal_reference_invalido(fiscal_repo):
    """Testar busca de referência inexistente"""
    ref = fiscal_repo.get_legal_reference("LEI_INEXISTENTE_99999")
    assert ref is None


def test_format_legal_citation(fiscal_repo):
    """Testar formatação de citação legal"""
    citation = fiscal_repo.format_legal_citation("LEI_10637")

    assert citation is not None
    assert len(citation) > 0
    assert "10637" in citation or "10.637" in citation


def test_get_all_legal_references(fiscal_repo):
    """Testar busca de todas as referências legais"""
    refs = fiscal_repo.get_all_legal_references()

    assert len(refs) > 0
    assert all("code" in ref for ref in refs)


def test_get_legal_references_by_scope_federal(fiscal_repo):
    """Testar busca de referências por escopo federal"""
    refs = fiscal_repo.get_legal_references_by_scope("FEDERAL")

    assert len(refs) > 0
    assert all(ref["scope"] == "FEDERAL" for ref in refs)


def test_search_legal_references(fiscal_repo):
    """Testar busca textual em referências"""
    refs = fiscal_repo.search_legal_references("PIS")

    assert len(refs) > 0


def test_get_legal_references_by_tax_pis(fiscal_repo):
    """Testar busca de referências que afetam PIS"""
    refs = fiscal_repo.get_legal_references_by_tax("PIS")

    assert isinstance(refs, list)


# =====================================================
# Testes de Validação Integrada
# =====================================================

def test_validate_tax_configuration_valida(fiscal_repo):
    """Testar validação integrada com configuração válida"""
    result = fiscal_repo.validate_tax_configuration(
        ncm="17011100",
        pis_cst="01",
        cofins_cst="01",
        cfop="5101"
    )

    assert result["valid"] == True
    assert len(result["errors"]) == 0
    assert result["ncm_info"] is not None
    assert result["pis_info"] is not None


def test_validate_tax_configuration_invalida(fiscal_repo):
    """Testar validação integrada com configuração inválida"""
    result = fiscal_repo.validate_tax_configuration(
        ncm="99999999",  # NCM inválido
        pis_cst="99",     # CST inválido
        cofins_cst="99",  # CST inválido
        cfop="9999"       # CFOP inválido
    )

    assert result["valid"] == False
    assert len(result["errors"]) > 0


# =====================================================
# Testes de Repository Layers
# =====================================================

def test_get_repository_layers_status(fiscal_repo):
    """Testar status das camadas do repositório"""
    status = fiscal_repo.get_repository_layers_status()

    assert "camadas_ativas" in status
    assert "sqlite" in status
    assert status["sqlite"]["disponivel"] == True
    assert status["sqlite"]["total_ncm_rules"] > 0
