# OrNexus

Framework para criação rápida de projetos com agentes usando as bibliotecas Agno e CrewAI.

## Instalação

Instalação básica:
```bash
pip install ornexus
```

Para instalar com suporte específico:

```bash
# Para suporte ao framework Agno
pip install ornexus[agno]

# Para suporte ao framework CrewAI
pip install ornexus[crewai]

# Para suporte completo (ambos frameworks)
pip install ornexus[all]
```

## Uso Básico

### Com Agno

```python
from ornexus import OrNexus

# Criar uma instância do OrNexus
ornexus = OrNexus()

# Executar o time de agentes
result = ornexus.team().run({
    "topico": "Impactos da política monetária dos bancos centrais em mercados emergentes",
    "tema": "Como as decisões do FED afetam economias emergentes em 2024",
    "extra_instruction": "Considere os impactos da política monetária recente dos bancos centrais."
})

print(result)
```

## Criando Projetos

### Projeto Agno

```bash
# Inicializar um novo projeto Agno
ornexus create agno meu_projeto_agno

# Navegar para o diretório do projeto
cd meu_projeto_agno

# Executar o projeto
python -m meu_projeto_agno
```

### Projeto CrewAI Flow

```bash
# Inicializar um novo projeto CrewAI
ornexus create flow meu_projeto_crewai

# Navegar para o diretório do projeto
cd meu_projeto_crewai

# Executar o projeto
crewai run
```

## Autenticação

```bash
# Fazer login na plataforma OrNexus
ornexus login

# Fazer logout
ornexus logout
```

## Estrutura de API

```bash
# Criar estrutura de API para um projeto existente
ornexus deploy -p caminho/para/projeto

# Criar estrutura de API em um novo diretório
ornexus deploy -p novo_diretorio
```

## Personalização

### Projetos Agno

Você pode personalizar os agentes e tarefas editando os arquivos YAML na pasta `config`:

- `agents.yaml`: Define os papéis e metas dos agentes
- `tasks.yaml`: Define as instruções e saídas esperadas para cada tarefa

### Projetos CrewAI

Os projetos CrewAI seguem a estrutura padrão do CrewAI, permitindo configuração de agentes e fluxos.

## Requisitos

- Python 3.8+
- Dependendo dos extras instalados:
  - Agno e MongoDB (para `ornexus[agno]`)
  - CrewAI (para `ornexus[crewai]`) 