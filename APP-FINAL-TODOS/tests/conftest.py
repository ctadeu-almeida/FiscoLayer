# -*- coding: utf-8 -*-
import pytest
import sys
from pathlib import Path
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nfe_validator.domain.entities.nfe_entity import (
    NFeEntity, NFeItem, Empresa, ImpostoItem, TotaisNFe, ValidationStatus
)

@pytest.fixture
def sample_empresa_emitente():
    return Empresa(
        cnpj="12345678000190",
        razao_social="USINA AÇÚCAR MODELO LTDA",
        uf="SP"
    )

@pytest.fixture
def sample_empresa_destinatario():
    return Empresa(
        cnpj="98765432000199",
        razao_social="DISTRIBUIDORA ALIMENTOS SA",
        uf="SP"
    )

@pytest.fixture
def sample_imposto_item():
    return ImpostoItem(
        pis_cst="01",
        pis_aliquota=Decimal("1.65"),
        pis_valor=Decimal("57.75"),
        cofins_cst="01",
        cofins_aliquota=Decimal("7.60"),
        cofins_valor=Decimal("266.00"),
        icms_aliquota=Decimal("12.00"),
        icms_valor=Decimal("420.00")
    )

@pytest.fixture
def sample_nfe_item(sample_imposto_item):
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
        impostos=sample_imposto_item
    )
