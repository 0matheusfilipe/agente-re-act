---
title: ReAct Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.16.0
app_file: react_assistant.py
pinned: false
---

# 🤖 ReAct Assistant

Agente de IA que implementa o paradigma **ReAct (Reasoning + Acting)** usando LangChain.

## 🆕 Novidades

- ✅ **Busca Web com SerpAPI**: Agora o agente pode buscar informações atualizadas na internet!
- ✅ **5 Ferramentas**: Calculator, KnowledgeBase, Weather, CryptoPrice e WebSearch
- ✅ **Modo Graceful Degradation**: Funciona mesmo sem SerpAPI configurada
- ✅ **Logging Aprimorado**: Tracking completo de todas as ferramentas

## 🎯 Funcionalidades

- **Reasoning**: O agente pensa antes de agir
- **Acting**: Usa ferramentas reais para resolver tarefas
- **Web Search**: Busca informações atualizadas no Google
- **Logging**: Sistema completo de LLMOps
- **Multi-tool**: 5 ferramentas integradas

## 🛠️ Ferramentas

1. **Calculator**: Cálculos matemáticos
2. **KnowledgeBase**: Base de conhecimento sobre tecnologia
3. **Weather**: API pública de clima (wttr.in)
4. **CryptoPrice**: Preços de criptomoedas (CoinGecko)
5. **WebSearch**: Busca no Google via SerpAPI ⭐!

## 🔑 Configuração

### Obrigatório

```bash
export OPENAI_API_KEY="sua_chave_openai"
```

### Opcional (para habilitar busca web)

```bash
export SERPAPI_KEY="sua_chave_serpapi"
```

**Como obter chave SerpAPI:**
1. Acesse [serpapi.com/users/sign_up](https://serpapi.com/users/sign_up)
2. Crie uma conta gratuita
3. Copie sua API key do dashboard
4. Plano gratuito: 100 buscas/mês

## 🚀 Como usar

### Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves

# Executar
python react_assistant.py
```

## 💡 Exemplos de Uso

### Sem WebSearch
```bash
- "Quanto é 15% de 2500?"
- "O que é LangChain?"
- "Qual o clima em São Paulo?"
- "Qual o preço do Bitcoin?"
```

### Com WebSearch
```bash
- "Quais as últimas notícias sobre IA?"
- "Quem ganhou a última Copa do Mundo?"
- "Qual o preço das ações da Apple hoje?"
- "Resumo das notícias de tecnologia desta semana"
```

## 📊 LLMOps

- Logging completo em `react_agent.log`
- Métricas de tokens e custo
- Tracking de performance por ferramenta
- Error handling robusto
- Graceful degradation (funciona sem SerpAPI)

## 🧩 Competências Demonstradas

✅ LangChain Agents (ReAct)  
✅ Custom Tools  
✅ API Integration (múltiplas APIs)  
✅ Web Scraping (SerpAPI)  
✅ LLMOps (logging, metrics)  
✅ Production-ready code  
✅ Graceful degradation  
✅ Error handling  
✅ Gradio Interface  
✅ HF Spaces Deploy

## 🏗️ Arquitetura

```bash
ReActAssistant v2.0
├── Tools (5)
│   ├── Calculator (local)
│   ├── KnowledgeBase (local)
│   ├── Weather (wttr.in API)
│   ├── CryptoPrice (CoinGecko API)
│   └── WebSearch (SerpAPI)
├── LLM (OpenAI GPT-3.5/4)
├── Agent (ReAct Pattern)
├── Logging (LLMOps)
└── Interface (Gradio)
```

## 📈 Custos

### OpenAI (obrigatório)
- GPT-3.5-turbo: ~$0.001 por query
- GPT-4: ~$0.03 por query

### SerpAPI (opcional)
- Plano gratuito: 250 buscas/mês
- Plano pago: A partir de $50/mês (5000 buscas)

## 🔒 Segurança

- ✅ Sanitização de inputs (Calculator)
- ✅ Timeout em requisições HTTP
- ✅ Error handling robusto
- ✅ Validação de API keys
- ✅ Rate limiting awareness

## 📝 Changelog

### v2.0 (2024-11-18)
- ➕ Adicionada ferramenta WebSearch (SerpAPI)
- ➕ Suporte a Answer Boxes e Knowledge Graphs
- ➕ Formatação rica de resultados de busca
- ➕ Graceful degradation (funciona sem SerpAPI)
- ➕ Método `get_available_tools()`
- 🔧 Melhorias no logging
- 📚 Documentação expandida

### v1.0 (2024-11-17)
- 🎉 Lançamento inicial
- ✅ 4 ferramentas básicas
- ✅ Interface Gradio
- ✅ Sistema de logging

## 🤝 Contribuindo

Sugestões de novas ferramentas:
- [ ] Wikipedia Search
- [ ] News API
- [ ] Stock Market Data
- [ ] Translation API
- [ ] Image Generation

## 📄 Licença

MIT License - Use livremente!

## 👨‍💻 Autor

Desenvolvido como demonstração de competências em:
- LangChain & Agents
- ReAct Pattern
- LLMOps
- Production ML Systems


## 5️⃣ GUIA DE USO DA SERPAPI

```markdown
# 🔍 Guia Completo: SerpAPI no ReAct Assistant

## O que é SerpAPI?

SerpAPI é um serviço que permite fazer buscas programáticas no Google, Bing, Yahoo e outros motores de busca, retornando resultados estruturados em JSON.

## Por que usar SerpAPI?

### ✅ Vantagens
- **Estruturado**: Resultados em JSON, fácil de parsear
- **Confiável**: API estável e bem documentada
- **Rico**: Inclui Answer Boxes, Knowledge Graphs, Related Questions
- **Legal**: Respeita os termos de serviço do Google
- **Simples**: Não precisa lidar com HTML parsing ou CAPTCHAs

### ❌ Alternativas (e por que não usamos)
- **Google Custom Search API**: Limitada, resultados menos ricos
- **Web Scraping direto**: Ilegal, instável, bloqueado por CAPTCHAs
- **Bing Search API**: Menos resultados, menos features

## Como funciona no ReAct Assistant?

### 1. Detecção Automática

O agente decide quando usar WebSearch baseado na query:

```python
# O LLM lê a description da tool:
description=(
    "Útil para buscar informações atualizadas na internet quando "
    "a base de conhecimento interna não tem a resposta. "
    "Use para: notícias recentes, eventos atuais, informações "
    "que mudam frequentemente, fatos que você não conhece."
)
```

### 2. Exemplos de Queries que Acionam WebSearch

✅ **Usa WebSearch:**
- "Quais as últimas notícias sobre IA?"
- "Quem ganhou a Copa do Mundo de 2022?"
- "Qual o preço das ações da Apple hoje?"
- "Resumo das notícias de tecnologia desta semana"

❌ **Não usa WebSearch (usa KnowledgeBase):**
- "O que é Python?" (conhecimento estático)
- "Explique o que é ReAct" (na base interna)

### 3. Fluxo de Execução

```
User: "Quais as últimas notícias sobre IA?"
  ↓
LLM Thought: "Preciso de informações atualizadas. Vou usar WebSearch."
  ↓
Action: WebSearch
Action Input: "últimas notícias inteligência artificial"
  ↓
SerpAPI: Faz busca no Google
  ↓
Retorna: Answer Box + 5 resultados orgânicos + Related Questions
  ↓
LLM: Sintetiza a resposta
  ↓
Final Answer: "As principais notícias sobre IA são..."
```

## Estrutura da Resposta SerpAPI

### Exemplo de JSON retornado:

```json
{
  "answer_box": {
    "answer": "Resposta direta do Google",
    "snippet": "Trecho destacado"
  },
  "knowledge_graph": {
    "title": "Inteligência Artificial",
    "description": "IA é o campo da ciência..."
  },
  "organic_results": [
    {
      "position": 1,
      "title": "Últimas notícias sobre IA",
      "link": "https://example.com/news",
      "snippet": "Descrição do resultado..."
    }
  ],
  "related_questions": [
    {
      "question": "O que é IA generativa?",
      "answer": "IA generativa é..."
    }
  ]
}
```

### Como formatamos para o usuário:

```
🔍 Resultados da busca para: 'últimas notícias IA'

📌 Resposta Direta:
IA é o campo da ciência da computação...

📄 Principais Resultados:

1. Últimas notícias sobre IA
Descrição do resultado...
🔗 https://example.com/news

2. Avanços em IA Generativa
Outra descrição...
🔗 https://example.com/ai

❓ Perguntas Relacionadas:
- O que é IA generativa?
- Como funciona o ChatGPT?
```

## Configuração Passo a Passo

### 1. Criar Conta

1. Acesse: https://serpapi.com/users/sign_up
2. Preencha email e senha
3. Confirme email

### 2. Obter API Key

1. Faça login
2. Vá para: https://serpapi.com/manage-api-key
3. Copie sua API key (formato: `abc123...xyz`)

### 3. Configurar no Projeto

#### Opção A: Variável de Ambiente

```bash
# Linux/Mac
export SERPAPI_KEY="sua_chave_aqui"

# Windows (CMD)
set SERPAPI_KEY=sua_chave_aqui

# Windows (PowerShell)
$env:SERPAPI_KEY="sua_chave_aqui"
```

#### Opção B: Arquivo .env

```bash
# .env
SERPAPI_KEY=sua_chave_aqui
```

#### Opção C: Código Direto (não recomendado)

```python
assistant = ReActAssistant(
    openai_api_key="sk-...",
    serpapi_key="sua_chave_serpapi"
)
```

### 4. Verificar Configuração

```python
from react_assistant import ReActAssistant

assistant = ReActAssistant()
print(assistant.get_available_tools())

# Se WebSearch aparecer, está configurado!
# ['Calculator', 'KnowledgeBase', 'Weather', 'CryptoPrice', 'WebSearch']
```

## Limites e Custos

### Plano Gratuito
- ✅ 250 buscas/mês
- ✅ Todos os recursos
- ✅ Sem cartão de crédito
- ❌ Não pode exceder limite

### Planos Pagos

| Plano | Buscas/mês | Preço/mês |
|-------|------------|-----------|
| Free | 250 | $0 |
| Developer | 5,000 | $50 |
| Production | 30,000 | $250 |
| Enterprise | Ilimitado | Custom |

### Dicas para Economizar

1. **Cache local**: Salve resultados de buscas comuns
2. **Use KnowledgeBase primeiro**: Só busca na web se necessário
3. **Limite num_results**: Padrão é 5, não precisa de mais
4. **Monitore uso**: Dashboard da SerpAPI mostra consumo

## Troubleshooting

### Erro: "SERPAPI_KEY não configurada"

**Causa**: Variável de ambiente não definida

**Solução**:
```bash
export SERPAPI_KEY="sua_chave"
python react_assistant.py
```

### Erro: "Chave SerpAPI inválida ou expirada"

**Causa**: Chave incorreta ou conta suspensa

**Solução**:
1. Verifique a chave no dashboard
2. Copie novamente (sem espaços)
3. Verifique se a conta está ativa

### Erro: "Limite de buscas excedido"

**Causa**: Ultrapassou 100 buscas/mês (plano gratuito)

**Solução**:
1. Aguarde o reset mensal
2. Ou faça upgrade para plano pago

### WebSearch não é chamada

**Causa**: LLM não identificou necessidade de busca web

**Solução**:
- Seja mais explícito: "Busque na internet sobre..."
- Use queries que exigem informação atualizada

## Exemplos Práticos

### Exemplo 1: Notícias Recentes

```python
result = assistant.run("Quais as últimas notícias sobre IA?")
print(assistant.explain_reasoning(result))
```

**Output:**
```
Passo 1:
💭 Pensamento: Preciso buscar notícias atualizadas. Vou usar WebSearch.
🔧 Ferramenta: WebSearch
📥 Input: últimas notícias inteligência artificial
📤 Resultado: [5 resultados do Google]

✅ RESPOSTA FINAL:
As principais notícias sobre IA incluem...
```

### Exemplo 2: Fatos Atuais

```python
result = assistant.run("Quem é o presidente do Brasil em 2024?")
```

### Exemplo 3: Combinação de Tools

```python
result = assistant.run(
    "Busque o preço do Bitcoin e me diga se está acima de $50,000"
)
```

**Fluxo:**
1. Usa `CryptoPrice` para obter preço
2. Usa `Calculator` para comparar
3. Retorna resposta

## Monitoramento

### Logs

Todos os usos de WebSearch são logados:

```
2024-11-18 10:30:45 - INFO - [WEBSEARCH] Buscando: últimas notícias IA
2024-11-18 10:30:46 - INFO - [WEBSEARCH] Sucesso: 5 resultados
```

### Métricas

```python
result = assistant.run("query")
print(result["metrics"])

# Output:
{
    "total_tokens": 450,
    "total_cost": 0.0023,
    "duration_seconds": 2.3
}
```

## Boas Práticas

### ✅ Faça

- Use para informações que mudam frequentemente
- Seja específico nas queries
- Monitore seu uso mensal
- Implemente cache para queries comuns

### ❌ Não Faça

- Não use para conhecimento estático
- Não faça buscas redundantes
- Não exponha sua API key no código
- Não ultrapasse o rate limit

## Alternativas Gratuitas

Se não quiser usar SerpAPI, o agente funciona normalmente com as outras 4 ferramentas:

```python
# Sem WebSearch, mas totalmente funcional
assistant = ReActAssistant()  # Sem SERPAPI_KEY

# Ainda pode:
- Calcular
- Buscar na base de conhecimento
- Consultar clima
- Ver preços de cripto
```

## Conclusão

A integração com SerpAPI transforma o ReAct Assistant em um agente verdadeiramente poderoso, capaz de:

✅ Acessar informações atualizadas  
✅ Responder sobre eventos recentes  
✅ Combinar múltiplas fontes de dados  
✅ Funcionar como um assistente completo  

**Próximos passos:**
1. Configure sua chave
2. Teste com queries atuais
3. Monitore o uso
4. Aproveite! 🚀
```

## 6️⃣ TESTES ATUALIZADOS

```python
# test_websearch.py
"""
Testes específicos para a ferramenta WebSearch
"""

import os
from react_assistant import ReActAssistant, WebSearchTool

def test_websearch_tool():
    """Testa a ferramenta WebSearch isoladamente"""
    print("=" * 80)
    print("TESTE: WebSearch Tool")
    print("=" * 80)
    
    # Inicializa a tool
    Web Search = WebSearchTool()
    
    # Verifica se está disponível
    if not Web Search.is_available():
        print("⚠️ WebSearch não disponível - SERPAPI_KEY não configurada")
        print("Configure SERPAPI_KEY para executar este teste")
        return
    
    # Teste 1: Busca simples
    print("\n📝 Teste 1: Busca simples")
    result = Web Search.search("Python programming language")
    print(result)
    
    # Teste 2: Busca em português
    print("\n📝 Teste 2: Busca em português")
    result = Web Search.search("últimas notícias tecnologia")
    print(result)
    
    # Teste 3: Busca com poucos resultados
    print("\n📝 Teste 3: Busca com 3 resultados")
    result = Web Search.search("inteligência artificial", num_results=3)
    print(result)


def test_agent_with_websearch():
    """Testa o agente completo com WebSearch"""
    print("\n" + "=" * 80)
    print("TESTE: Agente ReAct com WebSearch")
    print("=" * 80)
    
    try:
        assistant = ReActAssistant()
        
        # Verifica ferramentas disponíveis
        tools = assistant.get_available_tools()
        print(f"\n✅ Ferramentas disponíveis: {', '.join(tools)}")
        
        if "WebSearch" not in tools:
            print("⚠️ WebSearch não disponível - testes limitados")
            return
        
        # Teste 1: Query que deve usar WebSearch
        print("\n" + "=" * 80)
        print("📝 Teste 1: Notícias recentes (deve usar WebSearch)")
        print("=" * 80)
        
        result = assistant.run("Quais as últimas notícias sobre inteligência artificial?")
        print(assistant.explain_reasoning(result))
        
        # Teste 2: Query que deve usar KnowledgeBase (não WebSearch)
        print("\n" + "=" * 80)
        print("📝 Teste 2: Conhecimento estático (deve usar KnowledgeBase)")
        print("=" * 80)
        
        result = assistant.run("O que é Python?")
        print(assistant.explain_reasoning(result))
        
        # Teste 3: Query que combina múltiplas tools
        print("\n" + "=" * 80)
        print("📝 Teste 3: Multi-tool (WebSearch + Calculator)")
        print("=" * 80)
        
        result = assistant.run(
            "Busque o preço atual do Bitcoin e calcule quanto seria 0.5 BTC em dólares"
        )
        print(assistant.explain_reasoning(result))
        
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Configure OPENAI_API_KEY para executar este teste")


if __name__ == "__main__":
    # Executa testes
    test_websearch_tool()
    test_agent_with_websearch()
    
    print("\n" + "=" * 80)
    print("✅ Testes concluídos!")
    print("=" * 80)
```

## 🎯 RESUMO DAS MUDANÇAS

### ✅ O que foi adicionado:

1. **WebSearchTool**: Nova classe completa com:
   - Integração com SerpAPI
   - Formatação rica de resultados
   - Answer Boxes e Knowledge Graphs
   - Error handling robusto
   - Graceful degradation

2. **Método `is_available()`**: Verifica se SerpAPI está configurada
3. **Método `get_available_tools()`**: Lista ferramentas ativas
4. **Logging aprimorado**: Tracking de todas as buscas web
5. **Interface atualizada**: Mostra status da WebSearch
6. **Documentação completa**: Guia de uso da SerpAPI
7. **Testes específicos**: Suite de testes para WebSearch

### 🔑 Como usar:

```bash
# 1. Configure as chaves
export OPENAI_API_KEY="sua_chave_openai"
export SERPAPI_KEY="sua_chave_serpapi"  # Opcional

# 2. Execute
python react_assistant.py

# 3. Teste queries que usam WebSearch
"Quais as últimas notícias sobre IA?"
"Quem ganhou a Copa do Mundo de 2022?"
```