"""
ReAct Assistant - Agente de IA com Reasoning + Acting
Demonstra: LangChain Agents, Tools customizadas, LLMOps, Deploy-ready
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
import requests

# ============================================================================
# IMPORTS CORRIGIDOS DO LANGCHAIN
# ============================================================================
try:
    # Tenta importar da nova estrutura (LangChain 0.1+)
    from langchain.agents import create_react_agent, AgentExecutor
except ImportError:
    try:
        # Fallback para estrutura alternativa
        from langchain.agents import AgentExecutor
        from langchain.agents.react.agent import create_react_agent
    except ImportError:
        # Última tentativa - imports separados
        from langchain_core.agents import AgentExecutor
        from langchain.agents import create_react_agent

from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Callback para tracking de tokens
try:
    from langchain_community.callbacks import get_openai_callback
except ImportError:
    from langchain.callbacks import get_openai_callback

# ============================================================================
# CONFIGURAÇÃO DE LOGGING (LLMOps)
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('react_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# TOOLS - Ferramentas que o agente pode usar
# ============================================================================

class CalculatorTool:
    """Ferramenta para cálculos matemáticos"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """
        Calcula expressões matemáticas seguras.
        
        Args:
            expression: Expressão matemática (ex: "2 + 2", "10 * 5 + 3")
        
        Returns:
            Resultado do cálculo ou mensagem de erro
        """
        try:
            logger.info(f"[CALCULATOR] Calculando: {expression}")
            # Sanitização básica para segurança
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                return "Erro: Expressão contém caracteres inválidos"
            
            result = eval(expression, {"__builtins__": {}}, {})
            logger.info(f"[CALCULATOR] Resultado: {result}")
            return f"Resultado: {result}"
        except Exception as e:
            logger.error(f"[CALCULATOR] Erro: {str(e)}")
            return f"Erro ao calcular: {str(e)}"


class KnowledgeBaseTool:
    """Ferramenta para buscar informações em uma base de conhecimento simulada"""
    
    def __init__(self):
        self.knowledge_base = {
            "python": "Python é uma linguagem de programação de alto nível, interpretada e de propósito geral. Criada por Guido van Rossum em 1991.",
            "langchain": "LangChain é um framework para desenvolvimento de aplicações com LLMs. Facilita a criação de agentes, chains e integração com ferramentas.",
            "react": "ReAct (Reasoning + Acting) é um paradigma onde o agente alterna entre raciocínio (pensamento) e ação (uso de ferramentas) para resolver tarefas.",
            "ia": "Inteligência Artificial é o campo da ciência da computação que busca criar sistemas capazes de realizar tarefas que normalmente requerem inteligência humana.",
            "machine learning": "Machine Learning é um subcampo da IA focado em algoritmos que melhoram automaticamente através da experiência e uso de dados.",
            "serpapi": "SerpAPI é uma API que permite fazer buscas no Google, Bing e outros motores de busca de forma programática, retornando resultados estruturados em JSON.",
        }
    
    def search(self, query: str) -> str:
        """
        Busca informações na base de conhecimento.
        
        Args:
            query: Termo de busca
        
        Returns:
            Informação encontrada ou mensagem de não encontrado
        """
        logger.info(f"[KNOWLEDGE] Buscando: {query}")
        query_lower = query.lower()
        
        for key, value in self.knowledge_base.items():
            if key in query_lower:
                logger.info(f"[KNOWLEDGE] Encontrado: {key}")
                return f"Informação sobre '{key}': {value}"
        
        logger.info(f"[KNOWLEDGE] Não encontrado: {query}")
        return f"Não encontrei informações sobre '{query}' na base de conhecimento."


class WeatherTool:
    """Ferramenta para consultar clima via API pública"""
    
    def __init__(self):
        self.base_url = "https://wttr.in"
    
    def get_weather(self, city: str) -> str:
        """
        Consulta o clima de uma cidade.
        
        Args:
            city: Nome da cidade
        
        Returns:
            Informações do clima ou mensagem de erro
        """
        try:
            logger.info(f"[WEATHER] Consultando clima: {city}")
            # wttr.in é uma API pública que não requer chave
            response = requests.get(
                f"{self.base_url}/{city}?format=j1",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                current = data['current_condition'][0]
                
                result = (
                    f"Clima em {city}:\n"
                    f"🌡️ Temperatura: {current['temp_C']}°C\n"
                    f"☁️ Condição: {current['weatherDesc'][0]['value']}\n"
                    f"💨 Vento: {current['windspeedKmph']} km/h\n"
                    f"💧 Umidade: {current['humidity']}%"
                )
                logger.info(f"[WEATHER] Sucesso: {city}")
                return result
            else:
                return f"Não consegui obter o clima para {city}"
        except Exception as e:
            logger.error(f"[WEATHER] Erro: {str(e)}")
            return f"Erro ao consultar clima: {str(e)}"


class CryptoTool:
    """Ferramenta para consultar preços de criptomoedas"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_price(self, crypto: str) -> str:
        """
        Consulta o preço de uma criptomoeda.
        
        Args:
            crypto: Nome ou símbolo da criptomoeda (ex: bitcoin, btc)
        
        Returns:
            Preço atual ou mensagem de erro
        """
        try:
            logger.info(f"[CRYPTO] Consultando preço: {crypto}")
            
            # Mapeamento de símbolos comuns
            crypto_map = {
                "btc": "bitcoin",
                "eth": "ethereum",
                "usdt": "tether",
                "bnb": "binancecoin",
                "sol": "solana",
                "ada": "cardano",
                "xrp": "ripple",
            }
            
            crypto_id = crypto_map.get(crypto.lower(), crypto.lower())
            
            response = requests.get(
                f"{self.base_url}/simple/price",
                params={
                    "ids": crypto_id,
                    "vs_currencies": "usd,brl",
                    "include_24hr_change": "true"
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if crypto_id in data:
                    info = data[crypto_id]
                    change = info.get('usd_24h_change', 0)
                    emoji = "📈" if change > 0 else "📉"
                    
                    result = (
                        f"💰 {crypto.upper()} - Preço Atual:\n"
                        f"🇺🇸 USD: ${info['usd']:,.2f}\n"
                        f"🇧🇷 BRL: R$ {info['brl']:,.2f}\n"
                        f"{emoji} Variação 24h: {change:.2f}%"
                    )
                    logger.info(f"[CRYPTO] Sucesso: {crypto}")
                    return result
                else:
                    return f"Criptomoeda '{crypto}' não encontrada"
            else:
                return f"Erro ao consultar preço de {crypto}"
        except Exception as e:
            logger.error(f"[CRYPTO] Erro: {str(e)}")
            return f"Erro ao consultar criptomoeda: {str(e)}"


class WebSearchTool:
    """
    Ferramenta para busca web usando SerpAPI.
    
    SerpAPI permite fazer buscas no Google de forma programática,
    retornando resultados estruturados em JSON.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa a ferramenta de busca web.
        
        Args:
            api_key: Chave da API SerpAPI (ou usa variável de ambiente)
        """
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search"
        
        # Log se a chave está configurada
        if self.api_key:
            logger.info("[WEBSEARCH] SerpAPI configurada com sucesso")
        else:
            logger.warning("[WEBSEARCH] SerpAPI_KEY não configurada - busca web desabilitada")
    
    def search(self, query: str, num_results: int = 5) -> str:
        """
        Realiza uma busca no Google via SerpAPI.
        
        Args:
            query: Termo de busca
            num_results: Número de resultados a retornar (padrão: 5)
        
        Returns:
            Resultados formatados ou mensagem de erro
        """
        # Verifica se a API está configurada
        if not self.api_key:
            return (
                "❌ Busca web não disponível: SERPAPI_KEY não configurada.\n"
                "Para habilitar, configure a variável de ambiente SERPAPI_KEY.\n"
                "Obtenha sua chave gratuita em: https://serpapi.com/users/sign_up"
            )
        
        try:
            logger.info(f"[WEBSEARCH] Buscando: {query}")
            
            # Parâmetros da busca
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": num_results,
                "gl": "br",  # Geolocalização: Brasil
                "hl": "pt",  # Idioma: Português
            }
            
            # Faz a requisição
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se há resultados orgânicos
                if "organic_results" not in data or len(data["organic_results"]) == 0:
                    logger.info(f"[WEBSEARCH] Nenhum resultado encontrado para: {query}")
                    return f"Nenhum resultado encontrado para '{query}'"
                
                # Formata os resultados
                results = self._format_results(data, query)
                logger.info(f"[WEBSEARCH] Sucesso: {len(data['organic_results'])} resultados")
                return results
            
            elif response.status_code == 401:
                logger.error("[WEBSEARCH] Erro de autenticação: chave inválida")
                return "❌ Erro: Chave SerpAPI inválida ou expirada"
            
            elif response.status_code == 429:
                logger.error("[WEBSEARCH] Limite de requisições excedido")
                return "❌ Erro: Limite de buscas excedido. Tente novamente mais tarde."
            
            else:
                logger.error(f"[WEBSEARCH] Erro HTTP {response.status_code}")
                return f"❌ Erro ao buscar: Status {response.status_code}"
        
        except requests.exceptions.Timeout:
            logger.error("[WEBSEARCH] Timeout na requisição")
            return "❌ Erro: Timeout ao buscar. Tente novamente."
        
        except Exception as e:
            logger.error(f"[WEBSEARCH] Erro: {str(e)}")
            return f"❌ Erro ao buscar: {str(e)}"
    
    def _format_results(self, data: Dict, query: str) -> str:
        """
        Formata os resultados da busca de forma legível.
        
        Args:
            data: Dados JSON da SerpAPI
            query: Query original
        
        Returns:
            Resultados formatados
        """
        results_text = f"🔍 **Resultados da busca para: '{query}'**\n\n"
        
        # Answer Box (se disponível)
        if "answer_box" in data:
            answer_box = data["answer_box"]
            if "answer" in answer_box:
                results_text += f"📌 **Resposta Direta:**\n{answer_box['answer']}\n\n"
            elif "snippet" in answer_box:
                results_text += f"📌 **Resposta Direta:**\n{answer_box['snippet']}\n\n"
        
        # Knowledge Graph (se disponível)
        if "knowledge_graph" in data:
            kg = data["knowledge_graph"]
            if "description" in kg:
                results_text += f"📚 **Sobre:**\n{kg['description']}\n\n"
        
        # Resultados orgânicos
        results_text += "📄 **Principais Resultados:**\n\n"
        
        for i, result in enumerate(data["organic_results"][:5], 1):
            title = result.get("title", "Sem título")
            snippet = result.get("snippet", "Sem descrição")
            link = result.get("link", "")
            
            results_text += f"**{i}. {title}**\n"
            results_text += f"{snippet}\n"
            results_text += f"🔗 {link}\n\n"
        
        # Related Questions (se disponível)
        if "related_questions" in data and len(data["related_questions"]) > 0:
            results_text += "❓ **Perguntas Relacionadas:**\n"
            for q in data["related_questions"][:3]:
                results_text += f"- {q.get('question', '')}\n"
        
        return results_text
    
    def is_available(self) -> bool:
        """
        Verifica se a ferramenta está disponível (chave configurada).
        
        Returns:
            True se a chave está configurada, False caso contrário
        """
        return self.api_key is not None


# ============================================================================
# REACT AGENT - Configuração do Agente
# ============================================================================

class ReActAssistant:
    """
    Agente ReAct completo com múltiplas ferramentas e logging.
    Demonstra o paradigma Reasoning + Acting.
    Versão 2.0 - Agora com Web Search!
    """
    
    def __init__(
        self, 
        openai_api_key: Optional[str] = None,
        serpapi_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ):
        """
        Inicializa o ReAct Assistant.
        
        Args:
            openai_api_key: Chave da API OpenAI (ou usa variável de ambiente)
            serpapi_key: Chave da API SerpAPI (ou usa variável de ambiente)
            model: Modelo a ser usado
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        # Inicializa ferramentas
        self.calculator = CalculatorTool()
        self.knowledge = KnowledgeBaseTool()
        self.weather = WeatherTool()
        self.crypto = CryptoTool()
        self.WebSearch = WebSearchTool(api_key=serpapi_key)
        
        # Configura LLM
        self.llm = ChatOpenAI(
            temperature=0,
            model=model,
            api_key=self.openai_api_key
        )
        
        # Define as tools para o agente
        self.tools = [
            Tool(
                name="Calculator",
                func=self.calculator.calculate,
                description="Útil para fazer cálculos matemáticos. Input: expressão matemática como string (ex: '2+2', '10*5+3')"
            ),
            Tool(
                name="KnowledgeBase",
                func=self.knowledge.search,
                description="Útil para buscar informações sobre tecnologia, programação, IA na base de conhecimento interna. Input: termo de busca como string"
            ),
            Tool(
                name="Weather",
                func=self.weather.get_weather,
                description="Útil para consultar o clima atual de uma cidade. Input: nome da cidade como string"
            ),
            Tool(
                name="CryptoPrice",
                func=self.crypto.get_price,
                description="Útil para consultar preço de criptomoedas. Input: nome ou símbolo da criptomoeda (ex: 'bitcoin', 'btc', 'ethereum')"
            ),
        ]
        
        # Adiciona WebSearch apenas se estiver disponível
        if self.WebSearch.is_available():
            self.tools.append(
                Tool(
                    name="WebSearch",
                    func=self.WebSearch.search,
                    description=(
                        "Útil para buscar informações atualizadas na internet quando a base de conhecimento interna não tem a resposta. "
                        "Use para: notícias recentes, eventos atuais, informações que mudam frequentemente, fatos que você não conhece. "
                        "Input: query de busca como string (ex: 'notícias sobre IA 2024', 'quem ganhou a copa do mundo')"
                      )
                  )
              )
            logger.info("[AGENT] WebSearch habilitada")
        else:
            logger.warning("[AGENT] WebSearch desabilitada - SERPAPI_KEY não configurada")
        
        # Prompt ReAct customizado
        self.prompt = PromptTemplate.from_template("""
Você é um assistente inteligente que usa o paradigma ReAct (Reasoning + Acting).

Você tem acesso às seguintes ferramentas:

{tools}

Use o seguinte formato:

Question: a pergunta/tarefa do usuário
Thought: você deve sempre pensar sobre o que fazer
Action: a ação a tomar, deve ser uma de [{tool_names}]
Action Input: o input para a ação
Observation: o resultado da ação
... (esse ciclo Thought/Action/Action Input/Observation pode repetir N vezes)
Thought: Agora eu sei a resposta final
Final Answer: a resposta final para o usuário

IMPORTANTE:
- Sempre explique seu raciocínio (Thought)
- Use as ferramentas quando necessário
- Para informações atualizadas ou que você não conhece, use WebSearch
- Para informações na base de conhecimento interna, use KnowledgeBase primeiro
- Seja preciso e objetivo
- Responda em português brasileiro

Question: {input}
Thought: {agent_scratchpad}
""")
        
        # Cria o agente ReAct
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Executor com configurações de LLMOps
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        
        logger.info(f"[AGENT] ReAct Assistant inicializado com {len(self.tools)} ferramentas")
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Executa uma query no agente ReAct.
        
        Args:
            query: Pergunta ou tarefa do usuário
        
        Returns:
            Dicionário com resposta, steps e métricas
        """
        logger.info(f"[AGENT] Nova query: {query}")
        start_time = datetime.now()
        
        try:
            # Executa com tracking de tokens
            with get_openai_callback() as cb:
                result = self.agent_executor.invoke({"input": query})
                
                # Métricas de LLMOps
                metrics = {
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": cb.total_cost,
                    "duration_seconds": (datetime.now() - start_time).total_seconds()
                }
                
                logger.info(f"[AGENT] Métricas: {json.dumps(metrics, indent=2)}")
                
                return {
                    "success": True,
                    "answer": result["output"],
                    "intermediate_steps": result["intermediate_steps"],
                    "metrics": metrics,
                    "timestamp": datetime.now().isoformat()
                }
        
        except Exception as e:
            logger.error(f"[AGENT] Erro: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def explain_reasoning(self, result: Dict[str, Any]) -> str:
        """
        Explica o raciocínio do agente de forma legível.
        
        Args:
            result: Resultado do método run()
        
        Returns:
            Explicação formatada
        """
        if not result["success"]:
            return f"❌ Erro: {result['error']}"
        
        explanation = "🤖 **RACIOCÍNIO DO AGENTE ReAct**\n\n"
        
        # Mostra os passos intermediários
        for i, (action, observation) in enumerate(result["intermediate_steps"], 1):
            explanation += f"**Passo {i}:**\n"
            explanation += f"💭 Pensamento: {action.log}\n"
            explanation += f"🔧 Ferramenta: {action.tool}\n"
            explanation += f"📥 Input: {action.tool_input}\n"
            explanation += f"📤 Resultado: {observation}\n\n"
        
        explanation += f"✅ **RESPOSTA FINAL:**\n{result['answer']}\n\n"
        
        # Métricas
        metrics = result["metrics"]
        explanation += "📊 **MÉTRICAS:**\n"
        explanation += f"- Tokens: {metrics['total_tokens']}\n"
        explanation += f"- Custo: ${metrics['total_cost']:.4f}\n"
        explanation += f"- Duração: {metrics['duration_seconds']:.2f}s\n"
        
        return explanation
    
    def get_available_tools(self) -> List[str]:
        """
        Retorna lista de ferramentas disponíveis.
        
        Returns:
            Lista com nomes das ferramentas
        """
        return [tool.name for tool in self.tools]


# ============================================================================
# INTERFACE GRADIO (Deploy-ready para HF Spaces)
# ============================================================================

def create_gradio_interface():
    """Cria interface Gradio para deploy"""
    import gradio as gr
    
    # Inicializa o agente
    assistant = ReActAssistant()
    
    # Verifica quais ferramentas estão disponíveis
    available_tools = assistant.get_available_tools()
    websearch_enabled = "WebSearch" in available_tools
    
    def process_query(query: str, show_reasoning: bool = True):
        """Processa query e retorna resposta"""
        result = assistant.run(query)
        
        if show_reasoning:
            return assistant.explain_reasoning(result)
        else:
            return result["answer"] if result["success"] else f"Erro: {result['error']}"
    
    # Interface
    with gr.Blocks(title="ReAct Assistant v2.0", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🤖 ReAct Assistant v2.0
        
        Agente de IA que usa o paradigma **Reasoning + Acting** para resolver tarefas.
        
        ### 🛠️ Ferramentas disponíveis:
        - 🧮 **Calculator**: Cálculos matemáticos
        - 📚 **KnowledgeBase**: Busca em base de conhecimento interna
        - 🌤️ **Weather**: Consulta clima de cidades
        - 💰 **CryptoPrice**: Preços de criptomoedas
        - 🔍 **WebSearch**: Busca na internet (Google via SerpAPI) """ + 
        ("✅" if websearch_enabled else "❌ *Desabilitada - configure SERPAPI_KEY*") + """
        
        ### 💡 Exemplos de perguntas:
        - "Quanto é 15% de 2500?"
        - "O que é LangChain?"
        - "Qual o clima em São Paulo?"
        - "Qual o preço do Bitcoin?"
        - "Quais as últimas notícias sobre inteligência artificial?" (requer WebSearch)
        - "Quem ganhou a última Copa do Mundo?" (requer WebSearch)
        """)
        
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="Sua pergunta",
                    placeholder="Digite sua pergunta aqui...",
                    lines=3
                )
                show_reasoning = gr.Checkbox(
                    label="Mostrar raciocínio completo (ReAct steps)",
                    value=True
                )
                submit_btn = gr.Button("🚀 Executar", variant="primary")
            
            with gr.Column():
                output = gr.Markdown(label="Resposta")
        
        # Exemplos
        examples_list = [
            ["Quanto é 25 * 4 + 100?"],
            ["O que é ReAct?"],
            ["Qual o clima em Londres?"],
            ["Qual o preço do Ethereum?"],
            ["Calcule 15% de 3000 e me diga o resultado"],
        ]
        
        # Adiciona exemplos de WebSearch se estiver habilitada
        if websearch_enabled:
            examples_list.extend([
                ["Quais as últimas notícias sobre IA?"],
                ["Quem é o presidente do Brasil em 2024?"],
            ])
        
        gr.Examples(
            examples=examples_list,
            inputs=query_input
        )
        
        submit_btn.click(
            fn=process_query,
            inputs=[query_input, show_reasoning],
            outputs=output
        )
        
        gr.Markdown(f"""
        ---
        ### 📋 Status das Ferramentas
        - Calculator: ✅ Ativa
        - KnowledgeBase: ✅ Ativa
        - Weather: ✅ Ativa
        - CryptoPrice: ✅ Ativa
        - WebSearch: {"✅ Ativa" if websearch_enabled else "❌ Desabilitada (configure SERPAPI_KEY)"}
        
        ### 📝 Logs
        Os logs detalhados são salvos em `react_agent.log` para análise de LLMOps.
        
        ### 🔑 Configuração da SerpAPI
        Para habilitar a busca web:
        1. Crie uma conta gratuita em [serpapi.com](https://serpapi.com/users/sign_up)
        2. Copie sua API key
        3. Configure a variável de ambiente `SERPAPI_KEY`
        4. Reinicie a aplicação
        
        **Plano gratuito:** 100 buscas/mês
        """)
    
    return demo


# ============================================================================
# TESTES E DEMONSTRAÇÃO
# ============================================================================

def run_demo():
    """Executa demonstração do agente"""
    print("=" * 80)
    print("🤖 ReAct Assistant v2.0 - Demonstração")
    print("=" * 80)
    
    # Inicializa (você precisa configurar OPENAI_API_KEY)
    try:
        assistant = ReActAssistant()
        
        print(f"\n✅ Ferramentas disponíveis: {', '.join(assistant.get_available_tools())}")
        
        # Testes
        test_queries = [
            "Quanto é 15% de 2500?",
            "O que é LangChain?",
            "Qual o preço do Bitcoin?",
        ]
        
        # Adiciona teste de WebSearch se disponível
        if "WebSearch" in assistant.get_available_tools():
            test_queries.append("Quais as últimas notícias sobre inteligência artificial?")
        
        for query in test_queries:
            print(f"\n{'=' * 80}")
            print(f"📝 Query: {query}")
            print("=" * 80)
            
            result = assistant.run(query)
            print(assistant.explain_reasoning(result))
            print()
    
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Configure a variável de ambiente OPENAI_API_KEY para executar a demo")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        # Inicia interface Gradio
        demo = create_gradio_interface()

        demo.launch(share=True)
