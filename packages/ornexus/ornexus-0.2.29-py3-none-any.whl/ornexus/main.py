from typing import Dict, Any, Optional
from pathlib import Path
import os
from datetime import datetime
import re

from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude

# ======================================================================
# KNOWLEDGE BASE CONFIGURATION
# Para mais informações sobre bases de conhecimento no Agno, consulte:
# @https://docs.agno.com/knowledge/introduction
# ======================================================================
from agno.knowledge.text import TextKnowledgeBase
from agno.document.chunking.recursive import RecursiveChunking
from agno.vectordb.mongodb import MongoDb

from .utils import OrNexusConfig

def normalize_class_name(project_name):
    """
    Normaliza o nome do projeto para usar como nome de classe
    
    Args:
        project_name: Nome do projeto
        
    Returns:
        Nome da classe normalizado (PascalCase)
    """
    # Remover caracteres não alfanuméricos e substituir por espaços
    normalized = re.sub(r'[^a-zA-Z0-9]', ' ', project_name)
    # Dividir em palavras, capitalizar cada palavra e juntar
    return ''.join(word.capitalize() for word in normalized.split())

class OrNexus:
    """Classe base do framework OrNexus para criação de agentes com Agno"""
    
    def __init__(self, recreate_knowledge=False, knowledge_dir=None, mongodb_uri=None):
        """
        Inicializa a classe base do OrNexus
        
        Args:
            recreate_knowledge: Se True, recria a base de conhecimento
            knowledge_dir: Diretório com arquivos de conhecimento
            mongodb_uri: URI de conexão com o MongoDB
        """
        # Usando a conexão do MongoDB Atlas
        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_CONN")
        print(f"Usando MongoDB URI: {self.mongodb_uri}")

        # Configurar diretório de conhecimento
        self.knowledge_dir = Path(knowledge_dir or "knowledge")
        
        # Garantir que o diretório existe
        if not self.knowledge_dir.exists():
            self.knowledge_dir.mkdir(parents=True, exist_ok=True)
            print(f"Criado diretório: {self.knowledge_dir.absolute()}")
            
            # Criar um arquivo vazio de exemplo (opcional)
            readme_path = self.knowledge_dir / "README.txt"
            if not readme_path.exists():
                with open(readme_path, "w") as f:
                    f.write("# Diretório de conhecimento para OrNexus\n\n")
                    f.write("Coloque seus arquivos de conhecimento (.txt) neste diretório para uso pelo framework.\n")
        
        # Garantir que o diretório macro existe
        self.macro_dir = self.knowledge_dir / "macro"
        if not self.macro_dir.exists():
            self.macro_dir.mkdir(parents=True, exist_ok=True)
            print(f"Criado diretório: {self.macro_dir.absolute()}")

        # Contador de arquivos de texto
        txt_files = list(self.knowledge_dir.glob('*.txt'))
        print(f"Encontrados {len(txt_files)} arquivos de texto (.txt) em {self.knowledge_dir}")
        
        # Contador de arquivos de texto na pasta macro
        macro_txt_files = list(self.macro_dir.glob('*.txt'))
        print(f"Encontrados {len(macro_txt_files)} arquivos de texto (.txt) em {self.macro_dir}")
        
        # ======================================================================
        # KNOWLEDGE BASE INITIALIZATION
        # Para mais informações sobre bases de conhecimento no Agno, consulte:
        # @https://docs.agno.com/knowledge/introduction
        # 
        # O TextKnowledgeBase é usado para carregar arquivos de texto (.txt)
        # em uma base de conhecimento vetorial, que permite busca semântica.
        # O MongoDB é usado como banco de dados vetorial (vector_db).
        # O RecursiveChunking divide o texto em pedaços menores para indexação.
        # ======================================================================

        # Inicialização do TextKnowledgeBase
        self.macro_knowledge = TextKnowledgeBase(
            path=str(self.macro_dir),  # Caminho para a pasta macro com arquivos .txt
            vector_db=MongoDb(
                database="ornexus_knw",
                collection_name="knowledge", 
                db_url=self.mongodb_uri,
                wait_until_index_ready=60,
                wait_after_insert=300
            ),
            chunking_strategy=RecursiveChunking()
        )
        
        # Inicializar o modelo
        self.sonnet3_7 = Claude(
            id="claude-3-7-sonnet-20250219",
            temperature=0.0,
            max_tokens=8000
        )
        
        # ======================================================================
        # KNOWLEDGE BASE LOADING
        # Para mais informações sobre bases de conhecimento no Agno, consulte:
        # @https://docs.agno.com/knowledge/introduction
        #
        # O parâmetro recreate=True forçará a recriação completa da base de 
        # conhecimento, convertendo todos os textos em embeddings novamente.
        # Isto é útil após adicionar novos arquivos ou modificar os existentes.
        # ======================================================================
        # Carregar conhecimento
        if recreate_knowledge:
            self.macro_knowledge.load(recreate=True)
        else:
            self.macro_knowledge.load(recreate=False)

@OrNexusConfig
class DefaultProject(OrNexus):
    """Implementação padrão do OrNexus para demonstração"""
    
    def __init__(self, recreate=False):
        super().__init__(recreate_knowledge=recreate)
        
    @OrNexusConfig.agent
    def pesquisador(self) -> Agent:
        return Agent(
            name="Pesquisador Econômico",
            role=self.config_agents['researcher']['role'],
            goal=self.config_agents['researcher']['goal'],
            description=self.config_agents['researcher']['backstory'],
            instructions=self.config_tasks['pesquisador']['description'],
            expected_output=self.config_tasks['pesquisador']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            knowledge=self.macro_knowledge
        )
    
    @OrNexusConfig.agent
    def redator_twitter(self) -> Agent:
        return Agent(
            name="Redator de Conteúdo para Twitter",
            role=self.config_agents['content_writer']['role'],
            goal=self.config_agents['content_writer']['goal'],
            description=self.config_agents['content_writer']['backstory'],
            instructions=self.config_tasks['redator_twitter']['description'],
            expected_output=self.config_tasks['redator_twitter']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            knowledge=self.macro_knowledge
        )
    
    def team(self) -> Team:
        return Team(
            mode="collaborate",
            members=self.agents,
            model=self.sonnet3_7,
            debug_mode=True,
            success_criteria="Uma análise econômica completa com conteúdo pronto para redes sociais.",
            telemetry=False
        )

async def main(**kwargs):
    """
    Função principal para execução do framework como aplicação independente
    
    Args:
        kwargs: Dicionário com os parâmetros para execução
    """
    try:
        # Tenta detectar o nome do projeto a partir do diretório atual
        current_dir = os.path.basename(os.getcwd())
        class_name = normalize_class_name(current_dir)
        
        # Tenta importar a classe específica do projeto
        try:
            module = __import__(current_dir, fromlist=[class_name])
            project_class = getattr(module, class_name)
            print(f"Usando classe do projeto: {class_name}")
        except (ImportError, AttributeError):
            # Fallback para DefaultProject se não encontrar a classe do projeto
            project_class = DefaultProject
            print(f"Usando classe padrão: DefaultProject")
        
        if 'inputs' in kwargs:
            result = await project_class().kickoff(kwargs['inputs'])
            return result
        else:
            print("Nenhum input fornecido.")
            return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == "__main__":
    import asyncio
    inputs = {
        "topico": "Impactos da política monetária dos bancos centrais em mercados emergentes",
        "tema": "Como as decisões do FED afetam economias emergentes em 2024",
        "data_referencia": datetime.now().strftime("%Y-%m-%d"),
        "extra_instruction": "Considere os impactos da política monetária recente dos bancos centrais e tendências inflacionárias."
    }
    result = asyncio.run(main(inputs=inputs))
    print(result)
