import pytest
import sys
from pathlib import Path
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.nfe_validator.infrastructure.parsers.csv_parser import NFeCSVParser

def test_nfe_1_valida():
    """NF-e 1 deve ser válida sem erros"""
    csv_path = Path(__file__).parent.parent.parent / "test_data" / "nfe_teste_controlado.csv"
    
    if not csv_path.exists():
        pytest.skip("Arquivo não encontrado")
    
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_path))
    
    assert len(nfes) > 0
    nfe = nfes[0]
    
    # Chave sem notação científica
    assert "e+" not in nfe.chave_acesso.lower()
    assert nfe.chave_acesso == "35230100000001000000550010000000011000000011"
    
    # CST normalizado
    assert nfe.items[0].impostos.pis_cst == "01"
    assert nfe.items[0].impostos.cofins_cst == "01"

def test_aliquotas_corretas():
    """Alíquotas PIS/COFINS corretas"""
    csv_path = Path(__file__).parent.parent.parent / "test_data" / "nfe_teste_controlado.csv"
    
    if not csv_path.exists():
        pytest.skip("Arquivo não encontrado")
    
    parser = NFeCSVParser()
    nfes = parser.parse_csv(str(csv_path))
    item = nfes[0].items[0]
    
    assert item.impostos.pis_aliquota == Decimal("1.65")
    assert item.impostos.cofins_aliquota == Decimal("7.60")
