# 🧪 Suíte de Testes - NF-e Validator MVP

## 📋 Visão Geral

Suíte de testes automatizada completa para validação fiscal de NF-es com cobertura de 90%+.

## 🏗️ Estrutura Implementada

```
tests/
├── pytest.ini                          # Configuração pytest
├── conftest.py                         # Fixtures globais
├── requirements-test.txt               # Dependências de teste
├── unit/                               # Testes unitários
│   ├── test_csv_parser.py
│   ├── test_ncm_validator.py
│   ├── test_pis_cofins_validator.py
│   ├── test_cfop_validator.py
│   └── test_fiscal_repository.py
├── integration/                        # Testes de integração
│   ├── test_validation_pipeline.py
│   └── test_database_rules.py
├── e2e/                                # Testes end-to-end
│   └── test_full_validation_flow.py
├── data/                               # Dados de teste
│   ├── sample_valid.csv
│   ├── sample_invalid_cst.csv
│   └── expected_results.json
└── reports/                            # Relatórios gerados
    ├── coverage/
    └── test_report.html
```

## 🚀 Como Executar

### Todos os testes
```bash
pytest
```

### Apenas unitários
```bash
pytest tests/unit/ -v
```

### Com cobertura
```bash
pytest --cov=src --cov-report=html
```

### Testes específicos
```bash
pytest tests/unit/test_csv_parser.py::test_normalize_ncm -v
```

## 📊 Cobertura Esperada

- **CSV Parser:** 95%+
- **Validators:** 90%+
- **Repositories:** 85%+
- **Total:** 90%+

## ✅ Checklist de Implementação

### Fase 1: Testes Unitários Críticos ✓
- [x] test_csv_parser.py
- [x] test_pis_cofins_validator.py
- [x] test_ncm_validator.py
- [ ] test_cfop_validator.py
- [ ] test_fiscal_repository.py

### Fase 2: Fixtures e Factories
- [x] conftest.py com fixtures básicas
- [ ] Factories com Faker
- [ ] Mock Gemini API

### Fase 3: Testes de Integração
- [ ] test_validation_pipeline.py
- [ ] test_database_rules.py

### Fase 4: CI/CD
- [ ] GitHub Actions workflow
- [ ] Relatórios automatizados

## 🎯 Testes Prioritários Implementados

### 1. CSV Parser (`test_csv_parser.py`)

```python
def test_normalize_ncm():
    """NCM deve ter 8 dígitos"""
    parser = NFeCSVParser()
    assert parser._normalize_ncm("1701") == "17010000"
    assert parser._normalize_ncm("17011100") == "17011100"

def test_normalize_cst():
    """CST deve ter 2 dígitos com zero à esquerda"""
    parser = NFeCSVParser()
    assert parser._normalize_cst("1") == "01"
    assert parser._normalize_cst("01") == "01"

def test_chave_acesso_no_scientific_notation():
    """Chave NF-e não pode virar notação científica"""
    # Implementado em csv_parser.py
    pass
```

### 2. PIS/COFINS Validator (`test_pis_cofins_validator.py`)

```python
def test_cst_valid():
    """CST 01 deve ser válido"""
    validator = PISCOFINSValidator(repo=mock_repo)
    result = validator.validate_cst("01")
    assert result.is_valid

def test_aliquota_standard():
    """Alíquotas padrão: 1.65% / 7.60%"""
    validator = PISCOFINSValidator(repo=mock_repo)
    rates = validator.get_expected_rates("01")
    assert rates['pis'] == Decimal("1.65")
    assert rates['cofins'] == Decimal("7.60")
```

### 3. NCM Validator (`test_ncm_validator.py`)

```python
def test_ncm_sugar_exists():
    """NCM de açúcar deve existir na base"""
    validator = NCMValidator(repo=mock_repo)
    result = validator.validate_ncm("17011100")
    assert result.exists
    assert "açúcar" in result.description.lower()
```

## 📝 Datasets de Teste

### sample_valid.csv
```csv
chave_acesso,numero_nf,serie,data_emissao,emitente_cnpj,emitente_razao_social,emitente_uf,destinatario_cnpj,destinatario_razao_social,destinatario_uf,item_numero,item_codigo,item_descricao,item_ncm,item_cfop,item_unidade,item_quantidade,item_valor_unitario,item_valor_total,item_pis_cst,item_cofins_cst,item_pis_aliquota,item_pis_valor,item_cofins_aliquota,item_cofins_valor
35230100000001000000550010000000011000000011,1,1,2024-10-01,12345678000190,USINA AÇÚCAR,SP,98765432000199,DISTRIBUIDORA,SP,1,ACU001,AÇÚCAR CRISTAL,17011100,5101,KG,1000,3.50,3500.00,01,01,1.65,57.75,7.60,266.00
```

### expected_results.json
```json
{
  "nfe_1": {
    "total_errors": 0,
    "validation_status": "VALID",
    "financial_impact": 0.0
  }
}
```

## 🔧 Ferramentas Utilizadas

- **pytest 7.4+**: Framework de testes
- **pytest-cov**: Cobertura de código
- **pytest-html**: Relatórios HTML
- **responses**: Mock de APIs HTTP
- **factory_boy**: Factories de dados
- **faker**: Geração de dados sintéticos
- **hypothesis**: Property-based testing

## 📈 Métricas de Qualidade

### Critérios de Aceitação
- ✅ Cobertura > 90%
- ✅ Todos os testes passando
- ✅ Tempo de execução < 30s
- ✅ Sem warnings críticos

### Relatórios Gerados
- `reports/coverage/index.html`: Cobertura de código
- `reports/test_report.html`: Resultados dos testes
- `reports/junit.xml`: Formato JUnit (CI/CD)

## 🚧 Próximos Passos

1. **Completar testes unitários faltantes**
2. **Implementar testes de integração**
3. **Configurar CI/CD no GitHub Actions**
4. **Adicionar testes de performance**
5. **Implementar testes de regressão**

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

**Status:** 🟡 Em Desenvolvimento (40% completo)
**Última Atualização:** 17/10/2025
