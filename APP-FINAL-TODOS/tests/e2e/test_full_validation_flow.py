# -*- coding: utf-8 -*-
"""
Testes E2E - Fluxo Completo de Validação
CSV → Parser → Validators → Report
"""
import pytest
import sys
from pathlib import Path
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nfe_validator.infrastructure.parsers.csv_parser import NFeCSVParser
from src.nfe_validator.domain.services.federal_validators import (
    NCMValidator, PISCOFINSValidator, CFOPValidator, TotalsValidator
)
from src.nfe_validator.infrastructure.validators.report_generator import ReportGenerator
from src.repositories.fiscal_repository import FiscalRepository


@pytest.fixture
def test_data_path():
    """Caminho para arquivos de teste"""
    return Path(__file__).parent.parent.parent / "test_data"


@pytest.fixture
def fiscal_repo():
    """Repositório fiscal"""
    return FiscalRepository()


# =====================================================
# Teste E2E Completo - NF-e Válida
# =====================================================

def test_e2e_nfe_valida_completa(test_data_path, fiscal_repo):
    """Testar fluxo completo com NF-e válida"""
    csv_path = test_data_path / "nfe_teste_controlado.csv"

    if not csv_path.exists():
        pytest.skip("Arquivo de teste não encontrado")

    # 1. Parse CSV
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_path))

    assert len(nfes) > 0
    nfe = nfes[0]

    # 2. Validar com validators
    ncm_validator = NCMValidator(fiscal_repo)
    pis_cofins_validator = PISCOFINSValidator(fiscal_repo)
    cfop_validator = CFOPValidator(fiscal_repo)
    totals_validator = TotalsValidator(fiscal_repo)

    # Validar cada item
    for item in nfe.items:
        nfe.validation_errors.extend(ncm_validator.validate(item, nfe))
        nfe.validation_errors.extend(pis_cofins_validator.validate(item, nfe))
        nfe.validation_errors.extend(cfop_validator.validate(item, nfe))

    # Validar totais
    nfe.validation_errors.extend(totals_validator.validate(nfe))

    # 3. Gerar relatórios
    report_gen = ReportGenerator()
    json_report = report_gen.generate_json_report(nfe)
    md_report = report_gen.generate_markdown_report(nfe)

    # 4. Verificações
    assert json_report is not None
    assert "nfe_info" in json_report
    assert "validation_summary" in json_report

    assert md_report is not None
    assert len(md_report) > 0
    assert "RELATÓRIO DE AUDITORIA FISCAL" in md_report


# =====================================================
# Teste E2E - NF-e com Erros Diversos
# =====================================================

def test_e2e_nfe_com_erros_pis_cofins(test_data_path, fiscal_repo, tmp_path):
    """Testar fluxo completo com NF-e contendo erros de PIS/COFINS"""
    # Criar CSV de teste com erro de alíquota
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor,total_produtos,total_nfe,total_pis,total_cofins,total_icms
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,3.50,3500.00,01,5.00,3500.00,175.00,01,10.00,3500.00,350.00,3500.00,3500.00,175.00,350.00,420.00
"""
    csv_file = tmp_path / "nfe_erro_aliquota.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))
    nfe = nfes[0]

    # 2. Validar
    pis_cofins_validator = PISCOFINSValidator(fiscal_repo)

    for item in nfe.items:
        nfe.validation_errors.extend(pis_cofins_validator.validate(item, nfe))

    # 3. Verificar que erros foram detectados
    assert len(nfe.validation_errors) > 0

    # Deve ter erro de alíquota PIS
    pis_errors = [e for e in nfe.validation_errors if e.code == "PIS_002"]
    assert len(pis_errors) > 0

    # Deve ter erro de alíquota COFINS
    cofins_errors = [e for e in nfe.validation_errors if e.code == "COFINS_002"]
    assert len(cofins_errors) > 0

    # 4. Gerar relatório
    report_gen = ReportGenerator()
    json_report = report_gen.generate_json_report(nfe)

    assert json_report["validation_summary"]["total_errors"] > 0
    assert json_report["validation_summary"]["by_severity"]["critical"] > 0


def test_e2e_nfe_com_erro_cfop(test_data_path, fiscal_repo, tmp_path):
    """Testar fluxo completo com NF-e contendo erro de CFOP"""
    # CFOP interno em operação interestadual
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor,total_produtos,total_nfe,total_pis,total_cofins,total_icms
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,PE,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,3.50,3500.00,01,1.65,3500.00,57.75,01,7.60,3500.00,266.00,3500.00,3500.00,57.75,266.00,245.00
"""
    csv_file = tmp_path / "nfe_erro_cfop.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))
    nfe = nfes[0]

    # 2. Validar
    cfop_validator = CFOPValidator(fiscal_repo)

    for item in nfe.items:
        nfe.validation_errors.extend(cfop_validator.validate(item, nfe))

    # 3. Verificar erro de CFOP
    cfop_errors = [e for e in nfe.validation_errors if e.code in ["CFOP_003", "CFOP_004"]]
    assert len(cfop_errors) > 0


def test_e2e_nfe_com_erro_totais(test_data_path, fiscal_repo, tmp_path):
    """Testar fluxo completo com NF-e contendo erro de totais"""
    # Criar NF-e com múltiplos itens mas total divergente
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,3.50,3500.00,01,1.65,3500.00,57.75,01,7.60,3500.00,266.00
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,2,ACU002,AÇÚCAR REFINADO,17019900,5101,KG,500,4.00,2000.00,01,1.65,2000.00,33.00,01,7.60,2000.00,152.00
"""
    csv_file = tmp_path / "nfe_erro_totais.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))
    nfe = nfes[0]

    # 2. Modificar manualmente os totais para criar divergência
    nfe.totais.valor_produtos = Decimal("1000.00")  # Deveria ser 5500
    nfe.totais.valor_pis = Decimal("10.00")  # Deveria ser 90.75
    nfe.totais.valor_cofins = Decimal("20.00")  # Deveria ser 418.00

    # 3. Validar
    totals_validator = TotalsValidator(fiscal_repo)
    nfe.validation_errors.extend(totals_validator.validate(nfe))

    # 4. Verificar erros de totais
    assert len(nfe.validation_errors) > 0

    total_errors = [e for e in nfe.validation_errors if e.code.startswith("TOTAL")]
    assert len(total_errors) >= 3  # Produtos, PIS e COFINS divergentes


# =====================================================
# Teste E2E - Múltiplas NF-es
# =====================================================

def test_e2e_multiplas_nfes(test_data_path, fiscal_repo, tmp_path):
    """Testar processamento de múltiplas NF-es"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor,total_produtos,total_nfe,total_pis,total_cofins,total_icms
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,3.50,3500.00,01,1.65,3500.00,57.75,01,7.60,3500.00,266.00,3500.00,3500.00,57.75,266.00,420.00
35230100000001000000550010000000021000000022,2,1,2023-01-02,12345678000190,USINA TESTE,SP,11111111000111,OUTRO COMPRADOR,PE,6101,VENDA,1,ACU002,AÇÚCAR REFINADO,17019900,6101,KG,500,4.00,2000.00,01,1.65,2000.00,33.00,01,7.60,2000.00,152.00,2000.00,2000.00,33.00,152.00,140.00
"""
    csv_file = tmp_path / "multiplas_nfes.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))

    assert len(nfes) == 2

    # 2. Validar todas
    all_validators = [
        NCMValidator(fiscal_repo),
        PISCOFINSValidator(fiscal_repo),
        CFOPValidator(fiscal_repo),
        TotalsValidator(fiscal_repo)
    ]

    for nfe in nfes:
        for item in nfe.items:
            for validator in all_validators[:-1]:  # Exceto TotalsValidator
                nfe.validation_errors.extend(validator.validate(item, nfe))

        # Totals validator
        nfe.validation_errors.extend(all_validators[-1].validate(nfe))

    # 3. Gerar relatórios para cada uma
    report_gen = ReportGenerator()

    for i, nfe in enumerate(nfes, 1):
        json_report = report_gen.generate_json_report(nfe)
        assert json_report["nfe_info"]["numero"] == str(i)


# =====================================================
# Teste E2E - Impacto Financeiro
# =====================================================

def test_e2e_calculo_impacto_financeiro(fiscal_repo, tmp_path):
    """Testar cálculo de impacto financeiro em erros"""
    # NF-e com alíquotas erradas
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor,total_produtos,total_nfe,total_pis,total_cofins,total_icms
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,10.00,10000.00,01,5.00,10000.00,500.00,01,10.00,10000.00,1000.00,10000.00,10000.00,500.00,1000.00,1200.00
"""
    csv_file = tmp_path / "nfe_impacto_financeiro.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse e validar
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))
    nfe = nfes[0]

    pis_cofins_validator = PISCOFINSValidator(fiscal_repo)

    for item in nfe.items:
        nfe.validation_errors.extend(pis_cofins_validator.validate(item, nfe))

    # 2. Calcular impacto total
    total_impact = sum(
        e.financial_impact for e in nfe.validation_errors
        if e.financial_impact
    )

    assert total_impact > 0

    # 3. Verificar no relatório
    report_gen = ReportGenerator()
    json_report = report_gen.generate_json_report(nfe)

    assert json_report["validation_summary"]["financial_impact"]["total"] > 0


# =====================================================
# Teste E2E - Salvamento de Relatórios
# =====================================================

def test_e2e_salvamento_relatorios(fiscal_repo, tmp_path):
    """Testar salvamento de relatórios em arquivos"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor,total_produtos,total_nfe,total_pis,total_cofins,total_icms
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA TESTE,SP,98765432000199,COMPRADOR TESTE,SP,5101,VENDA,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,100,3.50,350.00,01,1.65,350.00,5.78,01,7.60,350.00,26.60,350.00,350.00,5.78,26.60,42.00
"""
    csv_file = tmp_path / "nfe_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # 1. Parse e validar
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_file))
    nfe = nfes[0]

    # Validações básicas
    ncm_validator = NCMValidator(fiscal_repo)
    for item in nfe.items:
        nfe.validation_errors.extend(ncm_validator.validate(item, nfe))

    # 2. Salvar relatórios
    report_gen = ReportGenerator()

    json_path = tmp_path / "relatorio.json"
    md_path = tmp_path / "relatorio.md"

    report_gen.save_json_report(nfe, str(json_path))
    report_gen.save_markdown_report(nfe, str(md_path))

    # 3. Verificar arquivos
    assert json_path.exists()
    assert md_path.exists()

    assert json_path.stat().st_size > 0
    assert md_path.stat().st_size > 0
