# Guia de Instalação Local - FiscoLayer

**Versão:** 1.1.0
**Data:** Outubro 2025
**Python:** 3.10+

---

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (11+)

### Software Necessário
1. **Python 3.10 ou superior**
   - Download: https://www.python.org/downloads/
   - Verificar versão: `python --version`

2. **pip** (gerenciador de pacotes Python)
   - Geralmente incluído com Python
   - Verificar: `pip --version`

3. **Git** (opcional, para clonar repositório)
   - Download: https://git-scm.com/downloads

---

## 🚀 Instalação Passo a Passo

### Método 1: Instalação Padrão (pip)

#### 1. Clonar ou Baixar Repositório

```bash
# Via Git
git clone https://github.com/ctadeu-almeida/FiscoLayer.git
cd FiscoLayer

# Ou baixe o ZIP e extraia
```

#### 2. Criar Ambiente Virtual (Recomendado)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Tempo estimado:** 3-5 minutos (depende da conexão)

#### 4. Popular Base de Dados Fiscal

```bash
python scripts/populate_db.py
```

**Saída esperada:**
```
[*] Populando Database - NF-e Validator MVP
[*] Database: C:\app\FiscoLayer\src\database\rules.db
[INFO] Populando NCM Rules...
[OK] 5 NCMs inseridos
[INFO] Populando PIS/COFINS Rules...
[OK] 7 CSTs inseridos
[INFO] Populando CFOP Rules...
[OK] 7 CFOPs inseridos
[INFO] Populando State Overrides...
[OK] 3 regras estaduais inseridas
[INFO] Populando Legal References...
[OK] 5 referências legais inseridas
[STATS] Database populado com sucesso!
Total de registros: 27
```

---

### Método 2: Instalação Rápida (uv)

O `uv` é um gerenciador de pacotes Python ultrarrápido (10-100x mais rápido que pip).

#### 1. Instalar uv

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Criar Projeto e Instalar Dependências

```bash
cd FiscoLayer
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt
```

**Tempo estimado:** 30-60 segundos

---

## 🔑 Configuração de APIs

### Obter Chaves de API

A aplicação suporta **3 provedores de IA**. Você precisa de **pelo menos uma** chave:

#### 1. Google Gemini (Recomendado)

**Por que usar:**
- ✅ Gratuito para uso moderado
- ✅ Excelente para análise de dados tabulares
- ✅ Modelo padrão do sistema

**Como obter:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com conta Google
3. Clique em "Create API Key"
4. Copie a chave (formato: `AIza...`)

**Limites gratuitos:**
- 60 requisições/minuto
- 1.500 requisições/dia

---

#### 2. OpenAI GPT (Alternativa)

**Por que usar:**
- ✅ Excelente raciocínio lógico
- ✅ Ideal para validações complexas
- ⚠️ Requer créditos pagos

**Como obter:**
1. Acesse: https://platform.openai.com/api-keys
2. Crie conta ou faça login
3. Adicione método de pagamento
4. Clique em "Create new secret key"
5. Copie a chave (formato: `sk-...`)

**Custos aproximados:**
- GPT-4o Mini: ~$0.15 / 1M tokens (entrada)
- GPT-4: ~$30 / 1M tokens (entrada)

---

#### 3. Grok (xAI) - Beta

**Por que usar:**
- ✅ Acesso a dados em tempo real
- ✅ Desenvolvido pela xAI (Elon Musk)
- ⚠️ Em fase beta (acesso limitado)

**Como obter:**
1. Acesse: https://x.ai
2. Solicite acesso beta
3. Aguarde aprovação
4. Copie a chave quando disponível

---

### Configurar Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Escolha UM dos provedores abaixo:

# Google Gemini (recomendado)
GOOGLE_API_KEY=AIza...

# OpenAI
OPENAI_API_KEY=sk-...

# Grok (xAI)
GROK_API_KEY=xai-...
```

**Nota:** Se não criar `.env`, você pode inserir a chave diretamente na interface Streamlit.

---

## ▶️ Executar Aplicação

### Iniciar Streamlit

```bash
streamlit run app.py
```

**Ou use o script helper:**

```bash
python run_streamlit.py
```

### Acesso

A aplicação abrirá automaticamente no navegador:

```
http://localhost:8501
```

Se não abrir, copie o link do terminal e cole no navegador.

---

## 🧪 Verificar Instalação

### Teste Rápido

```bash
python -c "
import streamlit as st
import pandas as pd
import langchain
print('✅ Todos os pacotes principais instalados!')
"
```

### Teste Completo (pytest)

```bash
# Instalar dependências de teste
pip install pytest pytest-cov

# Rodar testes
pytest tests/ -v
```

**Saída esperada:**
```
tests/test_integration.py::test_01_valid PASSED
tests/test_integration.py::test_02_ncm_error PASSED
tests/test_integration.py::test_03_pis_cofins_error PASSED
tests/test_integration.py::test_04_cfop_error PASSED
tests/test_integration.py::test_05_totals_error PASSED

========== 5 passed in 2.34s ==========
```

---

## 📁 Estrutura de Diretórios

Após instalação, você terá:

```
FiscoLayer/
├── app.py                      # Aplicação Streamlit principal
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação principal
├── INSTALL_LOCAL.md           # Este arquivo
├── ESTADO_ATUAL.md            # Estado da aplicação
│
├── src/                       # Código-fonte
│   ├── agents/               # Agentes de IA
│   │   ├── eda_agent.py     # Agente EDA multi-modelo
│   │   └── ncm_agent.py     # Agente NCM
│   ├── nfe_validator/        # Sistema de validação NF-e
│   │   ├── domain/          # Regras de negócio
│   │   └── infrastructure/  # Parsers e geradores
│   ├── repositories/         # Acesso a dados
│   ├── database/            # SQLite fiscal
│   └── visualization/       # Gráficos
│
├── tests/                    # Testes automatizados
│   ├── data/                # CSVs de teste
│   └── output/              # Relatórios de teste
│
├── scripts/                 # Scripts auxiliares
│   └── populate_db.py       # Popular database
│
└── charts/                  # Gráficos gerados (criado em runtime)
```

---

## 🔧 Troubleshooting

### Problema: `ModuleNotFoundError: No module named 'streamlit'`

**Solução:**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

---

### Problema: `ImportError: cannot import name 'ChatGoogleGenerativeAI'`

**Causa:** Versão incompatível do langchain-google-genai

**Solução:**
```bash
pip install --upgrade langchain-google-genai google-generativeai
```

---

### Problema: `sqlite3.OperationalError: database is locked`

**Causa:** Múltiplas instâncias acessando o mesmo database

**Solução:**
```bash
# Fechar todas as instâncias do Streamlit
# Deletar arquivo de lock
rm src/database/rules.db-journal  # Linux/macOS
del src\database\rules.db-journal  # Windows

# Reiniciar aplicação
streamlit run app.py
```

---

### Problema: API Key inválida

**Sintomas:**
```
google.api_core.exceptions.PermissionDenied: 403 API key not valid
```

**Soluções:**
1. Verifique se copiou a chave completa (sem espaços)
2. Confirme que a API está habilitada no console Google Cloud
3. Tente gerar nova chave em https://makersuite.google.com/app/apikey

---

### Problema: Port 8501 já em uso

**Sintoma:**
```
OSError: [Errno 98] Address already in use
```

**Solução:**
```bash
# Usar porta diferente
streamlit run app.py --server.port 8502

# Ou matar processo na porta 8501
# Linux/macOS
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

## 📊 Uso Básico

### 1. Análise EDA (Tab 1)

1. **Configurar API**
   - Insira chave Gemini/OpenAI/Grok
   - Clique em "🚀 Inicializar Modelo"
   - Aguarde mensagem: "✅ Modelo inicializado"

2. **Upload CSV**
   - Clique em "Browse files"
   - Selecione arquivo CSV ou ZIP
   - Sistema detecta automaticamente separador

3. **Analisar com Chat**
   - Digite pergunta: "Mostre estatísticas descritivas"
   - Agente gera análises e gráficos
   - Resultados aparecem em tempo real

---

### 2. Validação NF-e (Tab 2)

1. **Carregar Dados**
   - Faça upload do CSV de NF-e na Tab 1
   - Base fiscal é carregada automaticamente

2. **Validar**
   - Vá para Tab 2
   - Clique em "🔍 Validar NF-es dos Dados"
   - Aguarde progress bar

3. **Visualizar Resultados**
   - Veja relatório consolidado
   - Verifique erros por severidade
   - Baixe relatórios em MD ou JSON

---

## 🔄 Atualizar Aplicação

```bash
# Atualizar código do repositório
git pull origin main

# Atualizar dependências
pip install --upgrade -r requirements.txt

# Re-popular database (se necessário)
python scripts/populate_db.py
```

---

## 📞 Suporte

### Documentação
- **README principal:** `README.md`
- **Estado atual:** `ESTADO_ATUAL.md`
- **Testes:** `tests/README_TESTES.md`

### Comunidade
- **Issues:** https://github.com/ctadeu-almeida/FiscoLayer/issues
- **Discussões:** https://github.com/ctadeu-almeida/FiscoLayer/discussions

### Logs
- Logs aparecem no terminal onde executou `streamlit run app.py`
- Para debug detalhado, edite `app.py` e remova comentários de prints

---

## 📄 Licença

MIT License - Veja `LICENSE` para detalhes

---

**Desenvolvido para o setor sucroalcooleiro brasileiro** ❤️
*Versão 1.1.0 - Outubro 2025*
