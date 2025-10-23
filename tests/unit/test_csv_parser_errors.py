# -*- coding: utf-8 -*-
import pytest
import sys
import pandas as pd
from pathlib import Path
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nfe_validator.infrastructure.parsers.csv_parser import NFeCSVParser, CSVParserException


@pytest.fixture
def parser():
    """Criar parser"""
    return NFeCSVParser()


# =====================================================
# Testes de Arquivo Inexistente/Inválido
# =====================================================

def test_parse_arquivo_inexistente(parser):
    """Testar parsing de arquivo inexistente"""
    with pytest.raises(Exception):
        parser.parse_csv("arquivo_inexistente_12345.csv")


def test_parse_arquivo_vazio(parser, tmp_path):
    """Testar parsing de arquivo vazio"""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    with pytest.raises((CSVParserException, pd.errors.EmptyDataError, Exception)):
        parser.parse_csv(str(empty_file))


def test_parse_arquivo_sem_header(parser, tmp_path):
    """Testar parsing de arquivo sem cabeçalho"""
    no_header = tmp_path / "no_header.csv"
    no_header.write_text("123,456,789\n111,222,333", encoding="utf-8")

    with pytest.raises((CSVParserException, Exception)):
        parser.parse_csv(str(no_header))


# =====================================================
# Testes de Colunas Faltando
# =====================================================

def test_parse_colunas_minimas_faltando(parser, tmp_path):
    """Testar CSV com colunas mínimas faltando"""
    csv_content = """chave_acesso,numero_nfe
35230100000001000000550010000000011000000011,1
"""
    csv_file = tmp_path / "missing_columns.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(CSVParserException) as exc_info:
        parser.parse_csv(str(csv_file))

    assert "Colunas MÍNIMAS ausentes" in str(exc_info.value)


def test_parse_sem_chave_acesso(parser, tmp_path):
    """Testar CSV sem coluna chave_acesso"""
    csv_content = """numero_nfe,data_emissao,cnpj_emitente
1,2023-01-01,12345678000190
"""
    csv_file = tmp_path / "no_chave.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(CSVParserException):
        parser.parse_csv(str(csv_file))


# =====================================================
# Testes de Dados Malformados
# =====================================================

def test_parse_chave_acesso_invalida(parser, tmp_path):
    """Testar chave de acesso com formato inválido"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
ABC,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,17011100,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "invalid_chave.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # Parser deve processar mas validação posterior detectará erro
    nfes = parser.parse_csv(str(csv_file))
    assert len(nfes) > 0
    # Chave inválida deve ser preservada
    assert nfes[0].chave_acesso == "ABC"


def test_parse_data_invalida(parser, tmp_path):
    """Testar data com formato inválido"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,DATA_INVALIDA,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,17011100,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "invalid_date.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises((CSVParserException, Exception)):
        parser.parse_csv(str(csv_file))


def test_parse_valores_numericos_invalidos(parser, tmp_path):
    """Testar valores numéricos com formato inválido"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,17011100,5101,UN,ABC,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "invalid_numbers.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises((CSVParserException, ValueError, Exception)):
        parser.parse_csv(str(csv_file))


# =====================================================
# Testes de Valores Nulos/Vazios
# =====================================================

def test_parse_campos_obrigatorios_vazios(parser, tmp_path):
    """Testar campos obrigatórios com valores vazios"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,17011100,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "empty_required.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises((CSVParserException, Exception)):
        parser.parse_csv(str(csv_file))


def test_parse_ncm_vazio(parser, tmp_path):
    """Testar NCM vazio"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "empty_ncm.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # Parser deve processar mas item terá NCM vazio
    nfes = parser.parse_csv(str(csv_file))
    assert len(nfes) > 0
    # Validação posterior detectará NCM vazio/inválido


def test_parse_cst_vazio(parser, tmp_path):
    """Testar CST vazio"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO,17011100,5101,UN,1,10.00,10.00,,1.65,10.00,0.17,,7.60,10.00,0.76
"""
    csv_file = tmp_path / "empty_cst.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # Parser deve processar
    nfes = parser.parse_csv(str(csv_file))
    assert len(nfes) > 0
    # CST vazio será normalizado (pode ser "" ou "na" dependendo do keep_default_na)
    pis_cst = nfes[0].items[0].impostos.pis_cst
    assert pis_cst in ["", "na", "nan"]


# =====================================================
# Testes de Normalização
# =====================================================

def test_normalize_ncm_4_digitos(parser):
    """Testar normalização de NCM com 4 dígitos"""
    normalized = parser._normalize_ncm("1701")
    assert normalized == "17010000"
    assert len(normalized) == 8


def test_normalize_ncm_6_digitos(parser):
    """Testar normalização de NCM com 6 dígitos"""
    normalized = parser._normalize_ncm("170111")
    assert normalized == "17011100"
    assert len(normalized) == 8


def test_normalize_ncm_8_digitos(parser):
    """Testar normalização de NCM com 8 dígitos"""
    normalized = parser._normalize_ncm("17011100")
    assert normalized == "17011100"


def test_normalize_cst_1_digito(parser):
    """Testar normalização de CST com 1 dígito"""
    normalized = parser._normalize_cst("1")
    assert normalized == "01"


def test_normalize_cst_2_digitos(parser):
    """Testar normalização de CST com 2 dígitos"""
    normalized = parser._normalize_cst("01")
    assert normalized == "01"


def test_normalize_cfop_valido(parser):
    """Testar normalização de CFOP válido"""
    normalized = parser._normalize_cfop("5101")
    assert normalized == "5101"


# =====================================================
# Testes de Múltiplas NF-es
# =====================================================

def test_parse_multiplas_nfes(parser, tmp_path):
    """Testar parsing de múltiplas NF-es"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO1,17011100,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
35230100000001000000550010000000021000000022,2,1,2023-01-02,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P002,PRODUTO2,17019900,5101,UN,2,20.00,40.00,01,1.65,40.00,0.66,01,7.60,40.00,3.04
"""
    csv_file = tmp_path / "multiplas_nfes.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    nfes = parser.parse_csv(str(csv_file))

    assert len(nfes) == 2
    assert nfes[0].numero == "1"
    assert nfes[1].numero == "2"


def test_parse_nfe_com_multiplos_itens(parser, tmp_path):
    """Testar parsing de NF-e com múltiplos itens"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,1,P001,PRODUTO1,17011100,5101,UN,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,TESTE,SP,98765432000199,COMPRADOR,SP,5101,VENDA,2,P002,PRODUTO2,17019900,5101,UN,2,20.00,40.00,01,1.65,40.00,0.66,01,7.60,40.00,3.04
"""
    csv_file = tmp_path / "multiplos_itens.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    nfes = parser.parse_csv(str(csv_file))

    assert len(nfes) == 1
    assert len(nfes[0].items) == 2
    assert nfes[0].items[0].numero_item == 1
    assert nfes[0].items[1].numero_item == 2


# =====================================================
# Testes de Encoding
# =====================================================

def test_parse_caracteres_especiais(parser, tmp_path):
    """Testar parsing com caracteres especiais (acentos)"""
    csv_content = """chave_acesso,numero_nfe,serie,data_emissao,cnpj_emitente,razao_social_emitente,uf_emitente,cnpj_destinatario,razao_social_destinatario,uf_destinatario,cfop_nota,natureza_operacao,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,pis_cst,pis_aliquota,pis_base,pis_valor,cofins_cst,cofins_aliquota,cofins_base,cofins_valor
35230100000001000000550010000000011000000011,1,1,2023-01-01,12345678000190,USINA AÇÚCAR,SP,98765432000199,DISTRIBUIDORA CAFÉ,SP,5101,VENDA,1,P001,AÇÚCAR REFINADO,17011100,5101,KG,1,10.00,10.00,01,1.65,10.00,0.17,01,7.60,10.00,0.76
"""
    csv_file = tmp_path / "acentos.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    nfes = parser.parse_csv(str(csv_file))

    assert len(nfes) == 1
    assert "AÇÚCAR" in nfes[0].emitente.razao_social
    assert "AÇÚCAR" in nfes[0].items[0].descricao
