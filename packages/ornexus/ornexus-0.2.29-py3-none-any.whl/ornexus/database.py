"""
Módulo para integração com MongoDB via API OrNexus
"""

import requests
import json
from pathlib import Path
import hashlib

# URL da API de autenticação
AUTH_SERVICE_URL = "https://cli.ornexus.com/auth"

def md5_hash(text):
    """Gera um hash MD5 para o texto fornecido"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

class MongoDBAsyncIntegration:
    """
    Classe para integração com MongoDB - Agora via API OrNexus
    """
    def __init__(self, token=None, db_name=None):
        """
        Inicializa a integração
        
        Args:
            token: Token de autenticação (opcional)
            db_name: Nome do banco de dados (opcional)
        """
        self.token = token
        self.db_name = db_name or "users"
        self.connected = False
        
        # Se não foi fornecido token, tentar obter do arquivo de configuração
        if not self.token:
            config_file = Path.home() / ".ornexus" / "auth.json"
            if config_file.exists():
                try:
                    with open(config_file, "r") as f:
                        config = json.load(f)
                        self.token = config.get("token")
                except Exception:
                    pass
    
    async def inserir_documento(self, colecao, documento):
        """Método mantido por compatibilidade - usa API para operações"""
        # Esta é uma implementação mock que sempre falha, já que deveria usar a API
        raise NotImplementedError("Operações diretas de MongoDB não estão disponíveis. Use a API.")
    
    async def buscar_documento(self, colecao, filtro, limit=None, sort=None):
        """Método mantido por compatibilidade - usa API para operações"""
        # Esta é uma implementação mock que sempre falha, já que deveria usar a API
        raise NotImplementedError("Operações diretas de MongoDB não estão disponíveis. Use a API.")
    
    async def atualizar_documento(self, colecao, filtro, atualizacao):
        """Método mantido por compatibilidade - usa API para operações"""
        # Esta é uma implementação mock que sempre falha, já que deveria usar a API
        raise NotImplementedError("Operações diretas de MongoDB não estão disponíveis. Use a API.")
    
    async def deletar_documento(self, colecao, filtro):
        """Método mantido por compatibilidade - usa API para operações"""
        # Esta é uma implementação mock que sempre falha, já que deveria usar a API
        raise NotImplementedError("Operações diretas de MongoDB não estão disponíveis. Use a API.")
    
    async def fechar_conexao(self):
        """Método mantido por compatibilidade"""
        pass

# Função para autenticação diretamente via API
async def api_login(email, password):
    """
    Função para autenticar um usuário via API OrNexus
    
    Args:
        email: Email do usuário
        password: Senha em texto plano (será convertida para MD5)
        
    Returns:
        Token de autenticação ou None se a autenticação falhar
    """
    try:
        # Criar hash MD5 da senha
        password_md5 = md5_hash(password)
        
        # Fazer requisição para a API
        response = requests.post(
            f"{AUTH_SERVICE_URL}/login",
            data={"username": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        
        return None
    except Exception as e:
        print(f"❌ Erro ao conectar com o servidor: {str(e)}")
        return None 