import re

CAMINHO_SQL = "./bancodados/sql"

CAMINHO_SCRIPTS_ANALISES = "./bancodados/scripts"

CAMINHO_SQL_ANALISES = "./bancodados/sql/03-analises"
CAMINHO_SQL_ANALISES_SERIES = "./bancodados/sql/04-analises-serie"
CAMINHO_ANALISES = "../dados/analises"
CAMINHO_NORMALIZADOS = "../dados/normalizados"


'''
def ler_arquivo(caminho_arq)

ler o conteúdo de um arquivo texto
'''
def ler_arquivo(caminho_arq):

    with open(caminho_arq, 'r', encoding='utf8') as arq:
        template = arq.read()
        arq.close()

    return template

def extrair_campos_template(template):
    # Match the pattern $(something)
    matches = re.findall(r'\$\(([^)]+)\)', template)
    # Use set to remove duplicates
    unique_fields = list(set(matches))
    return unique_fields

def processar_template(caminho_template, valores_mapeados):
    conteudo_template = ler_arquivo(caminho_template)
    campos_template = extrair_campos_template(conteudo_template)

    for campo in campos_template:
        if not campo in valores_mapeados:
            continue

        conteudo_template = conteudo_template.replace(f'$({campo})', str(valores_mapeados[campo]))

    return conteudo_template
