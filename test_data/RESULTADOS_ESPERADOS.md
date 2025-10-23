# Resultados Esperados - Teste Controlado NF-e Validator

## 📋 Visão Geral do Teste

**Arquivo:** `nfe_teste_controlado.csv`
**Total de Notas:** 20 NF-e fictícias
**Período:** 01/10/2024 a 20/10/2024
**Emitente:** USINA AÇÚCAR MODELO LTDA (CNPJ: 12.345.678/0001-90) - SP
**Destinatário:** DISTRIBUIDORA ALIMENTOS SA (CNPJ: 98.765.432/0001-99)

---

## ✅ Grupo 1: Notas CORRETAS (NF-e 1 a 5)

### NF-e 1 - ✅ VÁLIDA
- **Chave:** 35230100000001...
- **Item:** Açúcar Cristal (NCM 17011100)
- **CFOP:** 5101 (Venda SP→SP)
- **Tributos:**
  - ICMS: R$ 420,00 (12% sobre R$ 3.500,00) ✅
  - PIS: R$ 57,75 (1,65% sobre R$ 3.500,00) ✅
  - COFINS: R$ 266,00 (7,60% sobre R$ 3.500,00) ✅
- **Status:** APROVADO ✅

### NF-e 2 - ✅ VÁLIDA
- **Chave:** 35230100000002...
- **Item:** Açúcar Refinado (NCM 17019900)
- **CFOP:** 6101 (Venda SP→PE - Interestadual)
- **Tributos:**
  - ICMS: R$ 240,00 (12% sobre R$ 2.000,00) ✅
  - PIS: R$ 33,00 (1,65% sobre R$ 2.000,00) ✅
  - COFINS: R$ 152,00 (7,60% sobre R$ 2.000,00) ✅
- **Status:** APROVADO ✅

### NF-e 3 - ✅ VÁLIDA
- **Chave:** 35230100000003...
- **Item:** Açúcar Demerara (NCM 17019900)
- **CFOP:** 5101 (Venda SP→SP)
- **Tributos:**
  - ICMS: R$ 480,00 (12% sobre R$ 4.000,00) ✅
  - PIS: R$ 66,00 (1,65% sobre R$ 4.000,00) ✅
  - COFINS: R$ 304,00 (7,60% sobre R$ 4.000,00) ✅
- **Status:** APROVADO ✅

### NF-e 4 - ✅ VÁLIDA
- **Chave:** 35230100000004...
- **Item:** Açúcar Cristal (NCM 17011100)
- **CFOP:** 6101 (Venda SP→MG - Interestadual)
- **Tributos:**
  - ICMS: R$ 504,00 (12% sobre R$ 4.200,00) ✅
  - PIS: R$ 69,30 (1,65% sobre R$ 4.200,00) ✅
  - COFINS: R$ 319,20 (7,60% sobre R$ 4.200,00) ✅
- **Status:** APROVADO ✅

### NF-e 5 - ✅ VÁLIDA
- **Chave:** 35230100000005...
- **Item:** Açúcar Refinado (NCM 17019900)
- **CFOP:** 5101 (Venda SP→SP)
- **Tributos:**
  - ICMS: R$ 288,00 (12% sobre R$ 2.400,00) ✅
  - PIS: R$ 39,60 (1,65% sobre R$ 2.400,00) ✅
  - COFINS: R$ 182,40 (7,60% sobre R$ 2.400,00) ✅
- **Status:** APROVADO ✅

---

## ⚠️ Grupo 2: Notas com DADOS FALTANTES (NF-e 6 a 10)

### NF-e 6 - ⚠️ DADOS INCOMPLETOS
- **Chave:** 35230100000006...
- **Problema:** Campos ICMS ausentes
  - ❌ `item_icms_base` = vazio
  - ❌ `item_icms_aliquota` = vazio
  - ❌ `item_icms_valor` = vazio
- **Mensagens Esperadas:**
  - ⚠️ "ICMS Base de Cálculo não informada"
  - ⚠️ "ICMS Alíquota não informada"
  - ⚠️ "ICMS Valor não informado"
- **Status:** VALIDAÇÃO PARCIAL ⚠️

### NF-e 7 - ⚠️ DADOS INCOMPLETOS
- **Chave:** 35230100000007...
- **Problema:** ICMS valor ausente
  - ❌ `item_icms_valor` = vazio
- **Mensagens Esperadas:**
  - ⚠️ "ICMS Valor não informado"
  - 💡 "Valor esperado: R$ 240,00 (12% sobre R$ 2.000,00)"
- **Status:** VALIDAÇÃO PARCIAL ⚠️

### NF-e 8 - ⚠️ DADOS INCOMPLETOS
- **Chave:** 35230100000008...
- **Problema:** PIS/COFINS base ausentes
  - ❌ `item_pis_base` = vazio
  - ❌ `item_pis_aliquota` = vazio
  - ❌ `item_cofins_base` = vazio
  - ❌ `item_cofins_aliquota` = vazio
- **Mensagens Esperadas:**
  - ⚠️ "PIS: Base de cálculo não informada"
  - ⚠️ "COFINS: Base de cálculo não informada"
- **Status:** VALIDAÇÃO PARCIAL ⚠️

### NF-e 9 - ⚠️ DADOS INCOMPLETOS
- **Chave:** 35230100000009...
- **Problema:** NCM e CFOP ausentes
  - ❌ `item_ncm` = vazio
  - ❌ `item_cfop` = vazio
- **Mensagens Esperadas:**
  - 🚨 "NCM não informado - impossível validar tributação"
  - 🚨 "CFOP não informado - impossível validar natureza da operação"
- **Status:** VALIDAÇÃO IMPOSSÍVEL 🚨

### NF-e 10 - ⚠️ DADOS INCOMPLETOS
- **Chave:** 35230100000010...
- **Problema:** Alíquotas PIS/COFINS ausentes
  - ❌ `item_pis_aliquota` = vazio
  - ❌ `item_cofins_aliquota` = vazio
- **Mensagens Esperadas:**
  - ⚠️ "PIS: Alíquota não informada"
  - ⚠️ "COFINS: Alíquota não informada"
  - 💡 "Alíquotas esperadas: PIS 1,65% / COFINS 7,60%"
- **Status:** VALIDAÇÃO PARCIAL ⚠️

---

## 🔴 Grupo 3: Notas com IMPOSTOS PAGOS A MAIS (NF-e 11 a 15)

### NF-e 11 - 🔴 IMPOSTO PAGO A MAIS
- **Chave:** 35230100000011...
- **Problema:** Valores tributários acima do esperado
- **Comparação:**

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 600,00 | R$ 420,00 | **+R$ 180,00** 🔴 |
| PIS | R$ 100,00 | R$ 57,75 | **+R$ 42,25** 🔴 |
| COFINS | R$ 400,00 | R$ 266,00 | **+R$ 134,00** 🔴 |

- **Total pago a mais:** R$ 356,25
- **Status:** PREJUÍZO FISCAL 🔴
- **Ação Recomendada:** Solicitar retificação da NF-e

### NF-e 12 - 🔴 IMPOSTO PAGO A MAIS
- **Chave:** 35230100000012...
- **Problema:** ICMS com alíquota incorreta (18% em vez de 12%)

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 360,00 | R$ 240,00 | **+R$ 120,00** 🔴 |
| PIS | R$ 50,00 | R$ 33,00 | **+R$ 17,00** 🔴 |
| COFINS | R$ 200,00 | R$ 152,00 | **+R$ 48,00** 🔴 |

- **Total pago a mais:** R$ 185,00
- **Status:** PREJUÍZO FISCAL 🔴

### NF-e 13 - 🔴 IMPOSTO PAGO A MAIS
- **Chave:** 35230100000013...
- **Problema:** PIS/COFINS com alíquotas superiores

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| PIS | R$ 80,00 | R$ 66,00 | **+R$ 14,00** 🔴 |
| COFINS | R$ 360,00 | R$ 304,00 | **+R$ 56,00** 🔴 |

- **Total pago a mais:** R$ 70,00
- **Status:** PREJUÍZO FISCAL 🔴

### NF-e 14 - 🔴 IMPOSTO PAGO A MAIS
- **Chave:** 35230100000014...
- **Problema:** Múltiplos tributos acima do esperado

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 630,00 | R$ 504,00 | **+R$ 126,00** 🔴 |
| PIS | R$ 84,00 | R$ 69,30 | **+R$ 14,70** 🔴 |
| COFINS | R$ 399,00 | R$ 319,20 | **+R$ 79,80** 🔴 |

- **Total pago a mais:** R$ 220,50
- **Status:** PREJUÍZO FISCAL 🔴

### NF-e 15 - 🔴 IMPOSTO PAGO A MAIS
- **Chave:** 35230100000015...
- **Problema:** ICMS com alíquota incorreta e PIS/COFINS elevados

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 432,00 | R$ 288,00 | **+R$ 144,00** 🔴 |
| PIS | R$ 45,00 | R$ 39,60 | **+R$ 5,40** 🔴 |
| COFINS | R$ 200,00 | R$ 182,40 | **+R$ 17,60** 🔴 |

- **Total pago a mais:** R$ 167,00
- **Status:** PREJUÍZO FISCAL 🔴

---

## 🟡 Grupo 4: Notas com IMPOSTOS PAGOS A MENOS (NF-e 16 a 20)

### NF-e 16 - 🟡 IMPOSTO PAGO A MENOS
- **Chave:** 35230100000016...
- **Problema:** Valores tributários abaixo do esperado

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 350,00 | R$ 420,00 | **-R$ 70,00** 🟡 |
| PIS | R$ 40,00 | R$ 57,75 | **-R$ 17,75** 🟡 |
| COFINS | R$ 180,00 | R$ 266,00 | **-R$ 86,00** 🟡 |

- **Total pago a menos:** R$ 173,75
- **Status:** RISCO FISCAL 🟡
- **Ação Recomendada:** Emitir NF-e complementar

### NF-e 17 - 🟡 IMPOSTO PAGO A MENOS
- **Chave:** 35230100000017...
- **Problema:** Todos os tributos subfaturados

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 200,00 | R$ 240,00 | **-R$ 40,00** 🟡 |
| PIS | R$ 25,00 | R$ 33,00 | **-R$ 8,00** 🟡 |
| COFINS | R$ 120,00 | R$ 152,00 | **-R$ 32,00** 🟡 |

- **Total pago a menos:** R$ 80,00
- **Status:** RISCO FISCAL 🟡

### NF-e 18 - 🟡 IMPOSTO PAGO A MENOS
- **Chave:** 35230100000018...
- **Problema:** Valores abaixo do esperado

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 400,00 | R$ 480,00 | **-R$ 80,00** 🟡 |
| PIS | R$ 50,00 | R$ 66,00 | **-R$ 16,00** 🟡 |
| COFINS | R$ 240,00 | R$ 304,00 | **-R$ 64,00** 🟡 |

- **Total pago a menos:** R$ 160,00
- **Status:** RISCO FISCAL 🟡

### NF-e 19 - 🟡 IMPOSTO PAGO A MENOS
- **Chave:** 35230100000019...
- **Problema:** PIS/COFINS subfaturados

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 420,00 | R$ 504,00 | **-R$ 84,00** 🟡 |
| PIS | R$ 55,00 | R$ 69,30 | **-R$ 14,30** 🟡 |
| COFINS | R$ 250,00 | R$ 319,20 | **-R$ 69,20** 🟡 |

- **Total pago a menos:** R$ 167,50
- **Status:** RISCO FISCAL 🟡

### NF-e 20 - 🟡 IMPOSTO PAGO A MENOS
- **Chave:** 35230100000020...
- **Problema:** Todos os tributos abaixo do esperado

| Tributo | Pago | Esperado | Diferença |
|---------|------|----------|-----------|
| ICMS | R$ 240,00 | R$ 288,00 | **-R$ 48,00** 🟡 |
| PIS | R$ 30,00 | R$ 39,60 | **-R$ 9,60** 🟡 |
| COFINS | R$ 140,00 | R$ 182,40 | **-R$ 42,40** 🟡 |

- **Total pago a menos:** R$ 100,00
- **Status:** RISCO FISCAL 🟡

---

## 📊 Resumo Estatístico Esperado

### Distribuição por Status
- ✅ **Aprovadas:** 5 NF-e (25%)
- ⚠️ **Dados Faltantes:** 5 NF-e (25%)
- 🔴 **Imposto Pago a Mais:** 5 NF-e (25%)
- 🟡 **Imposto Pago a Menos:** 5 NF-e (25%)

### Impacto Financeiro Total

| Categoria | Valor |
|-----------|-------|
| 💰 Total pago a MAIS (prejuízo) | **R$ 998,75** |
| ⚠️ Total pago a MENOS (risco) | **R$ 681,25** |
| 📉 Diferença líquida | **R$ 317,50** (empresa pagou a mais) |

### Erros por Tributo

| Tributo | Qtd Erros | Total Pago a Mais | Total Pago a Menos |
|---------|-----------|-------------------|--------------------|
| ICMS | 10 | R$ 570,00 | R$ 322,00 |
| PIS | 10 | R$ 93,35 | R$ 65,65 |
| COFINS | 10 | R$ 335,40 | R$ 293,60 |

---

## 🎯 Validações Específicas Esperadas

### Validação de NCM
- ✅ NCM 17011100 (Açúcar Cristal) → Encontrado na base
- ✅ NCM 17019900 (Açúcar Refinado/Demerara) → Encontrado na base
- ❌ NF-e 9 → NCM ausente

### Validação de CFOP
- ✅ CFOP 5101 (Venda interna SP) → Válido
- ✅ CFOP 6101 (Venda interestadual) → Válido
- ❌ NF-e 9 → CFOP ausente

### Validação de CST PIS/COFINS
- ✅ CST 01 (Operação Tributável - Base de Cálculo) → Válido para todas as notas

### Tolerância de Arredondamento
- **Margem aceita:** ±R$ 0,50
- **NF-e que devem passar na tolerância:** Nenhuma (todas as diferenças > R$ 0,50)

---

## 🔍 Como Usar Este Arquivo

1. **Carregar o CSV** no validador
2. **Executar validação local** (CSV + SQLite)
3. **Comparar resultados** com este documento
4. **Verificar cada grupo** de notas:
   - Grupo 1: Deve aprovar sem erros
   - Grupo 2: Deve mostrar avisos de dados faltantes
   - Grupo 3: Deve alertar sobre valores pagos a mais
   - Grupo 4: Deve alertar sobre valores pagos a menos
5. **Validar estatísticas** finais

---

**Gerado em:** 16/10/2024
**Versão do Schema:** 1.0.0
**Base Legal:** Lei 10.637/2002 (PIS), Lei 10.833/2003 (COFINS), RICMS-SP
