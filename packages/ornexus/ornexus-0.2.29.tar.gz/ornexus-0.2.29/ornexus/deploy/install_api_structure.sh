#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Iniciando instalação do Genius Deployer...${NC}"

# Criar arquivos
echo -e "${YELLOW}Criando arquivos do projeto...${NC}"

# 2. Criar api.py
echo -e "${YELLOW}Criando api.py...${NC}"
cat > api.py << 'EOL'
from fastapi import Header, HTTPException, FastAPI, status, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, create_model, Field
from typing import Optional, Dict, Any, List
import os
import logging
import ast
import time
import subprocess
import json
from task_manager import create_task, get_status, execute_task, normalize_queue_name
from utils import get_service_name
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone, UTC
import psutil
import redis
import traceback
import asyncio

# Configuração do Redis via env
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
DYNAMIC_INPUTS = {}

# Extrair SERVICE_NAME dinamicamente
SERVICE_NAME = get_service_name()
logger.info(f"SERVICE_NAME definido como: {SERVICE_NAME}")

def extract_inputs_from_main():
    """Extrai os inputs de todos os métodos kickoff do arquivo main.py"""
    try:
        inputs_dict = {}
        
        logger.info("Iniciando extração de inputs do main.py")
        src_dir = os.path.join('src')
        logger.info(f"Procurando main.py a partir do diretório: {src_dir}")
        
        # Procurar o main.py
        main_path = None
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                if 'main.py' in files:
                    main_path = os.path.join(root, 'main.py')
                    logger.info(f"main.py encontrado em: {main_path}")
                    break
        
        if not main_path:
            logger.warning("Arquivo main.py não encontrado")
            return {}

        with open(main_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        tree = ast.parse(content)
        
        # Primeiro, procurar classes que herdam de BaseModel
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                is_basemodel = False
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'BaseModel':
                        is_basemodel = True
                        break
                
                if is_basemodel:
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign):
                            field_name = item.target.id
                            
                            # Extrair tipo
                            if isinstance(item.annotation, ast.Name):
                                field_type = item.annotation.id
                            elif isinstance(item.annotation, ast.Subscript):
                                if isinstance(item.annotation.value, ast.Name):
                                    field_type = item.annotation.value.id
                                else:
                                    continue
                            else:
                                continue
                            
                            # Extrair valor padrão se existir
                            default_value = None
                            required = True
                            if item.value:
                                if isinstance(item.value, ast.Constant):
                                    default_value = item.value.value
                                    required = False
                                elif isinstance(item.value, ast.List):
                                    default_value = []
                                    required = False
                                elif isinstance(item.value, ast.Dict):
                                    default_value = {}
                                    required = False
                            
                            inputs_dict[field_name] = {
                                'type': field_type.lower(),
                                'required': required
                            }
                            if default_value is not None:
                                inputs_dict[field_name]['default'] = default_value

        # Se não encontrou inputs no BaseModel, procurar no kickoff
        if not inputs_dict:
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node, 'func') and isinstance(node.func, ast.Attribute):
                        if node.func.attr == 'kickoff':
                            for keyword in node.keywords:
                                if keyword.arg == 'inputs':
                                    if isinstance(keyword.value, ast.Dict):
                                        for key, value in zip(keyword.value.keys, keyword.value.values):
                                            if isinstance(key, ast.Constant):
                                                value_info = get_value_type(value)
                                                inputs_dict[key.value] = value_info

        logger.info(f"Inputs extraídos com sucesso: {inputs_dict}")
        return inputs_dict
        
    except Exception as e:
        logger.error(f"Erro ao extrair inputs: {str(e)}")
        return {}

def get_value_type(value_node):
    """Determina o tipo de valor de um nó AST"""
    if isinstance(value_node, ast.Constant):
        return {
            'type': type(value_node.value).__name__.lower(),
            'default': value_node.value
        }
    elif isinstance(value_node, ast.Name):
        return {
            'type': value_node.id.lower(),
            'required': True
        }
    elif isinstance(value_node, ast.List):
        return {
            'type': 'list',
            'required': True
        }
    elif isinstance(value_node, ast.Dict):
        return {
            'type': 'dict',
            'required': True
        }
    else:
        return {
            'type': 'any',
            'required': True
        }

# Inicializar FastAPI
app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar inputs iniciais
DYNAMIC_INPUTS = extract_inputs_from_main()

# Criar modelo Pydantic dinamicamente
input_fields = {}
for field_name, field_info in DYNAMIC_INPUTS.items():
    field_type = field_info.get('type')
    default_value = field_info.get('default')
    
    type_mapping = {
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'List': List,
        'Dict': Dict[str, Any]
    }
    
    field_type = type_mapping.get(field_type, Any)
    
    if default_value is not None:
        input_fields[field_name] = (field_type, Field(default=default_value))
    else:
        input_fields[field_name] = (field_type, Field())

InputModel = create_model('InputModel', **input_fields)

async def validate_token(authorization: str = Header(None)):
    """Valida o token de autorização"""
    try:
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization header is missing")
        
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        
        api_token = os.getenv("API_KEY")  # Token padrão para teste
        if token != api_token:
            raise HTTPException(status_code=403, detail="Invalid API token")
            
        return token
        
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid authorization header format")

@app.get("/inputs")
async def get_inputs(token: str = Security(validate_token)):
    """Retorna apenas os inputs obrigatórios (required=True) da classe BaseModel com valores vazios"""
    try:
        inputs_dict = extract_inputs_from_main()
        
        # Filtrar apenas os inputs obrigatórios (required=True) e criar dicionário com valores vazios
        required_inputs = {
            k: "" 
            for k, v in inputs_dict.items() 
            if v.get('required', False) and 'default' not in v
        }
        
        logger.info(f"Inputs obrigatórios filtrados: {required_inputs}")
        
        return required_inputs  # Retorna diretamente o dicionário
        
    except Exception as e:
        logger.error(f"Erro ao obter inputs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/kickoff", response_model=dict)
async def start_task(data: Dict[str, Any], token: str = Security(validate_token)):
    """Inicia uma tarefa assíncrona"""
    try:
        # Obter os inputs permitidos
        required_inputs = extract_inputs_from_main()
        
        if not required_inputs:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Não foi possível determinar os inputs necessários",
                    "help": "Verifique se o arquivo main.py está configurado corretamente"
                }
            )

        # Validar inputs
        input_dict = data.get('inputs', data)
        
        # Garantir que input_dict seja um dicionário
        if not isinstance(input_dict, dict):
            input_dict = {"inputs": input_dict}
        
        # Verificar se há inputs não permitidos
        invalid_inputs = [
            k for k in input_dict.keys() 
            if k not in required_inputs and k != 'output_api'
        ]
        
        if invalid_inputs:
            error_msg = (
                f"Inputs não permitidos: {', '.join(invalid_inputs)}. "
                f"Apenas os seguintes campos são aceitos: {', '.join(required_inputs.keys())}"
            )
            logger.error(error_msg)
            raise HTTPException(
                status_code=400,
                detail={
                    "error": error_msg,
                    "allowed_inputs": list(required_inputs.keys()),
                    "help": "Use o endpoint /inputs para ver os campos necessários"
                }
            )
        
        # Verificar se todos os inputs obrigatórios estão presentes
        required_fields = [
            k for k, v in required_inputs.items() 
            if v.get('required', True) and 'default' not in v
        ]
        
        missing_inputs = [
            k for k in required_fields 
            if k not in input_dict
        ]
        
        if missing_inputs:
            error_msg = (
                f"Campos obrigatórios ausentes: {', '.join(missing_inputs)}. "
                f"Todos os seguintes campos são obrigatórios: {', '.join(required_fields)}"
            )
            logger.error(error_msg)
            raise HTTPException(
                status_code=400,
                detail={
                    "error": error_msg,
                    "required_inputs": required_fields,
                    "help": "Use o endpoint /inputs para ver os campos necessários"
                }
            )
        
        # Processar valores para garantir que sejam serializáveis
        processed_input = {}
        for key, value in input_dict.items():
            if isinstance(value, (list, dict)):
                processed_input[key] = json.dumps(value)
            else:
                processed_input[key] = str(value)
        
        # Logs de diagnóstico corrigidos
        logger.info(f"Iniciando task com inputs: {processed_input}")
        logger.info(f"Queue atual: {SERVICE_NAME}")
        
        logger.info(f"""
        Enviando nova task:
        - SERVICE_NAME: {SERVICE_NAME}
        - Input: {processed_input}  # Usar processed_input ao invés de input_data
        """)

        # Enviar task usando kwargs com processed_input
        task_id = create_task(processed_input)

        logger.info(f"""
        Task enviada:
        - Task ID: {task_id}
        - Queue: {SERVICE_NAME}
        """)

        return {"task_id": task_id}
    except Exception as e:
        logger.error(f"Erro ao enviar task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def verify_api_key(authorization: str = Header(None)):
    """Valida o token de autorização"""
    try:
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization header is missing")
        
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        
        api_token = os.getenv("API_KEY")
        if token != api_token:
            raise HTTPException(status_code=403, detail="Invalid API token")
            
        return token
        
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid authorization header format")

@app.get("/status/{task_id}")
async def get_task_status(task_id: str, authorization: str = Header(None)):
    """Retorna o status cru de uma task"""
    try:
        # Validar token
        verify_api_key(authorization)
        
        # Importar funções necessárias
        from task_manager import get_status, normalize_queue_name
        import redis.asyncio as redis
        
        # Inicializar cliente Redis
        redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
        
        # Garantir que usamos o nome normalizado da queue
        normalized_queue = normalize_queue_name(SERVICE_NAME)
        logger.info(f"Buscando status da task {task_id} na queue {normalized_queue}")
        
        # Obter status da task usando a função get_status existente
        task_status = await get_status(task_id)
        
        # Verificar dados no Redis
        try:
            task_data = await redis_client.get(f"task:{task_id}")
            stored_data = json.loads(task_data) if task_data else {}
            logger.info(f"Dados do Redis: {stored_data}")
        except Exception as redis_error:
            logger.error(f"Erro ao acessar Redis: {str(redis_error)}")
            stored_data = {}
        finally:
            await redis_client.close()  # Fechar conexão com Redis
        
        # Garantir que retornamos um JSON válido com todos os dados
        response_data = {
            "task_id": task_id,
            "queue": normalized_queue,
            "state": task_status.get('state', 'UNKNOWN'),
            "result": stored_data.get('result', {}).get('output') if stored_data and 'result' in stored_data else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"Status data: {response_data}")
        return response_data

    except Exception as e:
        error_response = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.error(f"Erro ao obter status: {error_response}")
        return error_response

@app.get("/health")
@app.get("/")
async def health_check():
    """Endpoint de verificação de saúde com diagnóstico detalhado"""
    try:
        # Verificar Redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        redis_ok = r.ping()

        # Verificar processos
        redis_running = any('redis-server' in p.name() for p in psutil.process_iter(['name']))
        
        status = {
            "status": "healthy" if redis_ok and redis_running else "unhealthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {
                "redis": {
                    "connected": redis_ok,
                    "running": redis_running,
                },
                "service": {
                    "name": SERVICE_NAME,
                    "pid": os.getpid()
                }
            }
        }
        
        # Se algum componente estiver unhealthy, retornar 503
        if status["status"] == "unhealthy":
            return JSONResponse(
                status_code=503,
                content=status
            )
            
        return status

    except Exception as e:
        logger.error(f"Health check falhou: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Requisição recebida: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta enviada: {response.status_code}")
    return response

@app.get("/auth/github/login")
async def github_login():
    """Inicia o fluxo de login do GitHub OAuth"""
    try:
        # Gerar state aleatório para segurança
        state = secrets.token_urlsafe(32)
        
        # Construir URL de autorização do GitHub
        github_auth_url = (
            "https://github.com/login/oauth/authorize"
            f"?client_id={GITHUB_CLIENT_ID}"
            f"&redirect_uri={FRONTEND_URL}/auth/github/callback"
            f"&state={state}"
            "&scope=user:email"
        )
        
        # Redirecionar para a página de autorização do GitHub
        return RedirectResponse(url=github_auth_url)
        
    except Exception as e:
        logger.error(f"Erro no login do GitHub: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processo de login: {str(e)}"
        )

@app.post("/execute")
async def execute(request: Request):
    """
    Endpoint chamado pelo Cloud Tasks para executar a task
    """
    try:
        # Validar autorização
        authorization = request.headers.get('Authorization')
        verify_api_key(authorization)
        
        # Receber payload
        payload = await request.json()
        input_data = payload.get('input_data')
        task_id = payload.get('task_id')
        
        # Executar a tarefa em background sem bloquear o endpoint
        # MUDANÇA CRÍTICA: Iniciar a execução sem aguardar o resultado
        asyncio.create_task(execute_task(task_id, input_data))
        
        # Retornar imediatamente com confirmação de recebimento
        return {"status": "accepted", "task_id": task_id, "message": "Tarefa iniciada com sucesso"}
            
    except Exception as e:
        logger.error(f"Erro na execução da task: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 
EOL

# 3. Criar task_manager.py
echo -e "${YELLOW}Criando task_manager.py...${NC}"
cat > task_manager.py << 'EOL'
import os
import logging
import redis
import subprocess
import sys
import importlib
import ast
import re
import json
import traceback
from google.cloud import tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2
from utils import get_service_name
from datetime import datetime, timezone, UTC
from google.api_core import exceptions as google_exceptions
from google.iam.v1 import iam_policy_pb2
import time
import redis.asyncio as redis
import secrets
from multiprocessing import Process, Queue
import concurrent.futures
import asyncio

SERVICE_NAME = get_service_name()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(SERVICE_NAME)

# Configuração do Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '0')

logger.info(f"Configuração do Redis: Host={REDIS_HOST}, Port={REDIS_PORT}, DB={REDIS_DB}")

# Teste de conexão com o Redis
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0))
    )
    redis_client.ping()
    logger.info("Conexão com o Redis estabelecida com sucesso")
except redis.ConnectionError as e:
    logger.error(f"Erro ao conectar ao Redis: {e}")

# Configuração do Cloud Tasks
tasks_client = tasks_v2.CloudTasksClient()
project = os.getenv('GOOGLE_CLOUD_PROJECT')
location = os.getenv('GOOGLE_CLOUD_REGION')
queue = SERVICE_NAME

# Normalization for queue names (lowercase only, hyphens for separators)
normalized_queue = queue.lower().replace('_', '-')

logger.info(f"""
Configuração do Task Manager:
- SERVICE_NAME: {SERVICE_NAME}
- Queue Normalizada: {normalized_queue}
- Project: {project or 'projetos-com-ia'}
- Location: {location or 'us-central1'}
""")

def ensure_queue_exists():
    """
    Verifica se a fila do Cloud Tasks existe e a cria se necessário.
    Retorna True se a fila existe ou foi criada com sucesso, False caso contrário.
    """
    try:
        # Valores padrão se não estiverem definidos
        project_id = project or 'projetos-com-ia'
        region = location or 'us-central1'
        queue_name = normalized_queue
        
        # Caminho completo da fila
        parent = f"projects/{project_id}/locations/{region}"
        queue_path = f"{parent}/queues/{queue_name}"
        
        logger.info(f"Verificando existência da fila: {queue_path}")
        
        try:
            # Tenta obter a fila primeiro
            queue = tasks_client.get_queue(name=queue_path)
            logger.info(f"Fila {queue_name} já existe!")
            return True
        except google_exceptions.NotFound:
            # Fila não existe, precisamos criá-la
            logger.info(f"Fila {queue_name} não encontrada. Criando...")
            
            # Configura uma nova fila com configurações padrão
            queue = {
                "name": queue_path,
                "rate_limits": {
                    "max_dispatches_per_second": 5,
                    "max_concurrent_dispatches": 10
                },
                "retry_config": {
                    "max_attempts": 5,
                    "min_backoff": {"seconds": 1},
                    "max_backoff": {"seconds": 60},
                    "max_retry_duration": {"seconds": 3600}
                }
            }
            
            # Cria a fila
            response = tasks_client.create_queue(parent=parent, queue=queue)
            logger.info(f"Fila {queue_name} criada com sucesso: {response.name}")
            return True
            
    except Exception as e:
        logger.error(f"Erro ao verificar/criar fila: {str(e)}")
        return False

# Função para criar o path da queue
def get_queue_path():
    """
    Retorna o caminho completo da fila do Cloud Tasks.
    """
    project_id = project or 'projetos-com-ia'
    region = location or 'us-central1'
    queue_name = normalized_queue
    
    return tasks_client.queue_path(project_id, region, queue_name)

def setup_queue_permissions():
    """Configura permissões necessárias para a queue"""
    try:
        # Obter o email da service account atual
        service_account = f"crew-deploy-service@{project}.iam.gserviceaccount.com"
        queue_path = get_queue_path()
        parent = f"projects/{project}/locations/{location}"

        # 1. Primeiro criar a queue se não existir
        try:
            queue_config = {
                "name": queue_path,
                "rate_limits": {
                    "max_concurrent_dispatches": 1,
                    "max_dispatches_per_second": 1
                },
                "retry_config": {
                    "max_attempts": 5,
                    "min_backoff": {"seconds": 30},
                    "max_backoff": {"seconds": 3600},
                    "max_doublings": 5
                },
                "state": "RUNNING"
            }
            tasks_client.create_queue(request={"parent": parent, "queue": queue_config})
            logger.info(f"Queue {queue} criada com sucesso")
            # Aguardar propagação
            time.sleep(5)
        except google_exceptions.AlreadyExists:
            logger.info(f"Queue {queue} já existe")
        
        # 2. Configurar permissões no nível do projeto
        try:
            # Adicionar roles no nível do projeto
            for role in ["roles/cloudtasks.admin", "roles/cloudtasks.enqueuer", "roles/cloudtasks.taskRunner"]:
                subprocess.run([
                    "gcloud", "projects", "add-iam-policy-binding",
                    project,
                    f"--member=serviceAccount:{service_account}",
                    f"--role={role}",
                    "--condition=None"
                ], check=True)
            logger.info("Permissões do projeto configuradas")
        except Exception as e:
            logger.warning(f"Erro ao configurar permissões do projeto: {str(e)}")

        # 3. Configurar permissões específicas da queue
        try:
            policy = tasks_client.get_iam_policy(request={"resource": queue_path})
            
            # Adicionar todas as permissões necessárias
            for role in ["roles/cloudtasks.enqueuer", "roles/cloudtasks.taskRunner", "roles/cloudtasks.viewer"]:
                binding_exists = False
                for binding in policy.bindings:
                    if binding.role == role:
                        if f"serviceAccount:{service_account}" not in binding.members:
                            binding.members.append(f"serviceAccount:{service_account}")
                        binding_exists = True
                        break
                
                if not binding_exists:
                    new_binding = policy.bindings.add()
                    new_binding.role = role
                    new_binding.members.append(f"serviceAccount:{service_account}")
            
            # Atualizar política
            tasks_client.set_iam_policy(request={"resource": queue_path, "policy": policy})
            logger.info("Permissões da queue configuradas")
            
            # Aguardar propagação
            time.sleep(5)
            
        except Exception as e:
            logger.warning(f"Erro ao configurar permissões da queue: {str(e)}")

        return True

    except Exception as e:
        logger.error(f"Erro ao configurar permissões: {str(e)}")
        return False

def run_kickoff_in_process(main_module, queue):
    import traceback
    
    try:
        flow = main_module.kickoff()
        
        def extract_pydantic_data(obj):
            """Extrai recursivamente dados de modelos Pydantic"""
            if hasattr(obj, 'dict'):
                return obj.dict()
            elif isinstance(obj, dict):
                return {k: extract_pydantic_data(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [extract_pydantic_data(item) for item in obj]
            else:
                return obj

        # Lista de campos a serem ignorados (campos internos do Pydantic)
        ignore_fields = {
            'model_computed_fields', 
            'model_config', 
            'model_extra',
            'model_fields',
            'model_fields_set'
        }

        # Extrai apenas atributos que são dados (não métodos e não campos internos)
        result = {}
        for attr_name in dir(flow):
            if (not attr_name.startswith('_') and  # não é privado
                not callable(getattr(flow, attr_name)) and  # não é método
                attr_name not in ignore_fields):  # não é campo interno do Pydantic
                attr_value = getattr(flow, attr_name)
                result[attr_name] = extract_pydantic_data(attr_value)
            
        queue.put(result)
        
    except Exception as e:
        queue.put({
            "error": str(e), 
            "traceback": traceback.format_exc()
        })

async def execute_task(task_id, input_data):
    """
    Versão assíncrona da execução de task com logs simplificados
    """
    # logger.info(f"[DIAGNÓSTICO] Iniciando execute_task com task_id={task_id}")
    # logger.info(f"[DIAGNÓSTICO] Input data recebido: {json.dumps(input_data, indent=2)}")
    
    logger.info(f"⚙️ Iniciando execução da task {task_id}")
    
    try:
        # Iniciar atualizando o status para "PROCESSING"
        await store_task_result(task_id, {
            'status': 'PROCESSING',
            'started_at': datetime.now(UTC).isoformat()
        })
        
        # Log inicial detalhado
        # logger.info(f"""
        # [Task {task_id}] Iniciando execução:
        # - SERVICE_NAME: {SERVICE_NAME}
        # - Input Data: {input_data}
        # - Task ID: {task_id}
        # - Queue: {queue}
        # """)
        
        logger.info(f"🚀 Task {task_id} em processamento | Serviço: {SERVICE_NAME}")

        # Extrair inputs do wrapper se existir
        if isinstance(input_data, dict) and 'inputs' in input_data:
            input_data = input_data['inputs']
            
        # logger.info('Iniciando execução com input: %s', input_data)
        logger.info(f"📥 Recebidos {len(input_data) if isinstance(input_data, dict) else 'N/A'} parâmetros de entrada")

        # Validar inputs antes de prosseguir
        if not input_data:
            raise ValueError("Nenhum input fornecido. Use o endpoint /inputs para ver os campos necessários.")

        # Processar input_data para garantir que não haja listas como chaves
        processed_input = {}
        for key, value in input_data.items():
            if isinstance(value, (list, dict)):
                processed_input[key] = json.dumps(value)
            else:
                processed_input[key] = value

        input_data = processed_input

        # Extrair output_api do input se existir
        output_api = input_data.get('output_api', '')
        logger.info(f'Output API extraído: {output_api}')

        try:
            # Processar e atualizar main.py com os inputs
            src_dir = '/app/src'
            main_path = os.path.join(src_dir, SERVICE_NAME, 'main.py')
            logger.info(f'Analisando main.py em: {main_path}')

            # Criar __init__.py em todos os diretórios necessários
            def create_init_files(start_path):
                for root, dirs, files in os.walk(start_path):
                    init_file = os.path.join(root, '__init__.py')
                    if not os.path.exists(init_file):
                        with open(init_file, 'w') as f:
                            pass
                        logger.info(f'Criado __init__.py em: {root}')

            create_init_files(src_dir)

            # Adicionar diretório src ao PYTHONPATH
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)

            try:
                # Importar o módulo main usando importlib
                spec = importlib.util.spec_from_file_location(
                    f"{SERVICE_NAME}.main",
                    main_path
                )
                
                if spec is None:
                    raise ImportError(f"Não foi possível criar spec para {main_path}")
                    
                main_module = importlib.util.module_from_spec(spec)
                sys.modules[f"{SERVICE_NAME}.main"] = main_module
                main_module.__package__ = SERVICE_NAME
                
                package_path = os.path.dirname(main_path)
                if os.path.exists(package_path):
                    main_module.__path__ = [package_path]
                
                spec.loader.exec_module(main_module)
                logger.info("Módulo main.py importado com sucesso")

                # Processar BaseModel e inputs
                with open(main_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                # Encontrar a classe que herda de BaseModel
                basemodel_class = None
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            if isinstance(base, ast.Name) and base.id == 'BaseModel':
                                basemodel_class = node
                                logger.info(f'Classe BaseModel encontrada: {node.name}')
                                break

                if basemodel_class:
                    # Atualizar main.py com os novos valores
                    with open(main_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Procurar e substituir valores
                    updated_lines = []
                    for line in lines:
                        line_updated = line
                        for input_name, value in input_data.items():
                            patterns = [
                                f"{input_name}\\s*=\\s*.*",
                                f"{input_name}\\s*:\\s*\\w+\\s*=\\s*.*",
                                f"{input_name}\\s*:\\s*\\w+.*"
                            ]
                            
                            for pattern in patterns:
                                if re.search(pattern, line.strip()) and not re.search(r'^\s*def\s+', line.strip()):
                                    if isinstance(value, str):
                                        formatted_value = f"'{value}'"
                                    elif isinstance(value, (list, dict)):
                                        formatted_value = json.dumps(value)
                                    else:
                                        formatted_value = str(value)
                                    
                                    indent_match = re.match(r'^(\s*)', line)
                                    indentation = indent_match.group(1) if indent_match else ''
                                    
                                    type_match = re.search(f"{input_name}\\s*:\\s*(\\w+)", line)
                                    if type_match:
                                        line_updated = f"{indentation}{input_name}: {type_match.group(1)} = {formatted_value}\n"
                                    else:
                                        line_updated = f"{indentation}{input_name} = {formatted_value}\n"
                                    
                                    logger.info(f'Atualizando linha para: {line_updated.strip()}')
                                    break
                        
                        updated_lines.append(line_updated)
                    
                    # Encontrar a função kickoff e sua indentação
                    kickoff_indent = None
                    kickoff_start = None
                    kickoff_end = None
                    return_exists = False
                    flow_prefix = None
                    
                    for i, line in enumerate(updated_lines):
                        if 'def kickoff(' in line:
                            kickoff_start = i
                            kickoff_indent = len(line) - len(line.lstrip())
                        elif kickoff_start is not None:
                            # Procurar o prefixo do flow (ex: genius_flow)
                            if '.kickoff()' in line:
                                prefix_match = re.search(r'(\w+)\.kickoff\(\)', line)
                                if prefix_match:
                                    flow_prefix = prefix_match.group(1)
                                    logger.info(f'Prefixo do flow encontrado: {flow_prefix}')
                            
                            # Verificar se o return já existe
                            if flow_prefix and f"return {flow_prefix}.state" in line:
                                return_exists = True
                                logger.info('Return statement já existe em main.py')
                                break
                            
                            # Se encontrar outra def ou class, ou linha sem indentação, é o fim da função
                            current_indent = len(line) - len(line.lstrip())
                            if (('def ' in line or 'class ' in line) and current_indent <= kickoff_indent) or \
                               (line.strip() and current_indent < kickoff_indent):
                                kickoff_end = i
                                break
                    
                    # Só adiciona o return se ele não existir e se encontrou o prefixo
                    if not return_exists and flow_prefix:
                        # Se não encontrou o fim explicitamente, é a última linha do arquivo
                        if kickoff_end is None:
                            kickoff_end = len(updated_lines)

                        # Calcular indentação correta (4 espaços a mais que a def)
                        return_indent = ' ' * (kickoff_indent + 4)
                        return_line = f"{return_indent}return {flow_prefix}.state\n"

                        # Inserir o return antes do fim da função
                        updated_lines.insert(kickoff_end, return_line)
                        logger.info(f'Return statement adicionado ao main.py usando prefixo {flow_prefix}')
                    elif not flow_prefix:
                        logger.warning('Não foi possível encontrar o prefixo do flow no método kickoff')
                    
                    # Salvar arquivo atualizado
                    with open(main_path, 'w') as f:
                        f.writelines(updated_lines)
                    logger.info('main.py atualizado com os novos valores e return statement')

                # Executar o kickoff após atualizar o arquivo
                import traceback
                import asyncio
                logger.info("=== Iniciando execução do módulo main ===")
                
                try:
                    # Importar o módulo main usando importlib
                    spec = importlib.util.spec_from_file_location(
                        f"{SERVICE_NAME}.main",
                        os.path.join('/app/src', SERVICE_NAME, 'main.py')
                    )
                    
                    if spec is None:
                        raise ImportError(f"Não foi possível criar spec para {SERVICE_NAME}.main")
                        
                    main_module = importlib.util.module_from_spec(spec)
                    sys.modules[f"{SERVICE_NAME}.main"] = main_module
                    spec.loader.exec_module(main_module)
                    
                    logger.info(f"""
                    === Iniciando execução ===
                    Service: {SERVICE_NAME}
                    Task ID: {task_id}
                    Função: kickoff
                    """)
                    
                    # Verificar se existe a função kickoff
                    if not hasattr(main_module, 'kickoff'):
                        raise AttributeError(f"Módulo não possui função 'kickoff'")
                    
                    # MUDANÇA CRÍTICA: Processar em um executor separado para não bloquear
                    # em vez de p.join() que bloqueia
                    # Criar queue para receber o resultado
                    result_queue = Queue()
                    
                    # Iniciar o processo
                    p = Process(target=run_kickoff_in_process, args=(main_module, result_queue))
                    p.start()
                    
                    # Iniciar monitoramento assíncrono do processo 
                    process_done = False
                    start_time = time.time()
                    
                    # Function para verificar se o processo terminou
                    async def check_process_completion():
                        nonlocal process_done
                        while p.is_alive() and not process_done:
                            await asyncio.sleep(0.5)  # Verificar a cada 0.5 segundo sem bloquear
                            
                            # Timeout safety - interromper após tempo limite (ex: 30 minutos)
                            if time.time() - start_time > 1800:  # 30 minutos em segundos
                                logger.warning(f"Timeout de 30 minutos atingido para task {task_id}, encerrando processo")
                                p.terminate()
                                break
                        
                        process_done = True
                    
                    # Iniciar verificação em background
                    asyncio.create_task(check_process_completion())
                    
                    # Verificar periodicamente se o resultado está disponível
                    resultado = None
                    while not process_done:
                        # Tentar obter resultado da fila sem bloquear
                        try:
                            if not result_queue.empty():
                                resultado = result_queue.get(block=False)
                                process_done = True
                                break
                        except:
                            pass
                            
                        # Aguardar um pouco e verificar novamente
                        await asyncio.sleep(0.5)
                    
                    # Se o processo terminou mas não há resultado, tentar uma última vez
                    if resultado is None and not result_queue.empty():
                        resultado = result_queue.get(block=False)
                    
                    # Garantir que o processo foi encerrado
                    if p.is_alive():
                        p.terminate()
                    
                    # Calcular tempo de execução
                    execution_time = time.time() - start_time
                    
                    # Adicionar log antes de store_task_result
                    # logger.info(f"[DIAGNÓSTICO] Resultado bruto obtido do processo: {json.dumps(resultado, indent=2, default=str) if resultado else 'None'}")
                    logger.info(f"✅ Processamento concluído em {execution_time:.2f}s")
                    
                    # Armazenar resultado no Redis
                    task_result = {
                        'output': resultado,
                        'error': None,
                        'execution_time': execution_time,
                        'completed_at': datetime.now(UTC).isoformat(),
                        'status': 'COMPLETED'
                    }
                    
                    # logger.info(f"[DIAGNÓSTICO] task_result sendo enviado para store_task_result: {json.dumps(task_result, indent=2, default=str)}")
                    logger.info(f"💾 Salvando resultado da task {task_id}")
                    
                    await store_task_result(task_id, task_result)
                    
                    # Log do resultado final
                    # logger.info(f"[DIAGNÓSTICO] Resultado final de execute_task: {json.dumps(task_result, indent=2, default=str)}")
                    logger.info(f"✨ Task {task_id} finalizada com sucesso")
                    
                    return task_result

                except Exception as e:
                    error_msg = f"Erro durante execução: {str(e)}"
                    logger.error(error_msg)
                    logger.error(traceback.format_exc())
                    
                    # Armazenar erro no Redis com log
                    error_result = {
                        'output': None,
                        'error': {
                            'message': str(e),
                            'traceback': traceback.format_exc()
                        },
                        'completed_at': datetime.now(UTC).isoformat(),
                        'status': 'ERROR'
                    }
                    
                    # logger.info(f"[DIAGNÓSTICO] error_result em caso de exceção: {json.dumps(error_result, indent=2, default=str)}")
                    logger.info(f"❌ Erro ao executar task {task_id}: {str(e)}")
                    
                    await store_task_result(task_id, error_result)
                    return error_result

            finally:
                logger.info(f"Task {task_id} finalizada")

        except Exception as e:
            # logger.error(f"Erro na execução: {str(e)}")
            logger.error(f"❌ Erro ao executar task {task_id}: {str(e)}")
            await store_task_result(task_id, {'error': str(e)})
            raise

    except Exception as e:
        # logger.error(f"Erro na execução: {str(e)}")
        logger.error(f"❌ Erro ao executar task {task_id}: {str(e)}")
        await store_task_result(task_id, {'error': str(e)})
        raise

def normalize_queue_name(name: str) -> str:
    """
    Normaliza o nome da queue seguindo as regras do Cloud Tasks:
    - Apenas letras minúsculas, números e hífens
    - Deve começar com letra
    - Não pode terminar com hífen
    """
    if not name:
        return "default-queue"
        
    # Substituir underscore por hífen
    name = name.replace('_', '-')
    
    # Converter para minúsculas
    name = name.lower()
    
    # Remover caracteres inválidos
    name = re.sub(r'[^a-z0-9-]', '', name)
    
    # Remover hífens múltiplos
    name = re.sub(r'-+', '-', name)
    
    # Remover hífen do início se existir
    name = name.lstrip('-')
    
    # Remover hífen do final se existir
    name = name.rstrip('-')
    
    # Garantir que começa com letra
    if not name[0].isalpha():
        name = 'q-' + name
        
    return name

def get_queue_path():
    """Retorna o path completo da queue normalizado"""
    normalized_name = normalize_queue_name(SERVICE_NAME)
    logger.info(f"Nome da queue normalizado: {normalized_name} (original: {SERVICE_NAME})")
    return f"projects/{project}/locations/{location}/queues/{normalized_name}"

def create_task(input_data: dict):
    """
    Cria uma nova task no Cloud Tasks seguindo a estrutura oficial
    """
    try:
        logger.info("=== Iniciando criação de task ===")
        
        # Criar cliente
        client = tasks_v2.CloudTasksClient()
        logger.info("Cloud Tasks Client criado com sucesso")
        
        # Gerar task_id único
        task_id = f"{int(time.time() * 1000)}_{secrets.token_hex(4)}"
        logger.info(f"Task ID gerado: {task_id}")
        
        # Preparar payload
        json_payload = {
            'input_data': input_data,
            'task_id': task_id,
            'service_name': SERVICE_NAME
        }
        logger.info(f"Payload preparado: {json_payload}")

        # Garantir que a URL do serviço tenha o protocolo correto
        service_url = os.getenv('SERVICE_URL', '')
        if not service_url:
            raise ValueError("SERVICE_URL environment variable is not set")
            
        if not service_url.startswith(('http://', 'https://')):
            service_url = f"https://{service_url}"
            
        execute_url = f"{service_url.rstrip('/')}/execute"
        logger.info(f"URL do endpoint configurada: {execute_url}")

        # Construir a task usando a estrutura oficial
        task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=execute_url,  # URL corrigida com protocolo
                headers={
                    "Content-type": "application/json",
                    "Authorization": f"Bearer {os.getenv('API_KEY')}"
                },
                body=json.dumps(json_payload).encode(),
            ),
            name=client.task_path(project, location, normalize_queue_name(SERVICE_NAME), task_id)
        )
        logger.info(f"""
        Task configurada:
        - URL: {task.http_request.url}
        - Method: {task.http_request.http_method}
        - Headers: {task.http_request.headers}
        - Task Name: {task.name}
        """)

        # Adicionar deadline
        duration = duration_pb2.Duration()
        duration.FromSeconds(600)  # 10 minutos de deadline
        task.dispatch_deadline = duration
        logger.info(f"Deadline configurado: 600 segundos")

        # Log da queue
        queue_path = client.queue_path(
            project,
            location,
            normalize_queue_name(SERVICE_NAME)
        )
        logger.info(f"""
        Configuração da Queue:
        - Project: {project}
        - Location: {location}
        - Queue Name: {normalize_queue_name(SERVICE_NAME)}
        - Queue Path: {queue_path}
        """)

        # Criar a task usando CreateTaskRequest
        logger.info("Iniciando criação da task no Cloud Tasks...")
        response = client.create_task(
            tasks_v2.CreateTaskRequest(
                parent=queue_path,
                task=task,
            )
        )
        
        logger.info(f"""
        Task criada com sucesso:
        - Nome completo: {response.name}
        - Schedule Time: {response.schedule_time}
        - Create Time: {response.create_time}
        - Dispatch Count: {response.dispatch_count}
        """)
        
        return task_id

    except Exception as e:
        logger.error(f"""
        Erro ao criar task:
        - Erro: {str(e)}
        - Tipo: {type(e).__name__}
        - Task ID: {task_id if 'task_id' in locals() else 'Não gerado'}
        """, exc_info=True)
        raise

async def get_status(task_id: str):
    """
    Obtém o status de uma task usando o Cloud Tasks e Redis com logs simplificados
    """
    # logger.info(f"[DIAGNÓSTICO] Iniciando get_status para task_id={task_id}")
    logger.info(f"🔍 Verificando status da task {task_id}")
    
    try:
        task_path = tasks_client.task_path(
            project,
            location,
            normalize_queue_name(SERVICE_NAME),
            task_id
        )
        # logger.info(f"[DIAGNÓSTICO] Task path: {task_path}")
        
        # Verificar dados no Redis primeiro e logar
        task_data = await redis_client.get(f"task:{task_id}")
        # logger.info(f"[DIAGNÓSTICO] Dados brutos do Redis para task {task_id}: {task_data}")
        logger.info(f"📊 Buscando dados da task {task_id} no Redis")
        
        stored_data = {}
        if task_data:
            try:
                stored_data = json.loads(task_data)
                # logger.info(f"[DIAGNÓSTICO] Dados decodificados do Redis: {json.dumps(stored_data, indent=2, default=str)}")
                logger.info(f"✅ Dados encontrados no Redis para task {task_id}")
                
                # Analisar resultado e estrutura
                # if 'result' in stored_data:
                #     logger.info(f"[DIAGNÓSTICO] Estrutura de 'result': {type(stored_data['result'])}")
                #     logger.info(f"[DIAGNÓSTICO] Conteúdo de 'result': {json.dumps(stored_data['result'], indent=2, default=str)}")
                #     
                #     if isinstance(stored_data['result'], dict) and 'output' in stored_data['result']:
                #         logger.info(f"[DIAGNÓSTICO] Estrutura de 'result.output': {type(stored_data['result']['output'])}")
                #         logger.info(f"[DIAGNÓSTICO] Conteúdo de 'result.output': {json.dumps(stored_data['result']['output'], indent=2, default=str)}")
            except json.JSONDecodeError as e:
                # logger.error(f"[DIAGNÓSTICO] Erro ao decodificar dados do Redis: {e}")
                logger.error(f"⚠️ Erro ao processar dados do Redis: {e}")
        
        try:
            cloud_task = tasks_client.get_task(name=task_path)
            # logger.info(f"[DIAGNÓSTICO] Status da Cloud Task: {cloud_task}")
            logger.info(f"☁️ Informações obtidas do Cloud Tasks")
            
            # Extrair informações detalhadas da task
            task_status = {
                'id': task_id,
                'name': cloud_task.name,
                'dispatch_count': cloud_task.dispatch_count,
                'response_count': cloud_task.response_count if hasattr(cloud_task, 'response_count') else 0,
                'first_attempt': cloud_task.first_attempt.dispatch_time.timestamp() if hasattr(cloud_task, 'first_attempt') else None,
                'last_attempt': cloud_task.last_attempt.dispatch_time.timestamp() if hasattr(cloud_task, 'last_attempt') else None,
                'state': 'COMPLETED' if cloud_task.dispatch_count > 0 else 'PENDING',
                'view_name': cloud_task.view,
                'schedule_time': cloud_task.schedule_time.timestamp() if hasattr(cloud_task, 'schedule_time') else None,
                'create_time': cloud_task.create_time.timestamp() if hasattr(cloud_task, 'create_time') else None,
            }
            
            # Adicionar resultado do Redis se disponível
            if stored_data and stored_data.get('result'):
                task_status['result'] = stored_data['result']
            
            # logger.info(f"[DIAGNÓSTICO] task_status final a ser retornado: {json.dumps(task_status, indent=2, default=str)}")
            logger.info(f"📋 Status da task {task_id}: {task_status.get('state', 'UNKNOWN')}")
            return task_status
            
        except google_exceptions.NotFound:
            # logger.info(f"[DIAGNÓSTICO] Task {task_id} não encontrada no Cloud Tasks, verificando Redis...")
            logger.info(f"⚠️ Task {task_id} não encontrada no Cloud Tasks")
            
            # Verificação detalhada do Redis
            if stored_data:
                # logger.info("[DIAGNÓSTICO] Dados encontrados no Redis")
                logger.info(f"💾 Usando dados do Redis para task {task_id}")
                response = {
                    'id': task_id,
                    'state': 'COMPLETED',
                    'result': stored_data.get('result'),
                    'redis_data': stored_data
                }
                # logger.info(f"[DIAGNÓSTICO] Resposta baseada apenas no Redis: {json.dumps(response, indent=2, default=str)}")
                return response
            
            response = {
                'id': task_id,
                'state': 'NOT_FOUND',
                'error': 'Task não encontrada no Cloud Tasks nem no Redis'
            }
            # logger.info(f"[DIAGNÓSTICO] Resposta NOT_FOUND: {json.dumps(response, indent=2, default=str)}")
            logger.info(f"❌ Task {task_id} não encontrada")
            return response
        
    except Exception as e:
        # logger.error(f'[DIAGNÓSTICO] Erro ao buscar status da task: {str(e)}')
        # logger.error(traceback.format_exc())
        logger.error(f'❌ Erro ao consultar status da task {task_id}: {str(e)}')
        response = {
            'id': task_id,
            'state': 'ERROR',
            'error': str(e),
            'redis_data': stored_data if 'stored_data' in locals() else None
        }
        # logger.info(f"[DIAGNÓSTICO] Resposta de erro: {json.dumps(response, indent=2, default=str)}")
        return response

async def store_task_result(task_id, task_result):
    """
    Armazena o resultado da task no Redis com logs simplificados
    """
    # logger.info(f"[DIAGNÓSTICO] Iniciando store_task_result para task_id={task_id}")
    # logger.info(f"[DIAGNÓSTICO] task_result recebido: {json.dumps(task_result, indent=2, default=str)}")
    logger.info(f"💾 Salvando resultados da task {task_id}")
    
    # Criar objeto de dados para o Redis
    task_data = {
        'task_id': task_id,
        'queue_name': SERVICE_NAME,
        'result': task_result,
        'updated_at': datetime.now(UTC).isoformat()
    }
    
    # logger.info(f"[DIAGNÓSTICO] Dados a serem armazenados no Redis: {json.dumps(task_data, indent=2, default=str)}")
    
    # Verificar se já existe algum dado no Redis
    existing_data = await redis_client.get(f"task:{task_id}")
    if existing_data:
        # logger.info(f"[DIAGNÓSTICO] Dados existentes no Redis: {existing_data}")
        logger.info(f"🔄 Atualizando dados existentes para task {task_id}")
    else:
        # logger.info(f"[DIAGNÓSTICO] Sem dados existentes no Redis para task_id={task_id}")
        logger.info(f"➕ Criando novo registro para task {task_id}")
    
    # Armazenar no Redis
    await redis_client.set(f"task:{task_id}", json.dumps(task_data))
    
    # Verificar o que foi realmente armazenado
    # stored_data = await redis_client.get(f"task:{task_id}")
    # logger.info(f"[DIAGNÓSTICO] Dados confirmados no Redis após armazenamento: {stored_data}")
    
    # logger.info(f"Resultado da task {task_id} armazenado com sucesso: {task_data}")
    logger.info(f"✅ Dados da task {task_id} salvos com sucesso no Redis")

# Log de configuração inicial
logger.info(f"""
Configuração do Task Manager:
- SERVICE_NAME: {SERVICE_NAME}
- Queue Normalizada: {normalize_queue_name(SERVICE_NAME)}
- Project: {project}
- Location: {location}
""")
EOL

# 4. Criar utils.py
echo -e "${YELLOW}Criando utils.py...${NC}"
cat > utils.py << 'EOL'
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_service_name():
    """Extrai o nome do serviço baseado na estrutura de diretórios src/{nome_projeto}/main.py"""
    try:
        src_dir = os.path.join('src')
        if not os.path.exists(src_dir):
            logger.warning("Diretório src não encontrado")
            return "Diretório src não encontrado"
            
        # Procurar o main.py em src/{nome_projeto}/main.py
        for item in os.listdir(src_dir):
            project_dir = os.path.join(src_dir, item)
            if os.path.isdir(project_dir):
                if os.path.exists(os.path.join(project_dir, 'main.py')):
                    logger.info(f"Service name encontrado: {item}")
                    return item
                    
        logger.warning("Nenhum main.py encontrado em src/{nome_projeto}/")
        return "Nenhum main.py encontrado em src/{nome_projeto}/"
        
    except Exception as e:
        logger.error(f"Erro ao extrair service name: {str(e)}")
        return "Erro ao extrair service name"
EOL

# 5. Criar __init__.py vazio
echo -e "${YELLOW}Criando __init__.py...${NC}"
touch __init__.py

# 6. Criar requirements.txt
echo -e "${YELLOW}Criando requirements.txt...${NC}"
cat > requirements.txt << 'EOL'
fastapi
uvicorn[standard]
python-dotenv
httpx
python-multipart
instagrapi
pydub
psycopg2-binary
aiosqlite
sqlalchemy[asyncio]
asyncpg
aiohttp
redis
google-cloud-tasks
html2text
lxml
playwright
psutil
docling
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
google-auth
pymongo
whisper
moviepy
motor
databricks-sdk
EOL

# 7. Criar Dockerfile
echo -e "${YELLOW}Criando Dockerfile...${NC}"
cat > Dockerfile << 'EOL'
FROM python:3.12-slim

WORKDIR /app

# Configurar variáveis de ambiente essenciais
ENV PORT=8080 \
    PYTHONPATH=/app \
    SSL_CERT_DIR=/etc/ssl/certs \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Instalar Redis e outras dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ca-certificates \
    redis-server \
    procps \
    htop \
    postgresql \
    postgresql-client \
    postgresql-contrib \
    libpq-dev \
    python3-dev \
    gcc \
    curl \
    ffmpeg \
    imagemagick \
    && curl -sSL https://sdk.cloud.google.com | bash \
    && rm -rf /var/lib/apt/lists/*

# Configurar certificados
RUN mkdir -p /etc/ssl/certs \
    && update-ca-certificates

# Copiar requirements primeiro para aproveitar cache do Docker
COPY pyproject.toml .
COPY requirements.txt .

# Instalar dependências globalmente
RUN CREWAI_VERSION=$(grep -oP "crewai\[tools\]>=\K[0-9]+\.[0-9]+\.[0-9]+" pyproject.toml) && \
    CREWAI_TOOLS_VERSION="1.0.0" && \
    echo "CREWAI_VERSION=${CREWAI_VERSION}" && \
    echo "CREWAI_TOOLS_VERSION=${CREWAI_TOOLS_VERSION}" && \
    pip install --no-cache-dir \
        "crewai[tools]==${CREWAI_VERSION}" && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir moviepy && \
    crewai install && \
    # Verificar apenas a versão do crewai
    python3 -c 'import crewai; print(f"crewai version: {crewai.__version__}")' && \
    # Adicionar import no __init__.py do crewai-tools
    SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])") && \
    echo "from crewai.tools import BaseTool, tool" >> "${SITE_PACKAGES}/crewai_tools/__init__.py" && \
    # Verificar se a linha foi adicionada
    cat "${SITE_PACKAGES}/crewai_tools/__init__.py"

# Copiar arquivos da aplicação
COPY . .
 
# Criar estrutura de diretórios e __init__.py
RUN mkdir -p /app/src && \
    find /app/src -type d -exec touch {}/__init__.py \; && \
    touch /app/src/__init__.py

# Criar script de inicialização
RUN echo '#!/bin/bash\n\
# Ativar ambiente virtual\n\
source .venv/bin/activate\n\
\n\
# Verificar se o ambiente virtual está ativo\n\
if [[ "$VIRTUAL_ENV" != "" ]]; then\n\
    echo "Ambiente virtual ativo em: $VIRTUAL_ENV"\n\
else\n\
    echo "ERRO: Ambiente virtual não está ativo!"\n\
    exit 1\n\
fi\n\
\n\
# Verificar se crewai está instalado no ambiente virtual\n\
if pip list | grep -q crewai; then\n\
    echo "crewai instalado no ambiente virtual:"\n\
    pip show crewai | grep Version\n\
else\n\
    echo "ERRO: crewai não está instalado no ambiente virtual!"\n\
    exit 1\n\
fi\n\
\n\
# Iniciar Redis\n\
redis-server --daemonize yes\n\
\n\
# Iniciar API com Uvicorn na porta 8080\n\
uvicorn api:app --host 0.0.0.0 --port ${PORT:-8080}\n\
' > start.sh && chmod +x start.sh

EXPOSE 8080

ENTRYPOINT ["./start.sh"] 
EOL

