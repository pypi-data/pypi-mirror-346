"""
Gerenciamento de agentes para a aplicação ConselhoFinanceiro.
Fornece decoradores e utilitários para registro e manipulação de agentes.
"""
from typing import List, Callable, Any
from functools import wraps
from agno.agent import Agent

class AgentManager:
    """
    Gerenciador de agentes que fornece funcionalidades para registrar,
    rastrear e organizar agentes em um sistema.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de agentes com uma lista vazia."""
        self.agents: List[Agent] = []
    
    def agent_decorator(self):
        """
        Cria um decorador para funções que retornam instâncias de Agent.
        O decorador registra cada agente criado na lista de agentes.
        
        Returns:
            Callable: Um decorador para funções que criam agentes.
        """
        def decorator(func: Callable[..., Agent]):
            @wraps(func)
            def wrapper(*args, **kwargs):
                agent_instance = func(*args, **kwargs)
                # Registra a instância do agente na lista se ainda não estiver presente
                if agent_instance not in self.agents:
                    self.agents.append(agent_instance)
                return agent_instance
            return wrapper
        return decorator
    
    def get_all_agents(self) -> List[Agent]:
        """
        Retorna todos os agentes registrados.
        
        Returns:
            List[Agent]: Lista de todos os agentes registrados.
        """
        return self.agents
    
    def clear(self):
        """Limpa a lista de agentes."""
        self.agents.clear() 