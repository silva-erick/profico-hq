import os
import duckdb
import logs


CAMINHO_SQL = "./bancodados/sql"
CAMINHO_SQL_CRIACAO = "./bancodados/sql/01-criacao"
CAMINHO_SQL_CARGA = "./bancodados/sql/02-carga"
CAMINHO_BRUTO_CAMPANHAS_CATARSE = "../dados/brutos/catarse/campanhas"
'''
def executar_scripts_pasta(args, caminho)
'''
def executar_scripts_pasta(args, caminho):
    campanhas = []
    logs.verbose(args.verbose, f'executar scripts pasta: {caminho}')

    if not os.path.exists(caminho):
        return False
    
    caminho_scripts = os.listdir(caminho)

    con = duckdb.connect("file.db")

    # Percorre a lista de arquivos
    for caminho_script_sql in caminho_scripts:
        # Cria o caminho completo para o file
        caminho_arq = os.path.join(caminho, caminho_script_sql)

        if not os.path.isfile(caminho_arq):
            continue

        if not caminho_arq.endswith(".sql"):
            continue
        
        # abrir arquivo
        f = open (caminho_arq, "r")
        
        # ler arquivo
        sql = f.read()
        sql = sql.replace(f'$(cities.json)', f'{CAMINHO_BRUTO_CAMPANHAS_CATARSE}/{args.ano}/cities.json')

        con.sql(sql)

        # fechar arquivo
        f.close()

    return True

'''
async def executar_montarbd(args)
-- 
'''
async def executar_montarbd(args):
    print('montar banco de dados')

    executar_scripts_pasta(args, CAMINHO_SQL_CRIACAO)
    executar_scripts_pasta(args, CAMINHO_SQL_CARGA)
