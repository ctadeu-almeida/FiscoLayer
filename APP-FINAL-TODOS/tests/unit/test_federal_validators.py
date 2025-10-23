# -*- coding: utf-8 -*-
import pytest
import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nfe_validator.domain.entities.nfe_entity import (
    NFeEntity, NFeItem, Empresa, ImpostoItem, TotaisNFe, Severity
)
from src.nfe_validator.domain.services.federal_validators import (
    NCMValidator, PISCOFINSValidator, CFOPValidator, TotalsValidator
)
from src.repositories.fiscal_repository import FiscalRepository


@pytest.fixture
def fiscal_repo():
    """Criar repositório fiscal para testes"""
    return FiscalRepository()


@pytest.fixture
def sample_nfe_interna():
    """NF-e de operação interna (SP → SP)"""
    return NFeEntity(
        chave_acesso="35230100000001000000550010000000011000000011",
        numero="1",
        serie="1",
        data_emissao=datetime(2023, 1, 1),
        emitente=Empresa(cnpj="12345678000190", razao_social="USINA TESTE", uf="SP"),
        destinatario=Empresa(cnpj="98765432000199", razao_social="COMPRADOR TESTE", uf="SP"),
        cfop_nota="5101",
        natureza_operacao="VENDA",
        uf_origem="SP",
        uf_destino="SP",
        items=[],
        totais=TotaisNFe(
            valor_produtos=Decimal("1000.00"),
            valor_total_nota=Decimal("1000.00"),
            valor_pis=Decimal("16.50"),
            valor_cofins=Decimal("76.00"),
            valor_icms=Decimal("120.00")
        )
    )


@pytest.fixture
def sample_nfe_interestadual():
    """NF-e de operação interestadual (SP → PE)"""
    return NFeEntity(
        chave_acesso="35230100000001000000550010000000021000000022",
        numero="2",
        serie="1",
        data_emissao=datetime(2023, 1, 1),
        emitente=Empresa(cnpj="12345678000190", razao_social="USINA TESTE", uf="SP"),
        destinatario=Empresa(cnpj="98765432000199", razao_social="COMPRADOR TESTE", uf="PE"),
        cfop_nota="6101",
        natureza_operacao="VENDA",
        uf_origem="SP",
        uf_destino="PE",
        items=[],
        totais=TotaisNFe(
            valor_produtos=Decimal("1000.00"),
            valor_total_nota=Decimal("1000.00"),
            valor_pis=Decimal("16.50"),
            valor_cofins=Decimal("76.00"),
            valor_icms=Decimal("70.00")
        )
    )


@pytest.fixture
def item_acucar_valido():
    """Item de açúcar com dados válidos"""
    return NFeItem(
        numero_item=1,
        codigo_produto="ACU001",
        descricao="AÇÚCAR CRISTAL",
        ncm="17011100",
        cfop="5101",
        unidade="KG",
        quantidade=Decimal("1000"),
        valor_unitario=Decimal("3.50"),
        valor_total=Decimal("3500.00"),
        impostos=ImpostoItem(
            pis_cst="01",
            pis_aliquota=Decimal("1.65"),
            pis_base=Decimal("3500.00"),
            pis_valor=Decimal("57.75"),
            cofins_cst="01",
            cofins_aliquota=Decimal("7.60"),
            cofins_base=Decimal("3500.00"),
            cofins_valor=Decimal("266.00"),
            icms_aliquota=Decimal("12.00"),
            icms_valor=Decimal("420.00")
        )
    )


# =====================================================
# Testes de NCMValidator
# =====================================================

def test_ncm_validator_formato_invalido(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar NCM com formato inválido"""
    validator = NCMValidator(fiscal_repo)
    item_acucar_valido.ncm = "1701"  # Apenas 4 dígitos

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    assert len(errors) == 1
    assert errors[0].code == "NCM_001"
    assert errors[0].severity == Severity.CRITICAL


def test_ncm_validator_acucar_valido(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar NCM de açúcar válido"""
    validator = NCMValidator(fiscal_repo)

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve ter 0 erros ou apenas warnings
    critical_errors = [e for e in errors if e.severity == Severity.CRITICAL]
    assert len(critical_errors) == 0


def test_ncm_validator_produto_nao_acucar(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar NCM que não é açúcar"""
    validator = NCMValidator(fiscal_repo)
    item_acucar_valido.ncm = "12345678"  # NCM não-açúcar

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve ter erro indicando que não é açúcar
    assert len(errors) > 0
    assert any(e.code == "NCM_002" for e in errors)


# =====================================================
# Testes de PISCOFINSValidator
# =====================================================

def test_pis_cst_invalido(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CST PIS inválido"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.pis_cst = "99"  # CST inválido

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    assert len(errors) > 0
    assert any(e.code == "PIS_001" for e in errors)


def test_cofins_cst_invalido(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CST COFINS inválido"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.cofins_cst = "99"  # CST inválido

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    assert len(errors) > 0
    assert any(e.code == "COFINS_001" for e in errors)


def test_pis_aliquota_incorreta(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar alíquota PIS incorreta"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.pis_aliquota = Decimal("5.00")  # Alíquota errada

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve detectar alíquota incorreta
    pis_errors = [e for e in errors if e.code == "PIS_002"]
    assert len(pis_errors) > 0
    assert pis_errors[0].severity == Severity.CRITICAL


def test_cofins_aliquota_incorreta(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar alíquota COFINS incorreta"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.cofins_aliquota = Decimal("10.00")  # Alíquota errada

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve detectar alíquota incorreta
    cofins_errors = [e for e in errors if e.code == "COFINS_002"]
    assert len(cofins_errors) > 0
    assert cofins_errors[0].severity == Severity.CRITICAL


def test_pis_valor_incorreto(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar valor PIS calculado incorretamente"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.pis_valor = Decimal("100.00")  # Valor errado

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve detectar cálculo incorreto
    calc_errors = [e for e in errors if e.code == "PIS_003"]
    assert len(calc_errors) > 0
    assert calc_errors[0].financial_impact > 0


def test_pis_cofins_cst_divergentes(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CST PIS e COFINS divergentes"""
    validator = PISCOFINSValidator(fiscal_repo)
    item_acucar_valido.impostos.pis_cst = "01"
    item_acucar_valido.impostos.cofins_cst = "06"  # Divergente

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve gerar warning sobre divergência
    divergence_errors = [e for e in errors if e.code == "PISCOFINS_001"]
    assert len(divergence_errors) > 0
    assert divergence_errors[0].severity == Severity.WARNING


# =====================================================
# Testes de CFOPValidator
# =====================================================

def test_cfop_formato_invalido(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CFOP com formato inválido"""
    validator = CFOPValidator(fiscal_repo)
    item_acucar_valido.cfop = "510"  # Apenas 3 dígitos

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    assert len(errors) > 0
    assert errors[0].code == "CFOP_001"
    assert errors[0].severity == Severity.CRITICAL


def test_cfop_interno_correto(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CFOP interno correto"""
    validator = CFOPValidator(fiscal_repo)
    item_acucar_valido.cfop = "5101"

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Não deve ter erros críticos de CFOP
    cfop_critical = [e for e in errors if e.code.startswith("CFOP") and e.severity == Severity.CRITICAL]
    assert len(cfop_critical) == 0


def test_cfop_interno_em_operacao_interestadual(fiscal_repo, item_acucar_valido, sample_nfe_interestadual):
    """Testar CFOP interno em operação interestadual (erro)"""
    validator = CFOPValidator(fiscal_repo)
    item_acucar_valido.cfop = "5101"  # CFOP interno em operação interestadual

    errors = validator.validate(item_acucar_valido, sample_nfe_interestadual)

    # Deve detectar inconsistência
    cfop_errors = [e for e in errors if e.code == "CFOP_003"]
    assert len(cfop_errors) > 0
    assert cfop_errors[0].severity == Severity.CRITICAL


def test_cfop_interestadual_em_operacao_interna(fiscal_repo, item_acucar_valido, sample_nfe_interna):
    """Testar CFOP interestadual em operação interna (erro)"""
    validator = CFOPValidator(fiscal_repo)
    item_acucar_valido.cfop = "6101"  # CFOP interestadual em operação interna

    errors = validator.validate(item_acucar_valido, sample_nfe_interna)

    # Deve detectar inconsistência
    cfop_errors = [e for e in errors if e.code == "CFOP_004"]
    assert len(cfop_errors) > 0
    assert cfop_errors[0].severity == Severity.CRITICAL


# =====================================================
# Testes de TotalsValidator
# =====================================================

def test_totals_valor_produtos_correto(fiscal_repo, sample_nfe_interna, item_acucar_valido):
    """Testar valor total dos produtos correto"""
    validator = TotalsValidator(fiscal_repo)
    sample_nfe_interna.items = [item_acucar_valido]
    sample_nfe_interna.totais.valor_produtos = Decimal("3500.00")

    errors = validator.validate(sample_nfe_interna)

    # Não deve ter erro de total de produtos
    total_errors = [e for e in errors if e.code == "TOTAL_001"]
    assert len(total_errors) == 0


def test_totals_valor_produtos_divergente(fiscal_repo, sample_nfe_interna, item_acucar_valido):
    """Testar valor total dos produtos divergente"""
    validator = TotalsValidator(fiscal_repo)
    sample_nfe_interna.items = [item_acucar_valido]
    sample_nfe_interna.totais.valor_produtos = Decimal("1000.00")  # Incorreto

    errors = validator.validate(sample_nfe_interna)

    # Deve detectar divergência
    total_errors = [e for e in errors if e.code == "TOTAL_001"]
    assert len(total_errors) > 0
    assert total_errors[0].severity == Severity.CRITICAL
    assert total_errors[0].financial_impact > 0


def test_totals_pis_divergente(fiscal_repo, sample_nfe_interna, item_acucar_valido):
    """Testar total PIS divergente"""
    validator = TotalsValidator(fiscal_repo)
    sample_nfe_interna.items = [item_acucar_valido]
    sample_nfe_interna.totais.valor_pis = Decimal("100.00")  # Incorreto

    errors = validator.validate(sample_nfe_interna)

    # Deve detectar divergência
    pis_errors = [e for e in errors if e.code == "TOTAL_003"]
    assert len(pis_errors) > 0
    assert pis_errors[0].severity == Severity.ERROR


def test_totals_cofins_divergente(fiscal_repo, sample_nfe_interna, item_acucar_valido):
    """Testar total COFINS divergente"""
    validator = TotalsValidator(fiscal_repo)
    sample_nfe_interna.items = [item_acucar_valido]
    sample_nfe_interna.totais.valor_cofins = Decimal("500.00")  # Incorreto

    errors = validator.validate(sample_nfe_interna)

    # Deve detectar divergência
    cofins_errors = [e for e in errors if e.code == "TOTAL_004"]
    assert len(cofins_errors) > 0
    assert cofins_errors[0].severity == Severity.ERROR
