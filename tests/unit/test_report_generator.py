# -*- coding: utf-8 -*-
import pytest
import json
import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nfe_validator.domain.entities.nfe_entity import (
    NFeEntity, NFeItem, Empresa, ImpostoItem, TotaisNFe, ValidationError, Severity
)
from src.nfe_validator.infrastructure.validators.report_generator import ReportGenerator


@pytest.fixture
def sample_nfe_with_errors():
    """NF-e com erros de validação"""
    nfe = NFeEntity(
        chave_acesso="35230100000001000000550010000000011000000011",
        numero="1",
        serie="1",
        data_emissao=datetime(2023, 1, 15),
        emitente=Empresa(cnpj="12345678000190", razao_social="USINA TESTE LTDA", uf="SP"),
        destinatario=Empresa(cnpj="98765432000199", razao_social="COMPRADOR TESTE SA", uf="SP"),
        cfop_nota="5101",
        natureza_operacao="VENDA DE MERCADORIA",
        uf_origem="SP",
        uf_destino="SP",
        items=[
            NFeItem(
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
        ],
        totais=TotaisNFe(
            valor_produtos=Decimal("3500.00"),
            valor_total_nota=Decimal("3500.00"),
            valor_pis=Decimal("57.75"),
            valor_cofins=Decimal("266.00"),
            valor_icms=Decimal("420.00")
        )
    )

    # Adicionar erros de validação
    nfe.validation_errors = [
        ValidationError(
            code="PIS_002",
            field="pis_aliquota",
            message="Alíquota PIS incorreta",
            severity=Severity.CRITICAL,
            actual_value="5.00",
            expected_value="1.65",
            legal_reference="Lei 10.637/2002",
            legal_article="Art. 2º",
            item_numero=1,
            financial_impact=Decimal("117.25"),
            suggestion="Corrigir alíquota para 1.65%",
            can_auto_correct=True,
            corrected_value="1.65"
        ),
        ValidationError(
            code="NCM_003",
            field="descricao",
            message="Descrição pode não corresponder ao NCM",
            severity=Severity.WARNING,
            actual_value="AÇÚCAR CRISTAL",
            expected_value="Açúcar de cana em bruto",
            legal_reference="Tabela NCM/TIPI",
            item_numero=1
        ),
        ValidationError(
            code="TOTAL_001",
            field="valor_produtos",
            message="Valor total divergente",
            severity=Severity.ERROR,
            actual_value="3000.00",
            expected_value="3500.00",
            financial_impact=Decimal("500.00"),
            can_auto_correct=True
        )
    ]

    return nfe


@pytest.fixture
def sample_nfe_sem_erros():
    """NF-e válida sem erros"""
    return NFeEntity(
        chave_acesso="35230100000001000000550010000000021000000022",
        numero="2",
        serie="1",
        data_emissao=datetime(2023, 1, 20),
        emitente=Empresa(cnpj="12345678000190", razao_social="USINA TESTE LTDA", uf="SP"),
        destinatario=Empresa(cnpj="98765432000199", razao_social="COMPRADOR TESTE SA", uf="SP"),
        cfop_nota="5101",
        natureza_operacao="VENDA",
        uf_origem="SP",
        uf_destino="SP",
        items=[
            NFeItem(
                numero_item=1,
                codigo_produto="ACU001",
                descricao="AÇÚCAR CRISTAL",
                ncm="17011100",
                cfop="5101",
                unidade="KG",
                quantidade=Decimal("500"),
                valor_unitario=Decimal("3.50"),
                valor_total=Decimal("1750.00"),
                impostos=ImpostoItem(
                    pis_cst="01",
                    pis_aliquota=Decimal("1.65"),
                    pis_base=Decimal("1750.00"),
                    pis_valor=Decimal("28.88"),
                    cofins_cst="01",
                    cofins_aliquota=Decimal("7.60"),
                    cofins_base=Decimal("1750.00"),
                    cofins_valor=Decimal("133.00"),
                    icms_aliquota=Decimal("12.00"),
                    icms_valor=Decimal("210.00")
                )
            )
        ],
        totais=TotaisNFe(
            valor_produtos=Decimal("1750.00"),
            valor_total_nota=Decimal("1750.00"),
            valor_pis=Decimal("28.88"),
            valor_cofins=Decimal("133.00"),
            valor_icms=Decimal("210.00")
        )
    )


# =====================================================
# Testes de Geração JSON
# =====================================================

def test_generate_json_report_structure(sample_nfe_with_errors):
    """Testar estrutura básica do relatório JSON"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_with_errors)

    # Validar estrutura principal
    assert "metadata" in report
    assert "nfe_info" in report
    assert "validation_summary" in report
    assert "errors" in report
    assert "errors_by_type" in report
    assert "items_analysis" in report
    assert "recommendations" in report
    assert "legal_references" in report


def test_json_report_metadata(sample_nfe_with_errors):
    """Testar metadados do relatório"""
    generator = ReportGenerator(version="2.0.0-test")
    report = generator.generate_json_report(sample_nfe_with_errors)

    assert report["metadata"]["report_version"] == "2.0.0-test"
    assert "generated_at" in report["metadata"]
    assert "validator" in report["metadata"]


def test_json_report_nfe_info(sample_nfe_with_errors):
    """Testar informações da NF-e no relatório"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_with_errors)

    nfe_info = report["nfe_info"]
    assert nfe_info["chave_acesso"] == "35230100000001000000550010000000011000000011"
    assert nfe_info["numero"] == "1"
    assert nfe_info["emitente"]["cnpj"] == "12345678000190"
    assert nfe_info["destinatario"]["razao_social"] == "COMPRADOR TESTE SA"
    assert nfe_info["operacao"]["tipo"] == "INTERNA"


def test_json_report_validation_summary(sample_nfe_with_errors):
    """Testar resumo de validação"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_with_errors)

    summary = report["validation_summary"]
    assert summary["total_errors"] == 3
    assert summary["by_severity"]["critical"] == 1
    assert summary["by_severity"]["error"] == 1
    assert summary["by_severity"]["warning"] == 1
    assert summary["financial_impact"]["total"] > 0


def test_json_report_errors_format(sample_nfe_with_errors):
    """Testar formatação dos erros"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_with_errors)

    errors = report["errors"]
    assert len(errors) == 3

    # Verificar primeiro erro
    first_error = errors[0]
    assert "code" in first_error
    assert "field" in first_error
    assert "message" in first_error
    assert "severity" in first_error
    assert "financial_impact" in first_error


def test_json_report_serialization(sample_nfe_with_errors):
    """Testar se relatório é serializável em JSON"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_with_errors)

    # Deve serializar sem erros
    json_string = json.dumps(report, indent=2)
    assert json_string is not None
    assert len(json_string) > 0

    # Deve poder deserializar
    parsed = json.loads(json_string)
    assert parsed["nfe_info"]["numero"] == "1"


def test_json_report_nfe_sem_erros(sample_nfe_sem_erros):
    """Testar relatório de NF-e sem erros"""
    generator = ReportGenerator()
    report = generator.generate_json_report(sample_nfe_sem_erros)

    summary = report["validation_summary"]
    assert summary["total_errors"] == 0
    assert summary["by_severity"]["critical"] == 0
    assert summary["financial_impact"]["total"] == 0.0


# =====================================================
# Testes de Geração Markdown
# =====================================================

def test_generate_markdown_report(sample_nfe_with_errors):
    """Testar geração de relatório Markdown"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_with_errors)

    assert isinstance(markdown, str)
    assert len(markdown) > 0
    assert "# 📋 RELATÓRIO DE AUDITORIA FISCAL" in markdown


def test_markdown_contains_nfe_info(sample_nfe_with_errors):
    """Testar se Markdown contém informações da NF-e"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_with_errors)

    assert "35230100000001000000550010000000011000000011" in markdown
    assert "USINA TESTE LTDA" in markdown
    assert "COMPRADOR TESTE SA" in markdown


def test_markdown_contains_errors(sample_nfe_with_errors):
    """Testar se Markdown contém erros"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_with_errors)

    assert "PIS_002" in markdown
    assert "Alíquota PIS incorreta" in markdown
    assert "CRÍTICO" in markdown or "CRITICAL" in markdown


def test_markdown_contains_financial_impact(sample_nfe_with_errors):
    """Testar se Markdown mostra impacto financeiro"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_with_errors)

    assert "IMPACTO FINANCEIRO" in markdown or "Impacto" in markdown
    assert "R$" in markdown


def test_markdown_contains_items(sample_nfe_with_errors):
    """Testar se Markdown lista itens"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_with_errors)

    assert "Item 1" in markdown
    assert "AÇÚCAR CRISTAL" in markdown
    assert "17011100" in markdown or "1701.11.00" in markdown


def test_markdown_nfe_sem_erros(sample_nfe_sem_erros):
    """Testar Markdown de NF-e sem erros"""
    generator = ReportGenerator()
    markdown = generator.generate_markdown_report(sample_nfe_sem_erros)

    assert "Total de Problemas Encontrados:** 0" in markdown or "0 problema" in markdown.lower()


# =====================================================
# Testes de Formatação
# =====================================================

def test_format_cnpj():
    """Testar formatação de CNPJ"""
    generator = ReportGenerator()
    formatted = generator._format_cnpj("12345678000190")
    assert formatted == "12.345.678/0001-90"


def test_format_ncm():
    """Testar formatação de NCM"""
    generator = ReportGenerator()
    formatted = generator._format_ncm("17011100")
    assert formatted == "1701.11.00"


def test_extract_legal_references(sample_nfe_with_errors):
    """Testar extração de referências legais"""
    generator = ReportGenerator()
    refs = generator._extract_legal_references(sample_nfe_with_errors.validation_errors)

    assert len(refs) > 0
    assert any("Lei 10.637/2002" in ref["reference"] for ref in refs)


def test_group_errors_by_type(sample_nfe_with_errors):
    """Testar agrupamento de erros por tipo"""
    generator = ReportGenerator()
    grouped = generator._group_errors_by_type(sample_nfe_with_errors.validation_errors)

    assert "PIS" in grouped
    assert "NCM" in grouped
    assert "TOTAL" in grouped


# =====================================================
# Testes de Salvamento de Arquivos
# =====================================================

def test_save_json_report(sample_nfe_with_errors, tmp_path):
    """Testar salvamento de relatório JSON"""
    generator = ReportGenerator()
    output_file = tmp_path / "relatorio.json"

    generator.save_json_report(sample_nfe_with_errors, str(output_file))

    assert output_file.exists()

    # Verificar conteúdo
    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["nfe_info"]["numero"] == "1"


def test_save_markdown_report(sample_nfe_with_errors, tmp_path):
    """Testar salvamento de relatório Markdown"""
    generator = ReportGenerator()
    output_file = tmp_path / "relatorio.md"

    generator.save_markdown_report(sample_nfe_with_errors, str(output_file))

    assert output_file.exists()

    # Verificar conteúdo
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "RELATÓRIO DE AUDITORIA FISCAL" in content
