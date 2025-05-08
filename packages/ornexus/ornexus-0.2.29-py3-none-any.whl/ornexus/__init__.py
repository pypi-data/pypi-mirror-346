"""
OrNexus - Framework para criação de agentes com Agno
"""

import os
import configparser
from pathlib import Path

# Função para obter a versão diretamente do setup.cfg
def get_version_from_setup_cfg():
    try:
        # Localizar o arquivo setup.cfg relativo ao pacote
        package_dir = Path(__file__).resolve().parent
        repo_root = package_dir.parent  # Diretório pai do pacote ornexus
        setup_cfg_path = repo_root / "setup.cfg"
        
        # Se o arquivo não existir no caminho relativo, tente buscar o caminho instalado
        if not setup_cfg_path.exists():
            # Caso esteja instalado, procure na raiz do pacote
            import ornexus
            package_root = Path(ornexus.__file__).resolve().parent.parent
            setup_cfg_path = package_root / "setup.cfg"
        
        # Se ainda não encontrou, retorne uma versão padrão
        if not setup_cfg_path.exists():
            return "0.1.0"
            
        # Ler o arquivo setup.cfg
        config = configparser.ConfigParser()
        config.read(setup_cfg_path)
        
        # Extrair a versão
        if 'metadata' in config and 'version' in config['metadata']:
            return config['metadata']['version']
        
        return "0.1.0"  # Versão padrão se não encontrar
    except Exception:
        return "0.1.0"  # Versão padrão em caso de erro

# Definir a versão
__version__ = get_version_from_setup_cfg()

from .utils import OrNexusConfig
from .main import OrNexus, main
from .utils.config_utils import OrNexusConfig

__all__ = ["OrNexus", "OrNexusConfig", "main"] 