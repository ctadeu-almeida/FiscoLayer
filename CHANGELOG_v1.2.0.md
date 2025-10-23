# Changelog - v1.2.0

## 🚀 Principais Modificações

### ✅ Suporte a 4 Provedores de IA (anteriormente 3)

**Anterior (v1.1.0):**
- Google Gemini
- OpenAI GPT
- Grok (xAI)

**Atual (v1.2.0):**
- Google Gemini (Gemini 1.5 Pro, 2.0 Flash Exp, 2.5 Flash)
- OpenAI GPT (GPT-4o, GPT-4o Mini)
- **Claude (Anthropic)** - NOVO ✨
- Groq (Llama 3.3 70B)

---

### 🎛️ Seletor de Provedor Unificado

**Interface melhorada:**
- Dropdown único para seleção de provedor
- Campo de modelo personalizado (opcional)
- Modelos padrão inteligentes por provedor
- Aliases e normalização automática de nomes

**Antes:**
```
[ ] Gemini API Key
[ ] OpenAI API Key
[ ] Grok API Key
```

**Agora:**
```
[Dropdown] Provedor: Google Gemini / OpenAI / Claude / Groq
[Campo] Modelo preferencial: (opcional)
[Campo] API Key: (específica do provedor)
```

---

### 🧠 Sistema de Normalização de Provedores

**Arquivo:** `src/agents/eda_agent.py`

Funções adicionadas:
- `_normalize_provider()` - Mapeia aliases (google→gemini, anthropic→claude)
- `_normalize_model()` - Padroniza nomes de modelos
- `_provider_env_var()` - Retorna variável de ambiente correta
- `_export_env_for_provider()` - Configura env vars automaticamente

**Modelos padrão por provedor:**
```python
gemini  → gemini-1.5-pro
openai  → gpt-4o-mini
claude  → claude-3-5-sonnet-20240620
groq    → llama-3.3-70b-versatile
```

---

### 📝 Aliases de Modelos

**Gemini:**
- `flash` → `gemini-2.5-flash`
- `flash-exp` → `gemini-2.0-flash-exp`
- `1.5-pro` → `gemini-1.5-pro`

**OpenAI:**
- `gpt4o-mini` → `gpt-4o-mini`
- `gpt4o` → `gpt-4o`

**Claude:**
- `claude-35-sonnet-20240620` → `claude-3-5-sonnet-20240620`
- `claude-3-5-sonnet` → `claude-3-5-sonnet-20240620`

**Groq:**
- `llama-33-70b-versatile` → `llama-3.3-70b-versatile`
- `llama3.3-70b-versatile` → `llama-3.3-70b-versatile`

---

### 🔧 Melhorias na Inicialização

**EDAAgent - Construtor atualizado:**
```python
# Antes (v1.1.0)
EDAAgent(model_type="gemini", api_key="...")

# Agora (v1.2.0)
EDAAgent(provider="claude", model="claude-3-5-sonnet-20240620", api_key="...")
```

**Parâmetros:**
- `provider` - Provedor de IA (gemini/openai/claude/groq)
- `model` - Nome do modelo (opcional, usa padrão se omitido)
- `api_key` - Chave da API

---

### 📊 Interface app.py

**Catálogo de provedores (`provider_catalog`):**
```python
{
    "gemini": {
        "display": "Google Gemini",
        "help": "https://makersuite.google.com/app/apikey",
        "env": "GOOGLE_API_KEY",
        "state_key": "gemini_api_key",
        "default_model": "gemini-1.5-pro"
    },
    "claude": {
        "display": "Claude (Anthropic)",
        "help": "https://console.anthropic.com",
        "env": "ANTHROPIC_API_KEY",
        "state_key": "claude_api_key",
        "default_model": "claude-3-5-sonnet-20240620"
    },
    ...
}
```

---

### 🔄 Auto-população de Database

**Mantido da v1.1.0:**
- Database populado automaticamente na primeira execução
- Função `ensure_database_populated()` integrada no app.py

---

## 📦 Dependências

### Novas Dependências:
```
langchain-anthropic>=0.1.0  # Para Claude
```

### Mantidas:
```
langchain-google-genai>=1.0.0  # Gemini
langchain-openai>=0.0.5        # OpenAI + Groq
```

---

## 🎯 Benefícios

1. **Flexibilidade** - Usuário escolhe o provedor preferido
2. **Fallback inteligente** - Se um modelo falhar, pode trocar facilmente
3. **UX melhorada** - Interface mais limpa e intuitiva
4. **Aliases** - Nomes de modelos simplificados
5. **Modelos padrão** - Não precisa decorar nomes completos

---

## 🔄 Breaking Changes

### ⚠️ Mudança no construtor EDAAgent

**Código antigo (v1.1.0):**
```python
agent = EDAAgent(model_type="gemini", api_key="...")
```

**Código novo (v1.2.0):**
```python
agent = EDAAgent(provider="gemini", model="gemini-1.5-pro", api_key="...")
```

**Impacto:** Código que instancia diretamente `EDAAgent` precisa ser atualizado.

---

## 📈 Estatísticas

- **Linhas de código:** 2332 (app.py)
- **Funções principais:** 15
- **Provedores suportados:** 4 (era 3)
- **Modelos suportados:** 10+ (com aliases)

---

## 🐛 Correções

- Normalização de acentos em nomes de modelos
- Tratamento de aliases inconsistentes
- Validação de variáveis de ambiente por provedor

---

**Versão:** 1.2.0
**Data:** 23/10/2025
**Status:** ✅ Produção Ready
