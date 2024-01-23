import argparse
import logging
from datetime import datetime, timedelta
import os

import re

import pandas as pd

import analises.descritivo as descr

CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CSV = "../../dados/csv"

REGEX_PRIMEIRO_NOME = re.compile('^[\w]+$')

from datetime import datetime, timedelta

def calcular_diferenca_dias(data_inicial_str, data_final_str):
    # Converter as strings em objetos datetime
    data_inicial = datetime.fromisoformat(data_inicial_str.replace('Z', ''))
    
    if data_final_str is None or data_final_str == '':
        # Se a data final for None, use a data atual
        data_final = datetime.utcnow()
    else:
        data_final = datetime.fromisoformat(data_final_str.replace('Z', ''))
    
    # Calcular a diferença em dias
    diferenca = data_final - data_inicial
    
    # Extrair a parte dos dias da diferença
    diferenca_em_dias = diferenca.days
    
    return diferenca_em_dias

def log_verbose(verbose, msg):
    if verbose:
        print(msg)
    logging.debug(msg)

def parse_data(data_str):
    try:
        # Tenta converter com fração de segundo
        data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%f')
        return data_obj
    except ValueError:
        try:
            # Tenta converter sem fração de segundo
            data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            return data_obj
        except ValueError:
            raise ValueError("Formato de data inválido.")
    
class AnaliseCsv:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose

    def _realizar_analise_descritiva(self, df):
        processos = [
            {'Modalidade': {'arq': 'sint_resumo_por_modalidade', 'func': descr.calcular_resumo_por_modalidade}},
            {'Plataforma': {'arq':'sint_resumo_por_origem_modalidade', 'func': descr.calcular_resumo_por_origem_modalidade}},
            {'Unidade Federativa': {'arq': 'sint_resumo_por_ufbr', 'func': descr.calcular_resumo_por_ufbr}},
            {'Gênero': {'arq': 'sint_resumo_por_genero', 'func': descr.calcular_resumo_por_genero}},
            #{'Autoria': {'arq': 'sint_resumo_por_autoria', 'func': descr.calcular_resumo_por_autoria}},
            {'Menções: Ângelo Agostini': {'arq': 'sint_resumo_por_mencoes_angelo_agostini', 'func': descr.calcular_resumo_por_mencoes_angelo_agostini}},
            {'Menções: CCXP': {'arq': 'sint_resumo_por_mencoes_ccxp', 'func': descr.calcular_resumo_por_mencoes_ccxp}},
            {'Menções: Disputa': {'arq': 'sint_resumo_por_mencoes_disputa', 'func': descr.calcular_resumo_por_mencoes_disputa}},
            {'Menções: Erotismo': {'arq': 'sint_resumo_por_mencoes_erotismo', 'func': descr.calcular_resumo_por_mencoes_erotismo}},
            {'Menções: Fantasia': {'arq': 'sint_resumo_por_mencoes_fantasia', 'func': descr.calcular_resumo_por_mencoes_fantasia}},
            {'Menções: Ficcao Científica': {'arq': 'sint_resumo_por_mencoes_ficcao_cientifica', 'func': descr.calcular_resumo_por_mencoes_ficcao_cientifica}},
            {'Menções: FIQ': {'arq': 'sint_resumo_por_mencoes_fiq', 'func': descr.calcular_resumo_por_mencoes_fiq}},
            {'Menções: Folclore': {'arq': 'sint_resumo_por_mencoes_folclore', 'func': descr.calcular_resumo_por_mencoes_folclore}},
            {'Menções: Herois': {'arq': 'sint_resumo_por_mencoes_herois', 'func': descr.calcular_resumo_por_mencoes_herois}},
            {'Menções: HQMIX': {'arq': 'sint_resumo_por_mencoes_hqmix', 'func': descr.calcular_resumo_por_mencoes_hqmix}},
            {'Menções: Humor': {'arq': 'sint_resumo_por_mencoes_humor', 'func': descr.calcular_resumo_por_mencoes_humor}},
            {'Menções: Jogos': {'arq': 'sint_resumo_por_mencoes_jogos', 'func': descr.calcular_resumo_por_mencoes_jogos}},
            {'Menções: LGBTQIA+': {'arq': 'sint_resumo_por_mencoes_lgbtqiamais', 'func': descr.calcular_resumo_por_mencoes_lgbtqiamais}},
            {'Menções: Mídia Independente': {'arq': 'sint_resumo_por_mencoes_midia_independente', 'func': descr.calcular_resumo_por_mencoes_midia_independente}},
            {'Menções: Política': {'arq': 'sint_resumo_por_mencoes_politica', 'func': descr.calcular_resumo_por_mencoes_politica}},
            {'Menções: Questões de Gênero': {'arq': 'sint_resumo_por_mencoes_questoes_genero', 'func': descr.calcular_resumo_por_mencoes_questoes_genero}},
            {'Menções: Religiosidade': {'arq': 'sint_resumo_por_mencoes_religiosidade', 'func': descr.calcular_resumo_por_mencoes_religiosidade}},
            {'Menções: Salões de Humor': {'arq': 'sint_resumo_por_mencoes_saloes_humor', 'func': descr.calcular_resumo_por_mencoes_saloes_humor}},
            {'Menções: Terror': {'arq': 'sint_resumo_por_mencoes_terror', 'func': descr.calcular_resumo_por_mencoes_terror}},
            {'Menções: Webformatos': {'arq': 'sint_resumo_por_mencoes_webformatos', 'func': descr.calcular_resumo_por_mencoes_webformatos}},
            {'Menções: Zine': {'arq': 'sint_resumo_por_mencoes_zine', 'func': descr.calcular_resumo_por_mencoes_zine}},
        ]

        mapa_titulo = {}
        analise_md = []
        i = 1
        pasta = f'{CAMINHO_CSV}/{self._ano}/analise_descritiva'
        if not os.path.exists(pasta):
            os.mkdir(pasta)
        pasta = f'{CAMINHO_CSV}/{self._ano}/analise_descritiva/dados'
        if not os.path.exists(pasta):
            os.mkdir(pasta)
        for it in processos:
            for k,v in it.items():
                funcao_mapeada = v['func']
                nome_arquivo = v['arq']
                mapa_titulo[nome_arquivo] = k
                if not os.path.exists(pasta):
                    os.mkdir(pasta)
                res = funcao_mapeada(df, self._ano, pasta, nome_arquivo, analise_md)
                print(f'\t.{i}: {k}: {res}')
                i = i + 1
                if not res:
                    return False
                
        with open(f'analise-descritiva.template.md', 'r', encoding='utf8') as arq_template_analise_descritiva:
            template_analise_descritiva = arq_template_analise_descritiva.read()
                
        with open(f'analise-descritiva-modalidade.template.md', 'r', encoding='utf8') as arq_template_analise_descritiva_modalidade:
            template_analise_descritiva_modalidade = arq_template_analise_descritiva_modalidade.read()
                
        with open(f'analise-descritiva-outros.template.md', 'r', encoding='utf8') as arq_template_analise_descritiva_outros:
            template_analise_descritiva_outros = arq_template_analise_descritiva_outros.read()

        with open(f'{CAMINHO_CSV}/{self._ano}/analise_descritiva/README.md', 'w', encoding='utf8') as f:
            f.write(f'{template_analise_descritiva}\n')

            for it in analise_md:
                for k,v in it.items():
                    titulo = mapa_titulo[k]
                    caminho = f'./{k}.md'
                    f.write(f'[{titulo}]({caminho})\n\n')

                    with open(f'{CAMINHO_CSV}/{self._ano}/analise_descritiva/{k}.md', 'w', encoding='utf8') as md_descritivo:
                        if k == 'sint_resumo_por_modalidade':
                            md_descritivo.write(f'{template_analise_descritiva_modalidade.replace("$(nome_dimensao)", mapa_titulo[k])}')
                        else:
                            md_descritivo.write(f'{template_analise_descritiva_outros.replace("$(nome_dimensao)", mapa_titulo[k])}')

                        md_descritivo.write('\n')
                        md_descritivo.write(f'{v}')
                        md_descritivo.write('\n')

                        md_descritivo.close()


            f.close()

    def _analisar_campanhas(self):
        self._show_message('> arquivos individuais')

        pasta_normalizados = f'{CAMINHO_NORMALIZADOS}/{self._ano}'
        if not os.path.exists(pasta_normalizados):
            return False
        
        df = pd.read_csv(f'{CAMINHO_CSV}/{self._ano}/campanhas_{self._ano}.csv', sep=';', decimal=',')

        print(f'campanhas: {len(df)}')

        self._realizar_analise_descritiva(df)


        return True
    
    


    def _garantir_pastas(self):
        self._show_message('Verificando pastas')
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
            return False
        log_verbose(self._verbose, f"> pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            return False

        log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}")
        if not os.path.exists(f"{CAMINHO_CSV}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}")
            os.mkdir(f"{CAMINHO_CSV}")
        log_verbose(self._verbose, f"> pasta: {CAMINHO_CSV}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_CSV}/{self._ano}"):
            log_verbose(self._verbose, f"\tcriando pasta: {CAMINHO_CSV}/{self._ano}")
            os.mkdir(f"{CAMINHO_CSV}/{self._ano}")

        return True
    
    def _show_message(self, msg):
        log_verbose(self._verbose, msg)
        return True

    def executar(self):
        result = True

        self._campanhas = []
        
        result = (result
            and self._show_message("Carregando arquivos campanhas")
            and self._garantir_pastas()
            and self._analisar_campanhas()
        )
            



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "análises",
        description='Exportar os dados como CSV, XLSX e Gráficos')
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], required=False)
    # Adiciona o argumento obrigatório -a/--ano
    parser.add_argument('-a', '--ano', type=int, required=True, help='Ano limite para consolidação')
    
    args = parser.parse_args()

    log_level = logging.WARNING
    if args.loglevel == 'CRITICAL':
        log_level = logging.CRITICAL
    elif args.loglevel =='ERROR':
        log_level = logging.ERROR
    elif args.loglevel =='WARNING':
        log_level = logging.WARNING
    elif args.loglevel =='INFO':
        log_level = logging.INFO
    elif args.loglevel =='DEBUG':
        log_level = logging.DEBUG

    if not os.path.exists("log"):
        os.makedirs("log")
    log_filename = f"log/analises_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    if args.verbose:
        print(f"Processar campanhas até {args.ano}")

    arquivo_csv = AnaliseCsv(args.ano, args.verbose)
    arquivo_csv.executar()