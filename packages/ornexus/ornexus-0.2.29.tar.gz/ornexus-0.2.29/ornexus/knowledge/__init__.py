"""
Pacote para armazenamento de conhecimento do OrNexus.
O usuário deve adicionar arquivos de texto (.txt) neste diretório para uso pelo framework.

# ======================================================================
# KNOWLEDGE BASE CONFIGURATION
# Para mais informações sobre bases de conhecimento no Agno, consulte:
# @https://docs.agno.com/knowledge/introduction
# ======================================================================

O framework OrNexus utiliza a biblioteca TextKnowledgeBase do Agno para criar
uma base de conhecimento vetorial a partir de arquivos de texto.

A pasta 'macro' dentro deste diretório é utilizada para armazenar arquivos 
de conhecimento macroeconômico que serão convertidos em embeddings e 
armazenados em um banco de dados vetorial MongoDB.

Para adicionar novos conhecimentos:
1. Adicione arquivos .txt na pasta 'macro'
2. Inicialize o OrNexus com recreate_knowledge=True para recriar a base
3. Após a inicialização, os agentes terão acesso a esse conhecimento

Exemplo de uso:
```python
# Inicializar o OrNexus recriando a base de conhecimento
ornexus = OrNexus(recreate_knowledge=True)

# Os agentes agora terão acesso ao novo conhecimento
result = await ornexus.team().arun(inputs)
```
""" 