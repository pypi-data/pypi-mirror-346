"""
Módulo de registro e gerenciamento de agentes para a aplicação ConselhoFinanceiro.
Fornece um registry singleton para registrar e acessar agentes.
"""
from typing import Dict, List, Callable, Any, Optional, Set, Type
from functools import wraps
import inspect
from agno.agent import Agent
from agno.team import Team

# Dicionário para armazenar métodos de agente por classe
_agent_methods: Dict[Type, List[str]] = {}

class AgentMethod:
    """
    Classe que armazena uma referência ao método do agente e ao agente resultante.
    Permite representação no formato self.method_name().
    """
    def __init__(self, instance, method_name, agent_instance):
        self.instance = instance
        self.method_name = method_name
        self.agent_instance = agent_instance
    
    def __repr__(self):
        """Representação no formato self.method_name()"""
        return f"self.{self.method_name}()"
    
    def __str__(self):
        """Representação no formato self.method_name()"""
        return self.__repr__()
    
    def get_agent(self):
        """Retorna a instância do agente"""
        return self.agent_instance

class AgentMethodList(list):
    """
    Lista personalizada para armazenar objetos AgentMethod.
    Permite representação no formato [self.method1(), self.method2()].
    Pode ser usada diretamente como uma lista de agentes em Team(members=self.agents).
    """
    def __repr__(self):
        """Representação no formato [self.method1(), self.method2()]"""
        return f"[{', '.join(str(item) for item in self)}]"
    
    def __str__(self):
        """Representação no formato [self.method1(), self.method2()]"""
        return self.__repr__()
    
    def get_agents(self):
        """Retorna uma lista com todas as instâncias de agentes"""
        return [agent_method.get_agent() for agent_method in self]
    
    # Métodos mágicos para fazer a classe se comportar como uma lista de agentes
    def __iter__(self):
        """Permite iterar diretamente sobre os agentes reais, não sobre os AgentMethod"""
        for agent_method in super().__iter__():
            yield agent_method.get_agent()
    
    def __getitem__(self, index):
        """Permite acessar agentes reais por índice, não os AgentMethod"""
        if isinstance(index, slice):
            # Se for um slice, retorna uma lista de agentes para esse slice
            agent_methods = super().__getitem__(index)
            return [am.get_agent() for am in agent_methods]
        # Se for um índice único, retorna o agente diretamente
        return super().__getitem__(index).get_agent()
    
    def __len__(self):
        """Retorna o número de agentes na lista"""
        return super().__len__()
        
    # Sobrescreve o método especial para imprimir o objeto como string
    def __format__(self, format_spec):
        """Formata a lista para exibição como string, independente do contexto"""
        return self.__repr__()
    
    # Garantir que a representação seja usada em todos os contextos
    def __eq__(self, other):
        """Compara se as representações são iguais"""
        if isinstance(other, str):
            return str(self) == other
        return super().__eq__(other)

class AgentRegistry:
    """
    Singleton para registro e gerenciamento de agentes.
    Permite que agentes sejam armazenados e acessados de forma centralizada.
    """
    _instance = None
    _is_first_use = True
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._agents = []
            cls._instance._agent_names = set()  # Conjunto para rastrear nomes únicos
        return cls._instance
    
    def register(self, agent: Agent) -> Agent:
        """
        Registra um agente no registry.
        
        Args:
            agent (Agent): O agente a ser registrado
            
        Returns:
            Agent: O mesmo agente, para permitir encadeamento
        """
        # Verifica se o agente tem um nome definido
        if not hasattr(agent, 'name') or not agent.name:
            raise ValueError("O agente deve ter um nome definido")
            
        # Verifica se já existe um agente com o mesmo nome
        if agent.name in self._instance._agent_names:
            print(f"Aviso: Já existe um agente registrado com o nome '{agent.name}', atualizando o registro.")
            # Encontrar e remover o agente anterior com o mesmo nome
            for i, existing_agent in enumerate(self._instance._agents):
                if existing_agent.name == agent.name:
                    self._instance._agents.pop(i)
                    break
            
        # Registra o nome do agente
        self._instance._agent_names.add(agent.name)
        
        # Registra o agente
        if agent not in self._instance._agents:
            self._instance._agents.append(agent)
        
        print(f"Agente '{agent.name}' registrado com sucesso.")
        return agent
    
    def get_all(self) -> List[Agent]:
        """
        Retorna todos os agentes registrados.
        
        Returns:
            List[Agent]: Lista de todos os agentes registrados
        """
        return self._instance._agents
    
    def clear(self) -> None:
        """Limpa todos os agentes registrados."""
        self._instance._agents.clear()
        self._instance._agent_names.clear()  # Limpa também o conjunto de nomes
        print("Registro de agentes limpo.")

# Conjunto para rastrear as classes que já usaram o decorador
_decorated_classes: Set = set()

# Decorador global para registro de agentes
def agent(func: Callable[..., Agent]) -> Callable[..., Agent]:
    """
    Decorador para registrar funções que criam agentes.
    A função decorada registrará automaticamente o agente criado no AgentRegistry.
    
    - Limpa automaticamente o registro na primeira vez que é usado em uma classe
    - Registra o agente no registry global
    - Registra o método na lista de métodos de agente da classe
    
    Args:
        func (Callable[..., Agent]): Função que cria um agente
        
    Returns:
        Callable[..., Agent]: Wrapper que registra o agente no registry
    """
    # Obter o nome qualificado do método
    func_name = func.__name__
    
    # Marcar a função original como um método de agente
    func._is_agent_method = True
    
    # Registrar o nome do método para a classe (isso é feito em tempo de decoração)
    @wraps(func)
    def wrapper(*args, **kwargs) -> Agent:
        # Se for chamado como método de classe, args[0] é a instância (self)
        if args and hasattr(args[0], "__class__"):
            instance = args[0]
            cls = instance.__class__
            
            # Registra o método na lista de métodos de agente da classe, se ainda não estiver lá
            if cls not in _agent_methods:
                _agent_methods[cls] = []
            if func_name not in _agent_methods[cls]:
                _agent_methods[cls].append(func_name)
                print(f"Método '{func_name}' registrado para a classe {cls.__name__}")
            
            # Limpa o registro na primeira vez que qualquer método decorado é chamado para esta classe
            if cls not in _decorated_classes:
                print(f"Primeira chamada para a classe {cls.__name__}, limpando registro de agentes")
                AgentRegistry().clear()
                _decorated_classes.add(cls)
        
        print(f"Chamando método de agente: {func_name}")
        agent_instance = func(*args, **kwargs)
        # Registra o agente no registry
        AgentRegistry().register(agent_instance)
        return agent_instance
    
    # Marcar o wrapper para identificá-lo posteriormente
    wrapper._is_agent_method = True
    return wrapper

def initialize_agents(instance) -> AgentMethodList:
    """
    Inicializa todos os agentes registrados para uma instância.
    Retorna uma lista especializada que se representa como [self.finance_agent(), self.other_agent(), etc.]
    mas internamente contém referências aos métodos e às instâncias de agentes.
    
    Args:
        instance: A instância da classe que contém métodos decorados com @agent
        
    Returns:
        AgentMethodList: Lista especializada de métodos de agente e suas instâncias
    """
    cls = instance.__class__
    print(f"Inicializando agentes para a classe {cls.__name__}")
    
    # Limpa o registry na primeira inicialização
    if cls not in _decorated_classes:
        print(f"Primeira inicialização para a classe {cls.__name__}, limpando registro")
        AgentRegistry().clear()
        _decorated_classes.add(cls)
    
    # Se não houver métodos registrados, tenta encontrar todos os métodos decorados com @agent
    if cls not in _agent_methods:
        _agent_methods[cls] = []
        print(f"Procurando métodos decorados com @agent na classe {cls.__name__}")
        for name, method in inspect.getmembers(instance, inspect.ismethod):
            if hasattr(method, '_is_agent_method') or hasattr(method.__func__, '_is_agent_method'):
                print(f"Encontrado método decorado: {name}")
                _agent_methods[cls].append(name)
    
    # Chama os métodos para inicializar os agentes
    print(f"Métodos de agente encontrados: {_agent_methods.get(cls, [])}")
    
    # Lista especializada de agentes inicializados
    agent_methods = AgentMethodList()
    for method_name in _agent_methods.get(cls, []):
        # Obtém a referência para o método
        method = getattr(instance, method_name)
        # Chama o método para inicializar o agente
        print(f"Inicializando agente através do método: {method_name}")
        agent_instance = method()
        # Cria um objeto AgentMethod que guarda referência ao método e à instância
        agent_method = AgentMethod(instance, method_name, agent_instance)
        agent_methods.append(agent_method)
    
    # Use a representação formatada para o console
    formatted_repr = f"[{', '.join(f'self.{method_name}()' for method_name in _agent_methods.get(cls, []))}]"
    print(f"Agentes inicializados: {formatted_repr}")
    return agent_methods

# Lista de agentes - pode ser usada diretamente como membros de um Team
def agents(instance=None):
    """
    Retorna a lista de agentes registrados.
    
    Args:
        instance: Instância opcional da classe decorada com @OrNexusConfig
        
    Returns:
        List[Agent] ou AgentMethodList: Lista de agentes registrados ou AgentMethodList
          que se comporta como uma lista de agentes
    """
    if instance and hasattr(instance, 'agents'):
        # Retorna diretamente o agents, que agora pode ser usado como lista de agentes
        return instance.agents
    
    registered_agents = AgentRegistry().get_all()
    print(f"Obtendo agentes registrados: {registered_agents}")
    return registered_agents

# Atribui funções e propriedades ao decorador para maior conveniência
agent.registry = AgentRegistry()
agent.get_agents = agents
agent.clear = AgentRegistry().clear
agent.initialize_all = initialize_agents 