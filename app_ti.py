import os
import json
import streamlit as st
from typing import List, Dict, Union
from datetime import datetime
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain.schema import SystemMessage

class GerenciadorProblemasTI:
    """Gerenciador de problemas comuns de TI"""
    
    def __init__(self):
        self.base_conhecimento = {
            "internet": {
                "sintomas": ["conexão lenta", "sem internet", "quedas frequentes"],
                "solucoes": [
                    "Reinicie o roteador",
                    "Verifique os cabos de rede",
                    "Teste com outro dispositivo"
                ]
            },
            "software": {
                "sintomas": ["programa não abre", "erro ao iniciar", "tela azul"],
                "solucoes": [
                    "Reinicie o computador",
                    "Verifique atualizações pendentes",
                    "Execute verificação de arquivos do sistema"
                ]
            },
            "hardware": {
                "sintomas": ["computador quebrou", "não liga", "desliga sozinho"],
                "solucoes": [
                    "Verifique se o computador está conectado à energia",
                    "Teste a fonte de alimentação",
                    "Verifique as conexões internas",
                    "Procure um técnico especializado"
                ]
            }
        }
        
        self.chamados = {}
    
    @tool("diagnosticar_problema")
    def diagnosticar_problema(self, descricao: str) -> str:
        """
        Diagnostica um problema de TI baseado na descrição fornecida.
        
        Args:
            descricao: Descrição do problema relatado
            
        Returns:
            str: Diagnóstico e possíveis soluções
        """
        descricao = descricao.lower()
        for categoria, dados in self.base_conhecimento.items():
            for sintoma in dados["sintomas"]:
                if sintoma in descricao:
                    solucoes = "\n".join(f"- {sol}" for sol in dados["solucoes"])
                    return f"""
                    Categoria identificada: {categoria}
                    Sintoma detectado: {sintoma}
                    
                    Soluções recomendadas:
                    {solucoes}
                    """
        return "Não foi possível identificar o problema específico. Por favor, forneça mais detalhes."

    @tool("registrar_chamado")
    def registrar_chamado(self, dados: str) -> str:
        """
        Registra um novo chamado de suporte.
        
        Args:
            dados: JSON string com descrição e prioridade do chamado
            
        Returns:
            str: Número do chamado registrado
        """
        try:
            info = json.loads(dados)
            numero_chamado = datetime.now().strftime("%Y%m%d%H%M%S")
            self.chamados[numero_chamado] = {
                "descricao": info["descricao"],
                "prioridade": info["prioridade"],
                "status": "aberto",
                "data_abertura": datetime.now().isoformat()
            }
            return f"Chamado {numero_chamado} registrado com sucesso!"
        except Exception as e:
            return f"Erro ao registrar chamado: {str(e)}"

def criar_agente_suporte(token_hf: str) -> AgentExecutor:
    """
    Cria e configura o agente de suporte técnico.
    
    Args:
        token_hf: Token de acesso do Hugging Face
        
    Returns:
        AgentExecutor: Agente configurado
    """
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = token_hf
    llm = HuggingFaceHub(
        repo_id="bigscience/bloom-560m",
        model_kwargs={
            "temperature": 0.7,
            "max_length": 1024
        }
    )
    
    gerenciador = GerenciadorProblemasTI()
    
    ferramentas = [
        Tool(
            name="DiagnosticarProblema",
            func=gerenciador.diagnosticar_problema,
            description="Analisa a descrição de um problema de TI e sugere soluções"
        ),
        Tool(
            name="RegistrarChamado",
            func=gerenciador.registrar_chamado,
            description="Registra um novo chamado de suporte técnico"
        )
    ]
    
    memoria = ConversationBufferMemory(
        memory_key="historico_chat",
        return_messages=True
    )
    
    template_prompt = """Você é um assistente de suporte técnico especializado em resolver problemas de TI.

Histórico da conversa:
{historico_chat}

Ferramentas disponíveis:
{tools}

Nomes das ferramentas disponíveis:
{tool_names}

Problema atual: {input}

Use o framework ReAct (Pensamento, Ação, Observação) para resolver o problema:
1. Pense sobre o problema
2. Escolha uma ação apropriada
3. Observe o resultado
4. Repita se necessário

{agent_scratchpad}
"""

    prompt = PromptTemplate(
        template=template_prompt,
        input_variables=["input", "historico_chat", "tools", "tool_names", "agent_scratchpad"]
    )
    
    agente = create_react_agent(
        llm=llm,
        tools=ferramentas,
        prompt=prompt
    )
    
    return AgentExecutor.from_agent_and_tools(
        agent=agente,
        tools=ferramentas,
        memory=memoria,
        verbose=True,
        handle_parsing_errors=True
    )

def main():
    """Função principal da aplicação Streamlit"""
    st.set_page_config(
        page_title="Assistente de Suporte TI",
        page_icon="🖥️",
        layout="wide"
    )
    
    st.title("🖥️ Assistente de Suporte TI")
    
    with st.sidebar:
        st.header("Configuração")
        token_hf = st.text_input(
            "Token Hugging Face",
            type="password",
            help="Insira seu token de acesso do Hugging Face"
        )
        
        if token_hf:
            st.session_state["token"] = token_hf
            st.success("✅ Token configurado!")
    
    if "token" not in st.session_state:
        st.warning("⚠️ Configure seu token do Hugging Face na barra lateral.")
        return
    
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
        st.session_state.mensagens.append({
            "papel": "sistema",
            "conteudo": "Olá! Sou seu assistente de suporte técnico. Como posso ajudar?"
        })
    
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["papel"]):
            st.write(msg["conteudo"])
    
    if pergunta := st.chat_input("Descreva seu problema..."):
        st.session_state.mensagens.append({
            "papel": "usuario",
            "conteudo": pergunta
        })
        
        with st.chat_message("usuario"):
            st.write(pergunta)
        
        try:
            if "agente" not in st.session_state:
                st.session_state.agente = criar_agente_suporte(st.session_state["token"])
            
            with st.spinner("Analisando seu problema..."):
                resposta = st.session_state.agente.invoke(
                    {"input": pergunta}
                ).get("output", "Desculpe, não consegui processar sua solicitação.")
            
            st.session_state.mensagens.append({
                "papel": "assistente",
                "conteudo": resposta
            })
            
            with st.chat_message("assistente"):
                st.write(resposta)
        
        except Exception as erro:
            st.error(f"❌ Erro no processamento: {str(erro)}")
            st.session_state.mensagens.append({
                "papel": "sistema",
                "conteudo": f"Ocorreu um erro: {str(erro)}"
            })

if __name__ == "__main__":
    main()
