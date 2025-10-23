#!/bin/bash
# Script de execução de testes - NF-e Validator MVP

echo "🧪 Iniciando suíte de testes..."
echo "================================="

# Criar diretório de relatórios
mkdir -p reports/coverage

# Executar testes com cobertura
pytest tests/ \
    --verbose \
    --cov=src \
    --cov-report=html:reports/coverage \
    --cov-report=term-missing \
    --cov-fail-under=80 \
    --html=reports/test_report.html \
    --self-contained-html \
    --junitxml=reports/junit.xml \
    -v

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
    echo "📊 Relatório de cobertura: reports/coverage/index.html"
    echo "📄 Relatório de testes: reports/test_report.html"
else
    echo "❌ Alguns testes falharam. Verifique os logs acima."
    exit 1
fi
