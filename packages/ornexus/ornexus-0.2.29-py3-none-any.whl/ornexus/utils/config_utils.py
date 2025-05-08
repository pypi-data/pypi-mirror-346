"""
Utilitários para gerenciamento de configuração e validação para a aplicação ConselhoFinanceiro.
Fornece um decorador de classe OrNexusConfig para configuração automática.
"""
from typing import Dict, Any, Set, List, Optional, Callable, TypeVar, Type, Union
from pathlib import Path
import yaml
import re
import os
from dotenv import load_dotenv
from agno.team import Team
from functools import wraps
import functools
import inspect

# Importação circular - importamos aqui diretamente do módulo
from .agent_registry import agent, agents, initialize_agents

T = TypeVar('T')

def _extract_placeholders(text: str) -> Set[str]:
    """
    Extrai placeholders no formato {placeholder}, ignorando {{placeholder}}.
    
    Args:
        text: O texto a ser analisado
        
    Returns:
        Set[str]: Um conjunto de placeholders encontrados
    """
    all_matches = re.finditer(r'(?<!{){([^{}]+)}(?!})', text)
    return set(match.group(1) for match in all_matches)

def _find_all_placeholders(data: Any) -> Set[str]:
    """
    Encontra todos os placeholders em uma estrutura de dados complexa.
    
    Args:
        data: Os dados a serem analisados (string, dict, list, etc.)
        
    Returns:
        Set[str]: Um conjunto de todos os placeholders encontrados
    """
    required_placeholders = set()
    
    def find_placeholders(data: Any) -> None:
        if isinstance(data, str):
            required_placeholders.update(_extract_placeholders(data))
        elif isinstance(data, dict):
            for value in data.values():
                find_placeholders(value)
        elif isinstance(data, list):
            for item in data:
                find_placeholders(item)
    
    find_placeholders(data)
    return required_placeholders

def _validate_inputs(required_inputs: Set[str], provided_inputs: Dict[str, Any]) -> List[str]:
    """
    Valida se todos os inputs necessários foram fornecidos.
    
    Args:
        required_inputs: Conjunto de inputs necessários
        provided_inputs: Dicionário de inputs fornecidos
        
    Returns:
        List[str]: Lista de inputs que faltam, vazia se todos foram fornecidos
    """
    missing_inputs = required_inputs - set(provided_inputs.keys())
    return list(missing_inputs)

async def _run_with_validation(team_instance, required_inputs: Set[str], **kwargs) -> Dict[str, Any]:
    """
    Executa uma operação após validar os inputs necessários.
    
    Args:
        team_instance: Instância do Team a ser executada
        required_inputs: Conjunto de inputs necessários
        **kwargs: Inputs fornecidos
        
    Returns:
        Dict[str, Any]: O resultado da operação
        
    Raises:
        ValueError: Se faltarem inputs necessários
        RuntimeError: Se ocorrer um erro durante a execução
    """
    try:
        missing_inputs = _validate_inputs(required_inputs, kwargs)
        if missing_inputs:
            raise ValueError(
                f"Faltam os seguintes parâmetros obrigatórios: {', '.join(missing_inputs)}\n"
                f"Parâmetros necessários: {', '.join(required_inputs)}"
            )
        # Convertendo para string formatada para entrada do modelo
        input_data = str(kwargs)
        
        # O Team.run retorna um TeamRunResponse, que não é um awaitable
        # Usamos como objeto diretamente
        try:
            # Executamos o Team e capturamos o resultado
            team_response = team_instance.run(input_data)
            # Verificamos o tipo de resposta e formatamos adequadamente
            if hasattr(team_response, 'messages'):
                # Extrai a última mensagem se disponível
                response_text = team_response.messages[-1].content if team_response.messages else str(team_response)
                return response_text
            else:
                # Retorna o objeto como string se não for possível extrair a mensagem
                return str(team_response)
        except Exception as e:
            raise RuntimeError(f"Erro ao executar o Team: {str(e)}")
            
    except ValueError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Erro ao executar análise financeira: {e}")

def _load_config(config_path: Path) -> Dict[str, Any]:
    """
    Carrega e valida o arquivo de configuração.
    
    Args:
        config_path: O caminho para o arquivo de configuração
        
    Returns:
        Dict[str, Any]: A configuração carregada
        
    Raises:
        ValueError: Se houver um erro ao carregar o arquivo de configuração
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"Erro ao carregar arquivo de configuração: {e}")

def OrNexusConfig(cls_or_config_path=None, *, use_legacy_config=False):
    """
    Decorador de classe para configuração OrNexus.
    
    Carrega configurações dos arquivos YAML e inicializa agentes automaticamente.
    Por padrão, tenta carregar 'agents.yaml' e 'tasks.yaml' da pasta config.
    Se esses arquivos não existirem, usa 'config.yaml' como fallback.
    
    Pode ser usado de duas formas:
    - @OrNexusConfig - sem argumentos, usa o método padrão (agents.yaml + tasks.yaml)
    - @OrNexusConfig(config_path='caminho/para/config.yaml') - com parâmetros nomeados
    - @OrNexusConfig(use_legacy_config=True) - força uso de config.yaml
    
    Args:
        cls_or_config_path: Classe a ser decorada ou parâmetros para o decorador
        use_legacy_config: Se True, força o uso de config.yaml ao invés de arquivos separados
        
    Returns:
        A classe decorada ou uma função que decora a classe
    """
    # Captura o valor de use_legacy_config em uma variável de escopo externo
    legacy_config = use_legacy_config
    
    # Se é chamado como função sem parênteses (recebe a classe diretamente)
    if cls_or_config_path is not None and isinstance(cls_or_config_path, type):
        cls = cls_or_config_path
        config_path = None
        
        # Função interna para decorar a classe
        def wrap_class():
            # Salva a referência ao método __init__ original
            original_init = cls.__init__
            
            # Define um novo __init__ que carrega a configuração
            @functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                # Importação da classe Agent aqui para evitar problemas de importação circular
                from agno.agent import Agent
                # Importação de AgentRegistry para uso dentro da função
                from .agent_registry import AgentRegistry, agent, agents, initialize_agents
                
                # Salva a referência ao método __repr__ original da classe Agent
                original_agent_repr = Agent.__repr__
                
                # Define um método customizado para Agent.__repr__
                def custom_agent_repr(agent):
                    """Representação personalizada para debug: self.method_name()"""
                    return f"self.finance_agent()"
                
                # Aplica a sobrescrita do método __repr__ da classe Agent
                Agent.__repr__ = custom_agent_repr
                
                # Determina o caminho da configuração
                if config_path is None:
                    # Tenta encontrar os arquivos de configuração no mesmo diretório que o módulo da classe
                    module_path = inspect.getmodule(cls).__file__
                    module_dir = os.path.dirname(module_path)
                    
                    agents_file_path = os.path.join(module_dir, "config", "agents.yaml")
                    tasks_file_path = os.path.join(module_dir, "config", "tasks.yaml")
                    config_file_path = os.path.join(module_dir, "config", "config.yaml")
                else:
                    # Se um caminho específico foi fornecido, usamos apenas config.yaml
                    config_file_path = config_path
                    agents_file_path = None
                    tasks_file_path = None
                
                # Inicializa os atributos de configuração
                self.config_agents = {}
                self.config_tasks = {}
                
                # Verifica se deve usar config.yaml diretamente
                if legacy_config:
                    print(f"Usando configuração legacy: {config_file_path}")
                    if os.path.exists(config_file_path):
                        with open(config_file_path, "r") as f:
                            self.config = yaml.safe_load(f)
                            # Para manter compatibilidade, usamos o mesmo dicionário para agents e tasks
                            self.config_agents = self.config
                            self.config_tasks = self.config
                    else:
                        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_file_path}")
                else:
                    # Tenta carregar os arquivos separados (método prioritário)
                    agents_exists = os.path.exists(agents_file_path)
                    tasks_exists = os.path.exists(tasks_file_path)
                    
                    if agents_exists and tasks_exists:
                        print(f"Usando configuração dividida: {agents_file_path} e {tasks_file_path}")
                        # Carrega os agentes
                        with open(agents_file_path, "r") as f:
                            self.config_agents = yaml.safe_load(f)
                        
                        # Carrega as tarefas
                        with open(tasks_file_path, "r") as f:
                            self.config_tasks = yaml.safe_load(f)
                        
                        # Mescla as configurações em um único dicionário para compatibilidade
                        self.config = {**self.config_agents, **self.config_tasks}
                    else:
                        # Fallback para config.yaml se os arquivos separados não existirem
                        print(f"Arquivos divididos não encontrados. Usando configuração legacy: {config_file_path}")
                        if os.path.exists(config_file_path):
                            with open(config_file_path, "r") as f:
                                self.config = yaml.safe_load(f)
                                # Para manter compatibilidade, usamos o mesmo dicionário para agents e tasks
                                self.config_agents = self.config
                                self.config_tasks = self.config
                        else:
                            # Se nenhum dos métodos de configuração estiver disponível
                            raise FileNotFoundError("Nenhum arquivo de configuração encontrado. Esperava-se agents.yaml e tasks.yaml, ou config.yaml.")
                
                # Identifica os placeholders necessários (apenas os simples {placeholder})
                placeholders = set()
                
                def find_placeholders(obj, path=""):
                    """
                    Encontra placeholders no formato {placeholder}, ignorando os placeholders no formato {{placeholder}}
                    """
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            find_placeholders(v, f"{path}.{k}" if path else k)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            find_placeholders(item, f"{path}[{i}]")
                    elif isinstance(obj, str):
                        # Regex para encontrar {placeholder} mas não {{placeholder}}
                        # O padrão procura por chaves que não são imediatamente precedidas ou seguidas por outra chave
                        import re
                        matches = re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", obj)
                        for match in matches:
                            placeholders.add(match)
                
                # Encontra placeholders em todos os dicionários de configuração
                find_placeholders(self.config)
                print(f"Placeholders identificados: {placeholders}")
                
                # Função para interpolar os valores de self.config com valores de um dicionário
                def interpolate_config(config, values):
                    """
                    Interpola os placeholders {placeholder} no config com os valores do dicionário values.
                    Os placeholders {{placeholder}} são preservados.
                    
                    Args:
                        config: A configuração a ser interpolada (dict, list ou string)
                        values: Dicionário com os valores para interpolação
                        
                    Returns:
                        A configuração com os placeholders substituídos
                    """
                    if isinstance(config, dict):
                        return {k: interpolate_config(v, values) for k, v in config.items()}
                    elif isinstance(config, list):
                        return [interpolate_config(item, values) for item in config]
                    elif isinstance(config, str):
                        # Interpola apenas os placeholders simples {placeholder}
                        import re
                        
                        def replace_placeholder(match):
                            placeholder = match.group(1)
                            if placeholder in values:
                                return str(values[placeholder])
                            return match.group(0)  # Mantém o placeholder se o valor não for encontrado
                        
                        # Substitui {placeholder} mas não {{placeholder}}
                        return re.sub(r"(?<!\{)\{([^{}]+)\}(?!\})", replace_placeholder, config)
                    else:
                        return config
                
                # Adiciona o método de interpolação à instância para uso posterior
                self.interpolate_config = interpolate_config
                
                # Armazena os placeholders identificados
                self.placeholders = placeholders
                
                # Limpa o registro de agentes existente
                AgentRegistry().clear()
                
                # Chama o construtor original
                original_init(self, *args, **kwargs)
                
                # Inicializa os agentes automaticamente
                initialized_agents = initialize_agents(self)
                
                # Armazena os agentes inicializados como atributo da classe
                self._initialized_agents = initialized_agents
                
                # Adiciona acesso direto aos agentes inicializados
                self.agents = initialized_agents
                
                print(f"Agentes inicializados automaticamente: {self.agents}")
                
                # Método para restaurar a representação original da classe Agent
                def restore_agent_repr():
                    """Restaura o método __repr__ original da classe Agent"""
                    Agent.__repr__ = original_agent_repr
                
                # Armazena o método para restaurar o __repr__ original
                self._restore_agent_repr = restore_agent_repr
            
            # Substitui o __init__ da classe
            cls.__init__ = new_init
            
            # Define um método para destruir a instância e restaurar o método __repr__ original
            original_del = getattr(cls, '__del__', lambda self: None)
            
            @functools.wraps(original_del)
            def new_del(self):
                # Restaura o método __repr__ original da classe Agent
                if hasattr(self, '_restore_agent_repr'):
                    self._restore_agent_repr()
                
                # Chama o método __del__ original
                original_del(self)
            
            # Substitui o método __del__ da classe
            cls.__del__ = new_del
            
            # Adiciona acesso ao decorador agent como atributo de classe
            cls.agent = agent
            
            # Mantém a referência para o método agents para acesso aos agentes registrados
            cls.get_agents = agents
            
            # Adicionamos um método à classe para permitir a interpolação de valores
            def run(self, inputs=None, **kwargs):
                """
                Executa o time com os inputs fornecidos, interpolando os valores da configuração.
                
                Args:
                    inputs: String ou dicionário com os inputs
                    **kwargs: Argumentos adicionais para passar para o método run do time
                    
                Returns:
                    O resultado da execução do time
                """
                # Converte os inputs para um dicionário, se fornecido
                inputs_dict = {}
                if inputs:
                    if isinstance(inputs, str):
                        # Se for uma string, tenta converter para dicionário
                        try:
                            # Tenta como JSON
                            import json
                            inputs_dict = json.loads(inputs)
                        except json.JSONDecodeError:
                            # Tenta como literal Python
                            import ast
                            try:
                                inputs_dict = ast.literal_eval(inputs)
                            except (ValueError, SyntaxError):
                                # Se falhar na conversão, provavemente não é um formato válido
                                print(f"Aviso: Não foi possível converter inputs para dicionário: {inputs}")
                    elif isinstance(inputs, dict):
                        # Se já for um dicionário, usa diretamente
                        inputs_dict = inputs
                
                # Interpola os valores em todas as configurações
                if inputs_dict and hasattr(self, 'interpolate_config'):
                    print(f"Interpolando configuração com valores: {inputs_dict}")
                    self.config = self.interpolate_config(self.config, inputs_dict)
                    self.config_agents = self.interpolate_config(self.config_agents, inputs_dict)
                    self.config_tasks = self.interpolate_config(self.config_tasks, inputs_dict)
                
                # Executa o time - converte o dicionário para string para o formato esperado pelo Team.run()
                import json
                team_instance = self.team()
                
                # Se tivermos inputs em formato de dicionário, converte para string
                inputs_str = json.dumps(inputs_dict) if inputs_dict else None
                
                print(f"Executando time com inputs: {inputs_str}")
                return team_instance.run(inputs_str, **kwargs)
            
            # Adicionamos o método assíncrono para permitir execução não-bloqueante
            async def kickoff(self, inputs=None, **kwargs):
                """
                Executa o time de forma assíncrona com os inputs fornecidos, interpolando os valores da configuração.
                
                Args:
                    inputs: String ou dicionário com os inputs
                    **kwargs: Argumentos adicionais para passar para o método arun do time
                    
                Returns:
                    O resultado da execução assíncrona do time
                """
                # Converte os inputs para um dicionário, se fornecido
                inputs_dict = {}
                if inputs:
                    if isinstance(inputs, str):
                        # Se for uma string, tenta converter para dicionário
                        try:
                            # Tenta como JSON
                            import json
                            inputs_dict = json.loads(inputs)
                        except json.JSONDecodeError:
                            # Tenta como literal Python
                            import ast
                            try:
                                inputs_dict = ast.literal_eval(inputs)
                            except (ValueError, SyntaxError):
                                # Se falhar na conversão, provavemente não é um formato válido
                                print(f"Aviso: Não foi possível converter inputs para dicionário: {inputs}")
                    elif isinstance(inputs, dict):
                        # Se já for um dicionário, usa diretamente
                        inputs_dict = inputs
                
                # Interpola os valores em todas as configurações
                if inputs_dict and hasattr(self, 'interpolate_config'):
                    print(f"Interpolando configuração com valores: {inputs_dict}")
                    self.config = self.interpolate_config(self.config, inputs_dict)
                    self.config_agents = self.interpolate_config(self.config_agents, inputs_dict)
                    self.config_tasks = self.interpolate_config(self.config_tasks, inputs_dict)
                
                # Executa o time de forma assíncrona - converte o dicionário para string para o formato esperado pelo Team.arun()
                import json
                team_instance = self.team()
                
                # Se tivermos inputs em formato de dicionário, converte para string
                inputs_str = json.dumps(inputs_dict) if inputs_dict else None
                
                print(f"Executando time de forma assíncrona com inputs: {inputs_str}")
                return await team_instance.print_response(inputs_str, **kwargs)
            
            # Substitui o método run e arun da classe com nossas versões modificadas
            cls.run = run
            cls.kickoff = kickoff
            
            return cls
        
        return wrap_class()
    
    # Se é chamado como função com parâmetros (sem receber a classe ainda)
    def decorator(cls):
        nonlocal cls_or_config_path
        config_path = cls_or_config_path
        
        # Salva a referência ao método __init__ original
        original_init = cls.__init__
        
        # Define um novo __init__ que carrega a configuração
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            # Importação da classe Agent aqui para evitar problemas de importação circular
            from agno.agent import Agent
            # Importação de AgentRegistry para uso dentro da função
            from .agent_registry import AgentRegistry, agent, agents, initialize_agents
            
            # Salva a referência ao método __repr__ original da classe Agent
            original_agent_repr = Agent.__repr__
            
            # Define um método customizado para Agent.__repr__
            def custom_agent_repr(agent):
                """Representação personalizada para debug: self.method_name()"""
                return f"self.finance_agent()"
            
            # Aplica a sobrescrita do método __repr__ da classe Agent
            Agent.__repr__ = custom_agent_repr
            
            # Determina o caminho da configuração
            if config_path is None:
                # Tenta encontrar os arquivos de configuração no mesmo diretório que o módulo da classe
                module_path = inspect.getmodule(cls).__file__
                module_dir = os.path.dirname(module_path)
                
                agents_file_path = os.path.join(module_dir, "config", "agents.yaml")
                tasks_file_path = os.path.join(module_dir, "config", "tasks.yaml")
                config_file_path = os.path.join(module_dir, "config", "config.yaml")
            else:
                # Se um caminho específico foi fornecido, usamos apenas config.yaml
                config_file_path = config_path
                agents_file_path = None
                tasks_file_path = None
            
            # Inicializa os atributos de configuração
            self.config_agents = {}
            self.config_tasks = {}
            
            # Verifica se deve usar config.yaml diretamente
            if legacy_config:
                print(f"Usando configuração legacy: {config_file_path}")
                if os.path.exists(config_file_path):
                    with open(config_file_path, "r") as f:
                        self.config = yaml.safe_load(f)
                        # Para manter compatibilidade, usamos o mesmo dicionário para agents e tasks
                        self.config_agents = self.config
                        self.config_tasks = self.config
                else:
                    raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_file_path}")
            else:
                # Tenta carregar os arquivos separados (método prioritário)
                agents_exists = os.path.exists(agents_file_path)
                tasks_exists = os.path.exists(tasks_file_path)
                
                if agents_exists and tasks_exists:
                    print(f"Usando configuração dividida: {agents_file_path} e {tasks_file_path}")
                    # Carrega os agentes
                    with open(agents_file_path, "r") as f:
                        self.config_agents = yaml.safe_load(f)
                    
                    # Carrega as tarefas
                    with open(tasks_file_path, "r") as f:
                        self.config_tasks = yaml.safe_load(f)
                    
                    # Mescla as configurações em um único dicionário para compatibilidade
                    self.config = {**self.config_agents, **self.config_tasks}
                else:
                    # Fallback para config.yaml se os arquivos separados não existirem
                    print(f"Arquivos divididos não encontrados. Usando configuração legacy: {config_file_path}")
                    if os.path.exists(config_file_path):
                        with open(config_file_path, "r") as f:
                            self.config = yaml.safe_load(f)
                            # Para manter compatibilidade, usamos o mesmo dicionário para agents e tasks
                            self.config_agents = self.config
                            self.config_tasks = self.config
                    else:
                        # Se nenhum dos métodos de configuração estiver disponível
                        raise FileNotFoundError("Nenhum arquivo de configuração encontrado. Esperava-se agents.yaml e tasks.yaml, ou config.yaml.")
            
            # Identifica os placeholders necessários (apenas os simples {placeholder})
            placeholders = set()
            
            def find_placeholders(obj, path=""):
                """
                Encontra placeholders no formato {placeholder}, ignorando os placeholders no formato {{placeholder}}
                """
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        find_placeholders(v, f"{path}.{k}" if path else k)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        find_placeholders(item, f"{path}[{i}]")
                elif isinstance(obj, str):
                    # Regex para encontrar {placeholder} mas não {{placeholder}}
                    # O padrão procura por chaves que não são imediatamente precedidas ou seguidas por outra chave
                    import re
                    matches = re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", obj)
                    for match in matches:
                        placeholders.add(match)
            
            # Encontra placeholders em todos os dicionários de configuração
            find_placeholders(self.config)
            print(f"Placeholders identificados: {placeholders}")
            
            # Função para interpolar os valores de self.config com valores de um dicionário
            def interpolate_config(config, values):
                """
                Interpola os placeholders {placeholder} no config com os valores do dicionário values.
                Os placeholders {{placeholder}} são preservados.
                
                Args:
                    config: A configuração a ser interpolada (dict, list ou string)
                    values: Dicionário com os valores para interpolação
                    
                Returns:
                    A configuração com os placeholders substituídos
                """
                if isinstance(config, dict):
                    return {k: interpolate_config(v, values) for k, v in config.items()}
                elif isinstance(config, list):
                    return [interpolate_config(item, values) for item in config]
                elif isinstance(config, str):
                    # Interpola apenas os placeholders simples {placeholder}
                    import re
                    
                    def replace_placeholder(match):
                        placeholder = match.group(1)
                        if placeholder in values:
                            return str(values[placeholder])
                        return match.group(0)  # Mantém o placeholder se o valor não for encontrado
                    
                    # Substitui {placeholder} mas não {{placeholder}}
                    return re.sub(r"(?<!\{)\{([^{}]+)\}(?!\})", replace_placeholder, config)
                else:
                    return config
            
            # Adiciona o método de interpolação à instância para uso posterior
            self.interpolate_config = interpolate_config
            
            # Armazena os placeholders identificados
            self.placeholders = placeholders
            
            # Limpa o registro de agentes existente
            AgentRegistry().clear()
            
            # Chama o construtor original
            original_init(self, *args, **kwargs)
            
            # Inicializa os agentes automaticamente
            initialized_agents = initialize_agents(self)
            
            # Armazena os agentes inicializados como atributo da classe
            self._initialized_agents = initialized_agents
            
            # Adiciona acesso direto aos agentes inicializados
            self.agents = initialized_agents
            
            print(f"Agentes inicializados automaticamente: {self.agents}")
            
            # Método para restaurar a representação original da classe Agent
            def restore_agent_repr():
                """Restaura o método __repr__ original da classe Agent"""
                Agent.__repr__ = original_agent_repr
            
            # Armazena o método para restaurar o __repr__ original
            self._restore_agent_repr = restore_agent_repr
        
        # Substitui o __init__ da classe
        cls.__init__ = new_init
        
        # Define um método para destruir a instância e restaurar o método __repr__ original
        original_del = getattr(cls, '__del__', lambda self: None)
        
        @functools.wraps(original_del)
        def new_del(self):
            # Restaura o método __repr__ original da classe Agent
            if hasattr(self, '_restore_agent_repr'):
                self._restore_agent_repr()
            
            # Chama o método __del__ original
            original_del(self)
        
        # Substitui o método __del__ da classe
        cls.__del__ = new_del
        
        # Adiciona acesso ao decorador agent como atributo de classe
        cls.agent = agent
        
        # Mantém a referência para o método agents para acesso aos agentes registrados
        cls.get_agents = agents
        
        # Adicionamos um método à classe para permitir a interpolação de valores
        def run(self, inputs=None, **kwargs):
            """
            Executa o time com os inputs fornecidos, interpolando os valores da configuração.
            
            Args:
                inputs: String ou dicionário com os inputs
                **kwargs: Argumentos adicionais para passar para o método run do time
                
            Returns:
                O resultado da execução do time
            """
            # Converte os inputs para um dicionário, se fornecido
            inputs_dict = {}
            if inputs:
                if isinstance(inputs, str):
                    # Se for uma string, tenta converter para dicionário
                    try:
                        # Tenta como JSON
                        import json
                        inputs_dict = json.loads(inputs)
                    except json.JSONDecodeError:
                        # Tenta como literal Python
                        import ast
                        try:
                            inputs_dict = ast.literal_eval(inputs)
                        except (ValueError, SyntaxError):
                            # Se falhar na conversão, provavemente não é um formato válido
                            print(f"Aviso: Não foi possível converter inputs para dicionário: {inputs}")
                elif isinstance(inputs, dict):
                    # Se já for um dicionário, usa diretamente
                    inputs_dict = inputs
            
            # Interpola os valores em todas as configurações
            if inputs_dict and hasattr(self, 'interpolate_config'):
                print(f"Interpolando configuração com valores: {inputs_dict}")
                self.config = self.interpolate_config(self.config, inputs_dict)
                self.config_agents = self.interpolate_config(self.config_agents, inputs_dict)
                self.config_tasks = self.interpolate_config(self.config_tasks, inputs_dict)
            
            # Executa o time - converte o dicionário para string para o formato esperado pelo Team.run()
            import json
            team_instance = self.team()
            
            # Se tivermos inputs em formato de dicionário, converte para string
            inputs_str = json.dumps(inputs_dict) if inputs_dict else None
            
            print(f"Executando time com inputs: {inputs_str}")
            return team_instance.run(inputs_str, **kwargs)
        
        # Adicionamos o método assíncrono para permitir execução não-bloqueante
        async def kickoff(self, inputs=None, **kwargs):
            """
            Executa o time de forma assíncrona com os inputs fornecidos, interpolando os valores da configuração.
            
            Args:
                inputs: String ou dicionário com os inputs
                **kwargs: Argumentos adicionais para passar para o método arun do time
                
            Returns:
                O resultado da execução assíncrona do time
            """
            # Converte os inputs para um dicionário, se fornecido
            inputs_dict = {}
            if inputs:
                if isinstance(inputs, str):
                    # Se for uma string, tenta converter para dicionário
                    try:
                        # Tenta como JSON
                        import json
                        inputs_dict = json.loads(inputs)
                    except json.JSONDecodeError:
                        # Tenta como literal Python
                        import ast
                        try:
                            inputs_dict = ast.literal_eval(inputs)
                        except (ValueError, SyntaxError):
                            # Se falhar na conversão, provavemente não é um formato válido
                            print(f"Aviso: Não foi possível converter inputs para dicionário: {inputs}")
                elif isinstance(inputs, dict):
                    # Se já for um dicionário, usa diretamente
                    inputs_dict = inputs
            
            # Interpola os valores em todas as configurações
            if inputs_dict and hasattr(self, 'interpolate_config'):
                print(f"Interpolando configuração com valores: {inputs_dict}")
                self.config = self.interpolate_config(self.config, inputs_dict)
                self.config_agents = self.interpolate_config(self.config_agents, inputs_dict)
                self.config_tasks = self.interpolate_config(self.config_tasks, inputs_dict)
            
            # Executa o time de forma assíncrona - converte o dicionário para string para o formato esperado pelo Team.arun()
            import json
            team_instance = self.team()
            
            # Se tivermos inputs em formato de dicionário, converte para string
            inputs_str = json.dumps(inputs_dict) if inputs_dict else None
            
            print(f"Executando time de forma assíncrona com inputs: {inputs_str}")
            return await team_instance.print_response(inputs_str, **kwargs)
        
        # Substitui o método run e arun da classe com nossas versões modificadas
        cls.run = run
        cls.kickoff = kickoff
        
        return cls
    
    return decorator

# Para compatibilidade com código existente
load_config = _load_config
load_config.find_placeholders = _find_all_placeholders
load_config.configure_and_run = OrNexusConfig

# Adicionando funções do agent_registry para permitir importação única
OrNexusConfig.agent = agent
OrNexusConfig.agents = agents 
OrNexusConfig.initialize_agents = initialize_agents 