import pytest
from src.nfe_validator.infrastructure.parsers.csv_parser import NFeCSVParser

def test_normalize_ncm():
    parser = NFeCSVParser()
    assert parser._normalize_ncm("1701") == "17010000"
    assert parser._normalize_ncm("17011100") == "17011100"

def test_normalize_cst():
    parser = NFeCSVParser()
    assert parser._normalize_cst("1") == "01"
    assert parser._normalize_cst("01") == "01"

def test_normalize_cfop():
    parser = NFeCSVParser()
    assert parser._normalize_cfop("5101") == "5101"
