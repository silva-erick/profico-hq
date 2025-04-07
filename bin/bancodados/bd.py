import os
import duckdb
import logs
import json
from datetime import datetime, timedelta
import formatos


CAMINHO_SQL = "./bancodados/sql"
CAMINHO_SQL_CRIACAO = "./bancodados/sql/01-criacao"
CAMINHO_SQL_CARGA = "./bancodados/sql/02-carga"
CAMINHO_BRUTO_CAMPANHAS_CATARSE = "../dados/brutos/catarse/campanhas"
CAMINHO_NORMALIZADOS = "../dados/normalizados"


'''
def executar_scripts_pasta(args, caminho)
'''
def executar_scripts_pasta(args, caminho):
    campanhas = []
    logs.verbose(args.verbose, f'executar scripts pasta: {caminho}')

    if not os.path.exists(caminho):
        return False
    
    caminho_scripts = os.listdir(caminho)

    con = duckdb.connect(f"{CAMINHO_NORMALIZADOS}/analises_{args.ano}.db")

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


def construir_comando_autor(campanha):
    origem = campanha['origem']
    origemdados_id = -1
    if origem=='catarse':
        origemdados_id=2
    elif origem=='apoia.se':
        origemdados_id=3

    autoria_id = campanha['autoria_id']
    autoria_nome = campanha['autoria_nome']
    autoria_nome = autoria_nome.replace("'", "''")
    autoria_nome_publico = campanha['autoria_nome_publico']
    autoria_nome_publico = autoria_nome_publico.replace("'", "''")
    autoria_classificacao_id = campanha['autoria_classificacao_id']
    template = """
INSERT INTO Autor (
     autor_id
	,origemdados_id
	,original_id
	,nome
	,nome_publico
	,classificacaoautor_id
)
SELECT  nextval('seq_autor_id')
	,{origemdados_id}
	,'{original_id}'
	,'{nome}'
	,'{nome_publico}'
	,{classificacaoautor_id}
WHERE   NOT EXISTS (
    SELECT  1
    FROM    Autor
    WHERE   origemdados_id={origemdados_id}
    AND     original_id='{original_id}'
)
    """

    sql = template.format(
        origemdados_id=origemdados_id
        ,original_id=autoria_id
        ,nome=autoria_nome
        , nome_publico=autoria_nome_publico
        ,classificacaoautor_id=autoria_classificacao_id
        )
    return sql


def tratar_valor_data_null(val):
    if val is None or val == '':
        val = 'NULL'
    else:
        val = f"'{datetime.fromisoformat(val).date()}'"
    
    return val

def tratar_valor_num_null(val):
    if val is None or val == '':
        val = 'NULL'
    else:
        val = str(val)
    
    return val


def construir_comando_campanha(campanha):
    origem = campanha['origem']
    origemdados_id = -1
    if origem=='catarse':
        origemdados_id=2
    elif origem=='apoia.se':
        origemdados_id=3
    geral_project_id = campanha['geral_project_id']

    recompensas_menor_nominal = campanha['recompensas_menor_nominal']
    recompensas_menor_ajustado = campanha['recompensas_menor_ajustado']
    recompensas_quantidade = campanha['recompensas_quantidade']
    autoria_id = campanha['autoria_id']
 
    social_seguidores = campanha['social_seguidores']
    social_newsletter = campanha['social_newsletter']
    social_sub_contribuicoes_amigos = campanha['social_sub_contribuicoes_amigos']
    social_sub_novos_seguidores = campanha['social_sub_novos_seguidores']
    social_sub_posts_projeto = campanha['social_sub_posts_projeto']
    social_projetos_contribuidos = campanha['social_projetos_contribuidos']
    social_projetos_publicados = campanha['social_projetos_publicados']

    geral_city_id = campanha['geral_city_id']

    geral_content_rating = campanha['geral_content_rating']
    if geral_content_rating is None:
        geral_content_rating=0
    geral_contributed_by_friends = campanha['geral_contributed_by_friends']
    if geral_contributed_by_friends is None:
        geral_contributed_by_friends=0
    geral_capa_imagem = campanha['geral_capa_imagem']
    geral_capa_video = campanha['geral_capa_video']
    geral_dias_campanha = campanha['geral_dias_campanha']
    geral_data_fim = tratar_valor_data_null(campanha['geral_data_fim'])    
    geral_data_ini = tratar_valor_data_null(campanha['geral_data_ini'])
    
    geral_meta = tratar_valor_num_null(campanha['geral_meta'])
    geral_meta_corrigida = tratar_valor_num_null(campanha['geral_meta_corrigida'])
    geral_arrecadado = campanha['geral_arrecadado']
    geral_arrecadado_corrigido = campanha['geral_arrecadado_corrigido']
    geral_percentual_arrecadado = campanha['geral_percentual_arrecadado']
    geral_conteudo_adulto = campanha['geral_conteudo_adulto']
    geral_posts = campanha['geral_posts']
    geral_modalidade = campanha['geral_modalidade']
    modalidadecampanha_id=-1
    if geral_modalidade=='aon':
        modalidadecampanha_id=1
    elif geral_modalidade=='flex':
        modalidadecampanha_id=2
    elif geral_modalidade=='sub':
        modalidadecampanha_id=3

    geral_titulo = campanha['geral_titulo']
    geral_titulo = geral_titulo.replace("'", "''")
    geral_status = campanha['geral_status']
    statuscampanha_id=-1
    if geral_status=='successful':
        statuscampanha_id=1
    elif geral_status=='failed':
        statuscampanha_id=2
    elif geral_status=='published':
        statuscampanha_id=3
    elif geral_status=='waiting_funds':
        statuscampanha_id=4

    geral_total_contribuicoes = campanha['geral_total_contribuicoes']
    geral_total_apoiadores = campanha['geral_total_apoiadores']
    geral_sobre = campanha['geral_sobre']
    geral_sobre = geral_sobre.replace("'", "''")

 
    template = """
INSERT INTO Campanha (
	 campanha_id
	,origemdados_id
	,original_id
	,recompensas_menor_nominal
	,recompensas_menor_ajustado
	,recompensas_quantidade
	,autor_id
	,social_seguidores
	,social_newsletter
	,social_sub_contribuicoes_amigos
	,social_sub_novos_seguidores
	,social_sub_posts_projeto
	,social_projetos_contribuidos
	,social_projetos_publicados
	,municipio_id
	,geral_content_rating
	,geral_contributed_by_friends
	,geral_capa_imagem
	,geral_capa_video
	,geral_dias_campanha
	,geral_data_fim
	,geral_data_ini
	,geral_meta
	,geral_meta_corrigida
	,geral_arrecadado
	,geral_arrecadado_corrigido
	,geral_percentual_arrecadado
	,geral_conteudo_adulto
	,geral_posts
	,modalidadecampanha_id
	,geral_titulo
	,statuscampanha_id
	,geral_total_contribuicoes
	,geral_total_apoiadores
	,geral_sobre
)
SELECT  nextval('seq_campanha_id')
	,{origemdados_id}
	,'{original_id}'
	,{recompensas_menor_nominal}
	,{recompensas_menor_ajustado}
	,{recompensas_quantidade}
    ,(SELECT autor_id FROM Autor WHERE original_id='{autoria_id}' AND origemdados_id={origemdados_id})
    ,{social_seguidores}
    ,{social_newsletter}
    ,{social_sub_contribuicoes_amigos}
    ,{social_sub_novos_seguidores}
    ,{social_sub_posts_projeto}
    ,{social_projetos_contribuidos}
    ,{social_projetos_publicados}
    ,{municipio_id}
	,{geral_content_rating}
	,{geral_contributed_by_friends}
	,{geral_capa_imagem}
	,{geral_capa_video}
	,{geral_dias_campanha}
	,{geral_data_fim}
	,{geral_data_ini}
	,{geral_meta}
	,{geral_meta_corrigida}
	,{geral_arrecadado}
	,{geral_arrecadado_corrigido}
	,{geral_percentual_arrecadado}
	,{geral_conteudo_adulto}
	,{geral_posts}
	,{modalidadecampanha_id}
	,'{geral_titulo}'
	,{statuscampanha_id}
	,{geral_total_contribuicoes}
	,{geral_total_apoiadores}
	,'{geral_sobre}'

WHERE   NOT EXISTS (
    SELECT  1
    FROM    Campanha
    WHERE   origemdados_id={origemdados_id}
    AND     original_id='{original_id}'
)
    """

    sql = template.format(
        origemdados_id=origemdados_id
        ,original_id=geral_project_id
        ,recompensas_menor_nominal=recompensas_menor_nominal
        ,recompensas_menor_ajustado=recompensas_menor_ajustado
        ,recompensas_quantidade=recompensas_quantidade
        ,autoria_id=autoria_id
        ,social_seguidores=social_seguidores
        ,social_newsletter=social_newsletter
        ,social_sub_contribuicoes_amigos=social_sub_contribuicoes_amigos
        ,social_sub_novos_seguidores=social_sub_novos_seguidores
        ,social_sub_posts_projeto=social_sub_posts_projeto
        ,social_projetos_contribuidos=social_projetos_contribuidos
        ,social_projetos_publicados=social_projetos_publicados
        ,municipio_id=geral_city_id
    	,geral_content_rating=geral_content_rating
    	,geral_contributed_by_friends=geral_contributed_by_friends
    	,geral_capa_imagem=geral_capa_imagem
    	,geral_capa_video=geral_capa_video
    	,geral_dias_campanha=geral_capa_video
    	,geral_data_fim=geral_data_fim
    	,geral_data_ini=geral_data_ini
    	,geral_meta=geral_meta
    	,geral_meta_corrigida=geral_meta
    	,geral_arrecadado=geral_arrecadado
    	,geral_arrecadado_corrigido=geral_arrecadado_corrigido
    	,geral_percentual_arrecadado=geral_arrecadado_corrigido
    	,geral_conteudo_adulto=geral_conteudo_adulto
    	,geral_posts=geral_posts
    	,modalidadecampanha_id=modalidadecampanha_id
    	,geral_titulo=geral_titulo
    	,statuscampanha_id=statuscampanha_id
    	,geral_total_contribuicoes=geral_total_contribuicoes
    	,geral_total_apoiadores=geral_total_apoiadores
    	,geral_sobre=geral_sobre

        )
    return sql

'''
def executar_carga_campanhas(args)
'''
def executar_carga_campanhas(args):
    campanhas = []
    caminho_campanhas = f'{CAMINHO_NORMALIZADOS}/{args.ano}'
    logs.verbose(args.verbose, f'executar scripts pasta: {caminho_campanhas}')

    if not os.path.exists(caminho_campanhas):
        return False
    
    arquivos_campanhas = os.listdir(caminho_campanhas)

    con = duckdb.connect(f"{CAMINHO_NORMALIZADOS}/analises_{args.ano}.db")

    # Percorre a lista de arquivos
    for arq_campanha in arquivos_campanhas:
        # Cria o caminho completo para o file
        caminho_arq = os.path.join(caminho_campanhas, arq_campanha)

        if not os.path.isfile(caminho_arq):
            continue

        if not caminho_arq.endswith(".json"):
            continue
        
        # abrir arquivo
        f = open (caminho_arq, "r")
        
        # ler arquivo
        campanha = json.loads(f.read()) 
        sql = construir_comando_autor(campanha)
        con.sql(sql)
        sql = construir_comando_campanha(campanha)
        try:
            con.sql(sql)
        except ValueError:
            print(sql)

        # fechar arquivo
        f.close()

    return True

'''
async def executar_montarbd(args)
-- 
'''
async def executar_montarbd(args):
    p1 = datetime.now()

    caminho_arq = f"{CAMINHO_NORMALIZADOS}/analises_{args.ano}.db"

    print(f'montar banco de dados (duckdb): {caminho_arq}')

    if os.path.exists(caminho_arq):
        os.remove(caminho_arq) 

    executar_scripts_pasta(args, CAMINHO_SQL_CRIACAO)
    executar_scripts_pasta(args, CAMINHO_SQL_CARGA)

    executar_carga_campanhas(args)


    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args.verbose, f'Tempo: {tempo}s')
