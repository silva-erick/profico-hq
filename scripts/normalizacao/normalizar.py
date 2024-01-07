import argparse
import logging
from datetime import datetime
import os
import json

from bs4 import BeautifulSoup

import re


CAMINHO_NORMALIZADOS = "../../dados/normalizados"
CAMINHO_CONVERSAO_MONETARIA = "../../dados/brutos/aasp/conversao-monetaria.json"
CAMINHO_ALBUNS = "../../dados/brutos/guiadosquadrinhos/totais.json"
CAMINHO_MUNICIPIOS = "../../dados/brutos/catarse/cities.json"
CAMINHO_CAMPANHAS = "../../dados/brutos/catarse/campanhas"


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
            
        
class Normalizacao:
    def __init__(self, ano, verbose):
        self._ano = ano
        self._verbose = verbose

    def _carregar_carrapichos(self):
        self._carrapichos = {}
        self._carrapichos['Festivais'] = re.compile(r'festiva(l|is)')
        self._carrapichos['Salões de Humor'] = re.compile(r'sal[aã]o(\s*internacional){0,1}\s*d[eo]\w*humor')
        self._carrapichos['HQMIX'] = re.compile(r'hqmix')
        self._carrapichos['CCXP'] = re.compile(r'ccxp')
        self._carrapichos['FIQ'] = re.compile(r'fiq|festival\s*internacional\s*de\s*quadrinhos')
        self._carrapichos['Ângelo Agostini'] = re.compile(r'gelo[\s\\\w]+agostini')
        self._carrapichos['Política'] = re.compile(r'ministr|minist[eé]rio|president|governador|prefeit[oa]|pol[ií]ti|economia|capitalis|comunis[tm]|socialis|anarquis|esquerdis|direitis|reacion[aá]|reaça|autoritari|ditadura|autogest|libertarian')
        self._carrapichos['Questões de Gênero'] = re.compile(r'machis|feminis|sexismo|empoderamento\s*feminino|direito\s*feminino|direito\*d(e|a|as)\s*mulheres|viol[eê]ncia\s*dom[eé]stica|cultura\s*patriarcal|masculinidade\s*t[oóxica]|feminic[ií]dio|consentimento|(pap[eé]is|normas|estudos*|igualdade|estereótipos*|diversidade|identidade|discriminação)\s*de\s*g[eê]nero')
        self._carrapichos['LGBTQIA+'] = re.compile(r'homos+exual|bis+exual|trans+exual|pans+exual|transg[eê]ner|\bace\b|as+sexual|ag[eê]nero|big[eê]nero|n[aã]o[\s-]*binário|traveco|travesti|she-*her|gay|sapat[aã]o|s[aá]fico|l[eé]sbica|queer|aliado|sa[ií](r|da)\s*d[eo]\s*arm[aá]rio|espa[çc]o\s*seguro|homofobia|transfobia|lesbofobia|orienta[cç][aã]o\s*sexual|(pap[eé]is|normas|estudos*|igualdade|estereótipos*|diversidade|identidade|discriminação)\s*de\s*g[eê]nero')
        self._carrapichos['Terror'] = re.compile(r'terror|horror|suspense|sobrenatural|monstro|kaiju|godzila|vampir|lobisomem|zumb[oô]|assassin|corpo\s*seco|m[uú]mia|fantasma|morto|esp[ií]rit|zumbi|zombi|zombie|pos+es+[aã]o|dem[oôó]io|demon[ií]ac|slasher|arrepio|lovecraft|sinistr|claustrofobia|desespero|tens[aã]o|assobrad|sombri[ao]|cemit[eé]rio|abandonad|macabro|medo|desconhecido|as+ustador|maldit[ao]|maldi[çc][ãa]o|apocalipse|distopia')
        self._carrapichos['Humor'] = re.compile(r'piada|humor|c[oôó]mic[oa]|comicidade|risada|engra[cç]ad|gozad[ao]|divertid|z[ou][eê]i*ra')
        self._carrapichos['Heróis'] = re.compile(r'her[oó]i|hero[íi]na|super[\s\-]*poder|super[\s\-]*vil|inimigo')
        self._carrapichos['Luta'] = re.compile(r'luta|combate|oponente|derrota')
        self._carrapichos['Guerra'] = re.compile(r'guerra|conflito|derrota|disputa|conflito|vit[oó]ria')
        self._carrapichos['Gêneros'] = re.compile(r'suspense|\bconto|romance|novela|graphic novel|biografia|fic[çc][aã]o|fantasia|\bmang[áa]\b')
        self._carrapichos['Ficção Científica'] = re.compile(r'rob[ôóo]|andr[oó]id|tecnologia|cyber|ciber|zumb[oô]|planeta|viage[nm]\s*espacial|astronauta|cosmonauta|taikonauta|planeta|space\s*opera|computador|intelig[êe]ncia\s*artificial|i\.a\.|a\.i\.|apocalipse|distopia')
        self._carrapichos['Fantasia'] = re.compile(r'aventura|saga|elfo|elfa|troll|m[aá]gico|magia|feiticeir|feiti[çc]|castelo|cavaleir|drag[ãa]o|duend|cavalaria|espada|escudo|\blança\b|arqueir')
        self._carrapichos['Folclore'] = re.compile(r"saci|mula[\s*-]sem[\s*-]cabe|corpo\s*seco|lobisomem|assombra[çc][ãa]|sereia|m[ãa]e\s*d['a]\s*[áa]gua|supersti|loira\s*do|\blenda|cuca|mito\b|mitologia|cemit[ée]rio")
        self._carrapichos['Zine'] = re.compile(r'zine')
        self._carrapichos['WebFormatos'] = re.compile(r'web[\s\-]*(comic|quadrinh|tirinh|zine|toon)')
        self._carrapichos['Erotismo'] = re.compile(r'er[oó]tic|porn[oô]|sad[oô][-\s]mas[oô]|sadomasoquist|bdsm|\+18|18\+|sexo|sexualidade|sacanagem|putaria|gozar|posi[çc][aã]o\s*sexual|fantasia|desejo|libido')
        self._carrapichos['Religiosidade'] = re.compile(r'cat[óo]lic|crist[ãa]o|gospel|evangelho|\bdeus|santifica|evang[eé]li[zc]|\bbuda\b|budism|bramanism|jesus|\b[ij]av[eé]h*\b|\breza|bendito|bendizer|premoni|profecia|profeta|b[íi]blia|\btor[aá]\b|alco+r[ãa]o|m[ií]stico|misticismo|sobrenatural|pajé|pa[gj]elan|orix[aá]|macumba|umbanda|candonbl|terreiro|oculto|ocultismo')
        self._carrapichos['Jogos'] = re.compile(r'jogo|\bgame\b|tabuleiro|board|xadrez|gam[ãa]o|cartas|card\b|disputa|conflito|vit[oó]ria')
        RE_POLITICA = r''

    def _carregar_json(self, caminho):
        result = {}
        result['sucesso'] = False
        try:
            f = open(caminho, "r")

            # Reading from file
            result['json'] = json.loads(f.read())

            result['sucesso'] = True
        except Exception as e:
            # Lidar com a exceção, se necessário
            log_verbose(self._verbose, f"Erro ao ler o arquivo: {e}")

        finally:
            # Certifique-se de fechar o arquivo, mesmo em caso de exceção
            if f:
                f.close()

            return result

    def _carregar_conversao_monetaria(self):
        result = self._carregar_json(CAMINHO_CONVERSAO_MONETARIA)
        if result['sucesso']:
            self._conversao_monetaria = result['json']
            # existe data de dezembro do ano selecionado?
            ano = str(self._ano * 100 + 12)
            if (not ano in self._conversao_monetaria) or (self._conversao_monetaria[ano] is None):
                log_verbose(self._verbose, f"Não existe conversão de valores monetários em dezembro/{self._ano}")
                result['sucesso'] = False
        return result['sucesso']

    def _carregar_albuns(self):
        result = self._carregar_json(CAMINHO_ALBUNS)
        if result['sucesso']:
            self._albuns = result['json']
        return result['sucesso']

    def _carregar_municipios(self):
        result = self._carregar_json(CAMINHO_MUNICIPIOS)
        if result['sucesso']:
            self._municipios = result['json']
        return result['sucesso']

    def _ajustar_valor(self, ano_ini, mes_ini, valor_ini, ano_fim, mes_fim):
        anomes_ini = str(ano_ini * 100 + mes_ini)
        anomes_fim = str(ano_fim * 100 + mes_fim)

        if valor_ini is None:
            return valor_ini

        return (valor_ini/self._conversao_monetaria[anomes_ini]) * self._conversao_monetaria[anomes_fim]

    def _carregar_campanhas(self):
        if not os.path.exists(CAMINHO_CAMPANHAS):
            return False
        
        caminho_campanhas = os.listdir(CAMINHO_CAMPANHAS)

        quantidade_campanhas = 0

        self._campanhas = []

        # Percorre a lista de arquivos
        for caminho_campanha in caminho_campanhas:
            # Cria o caminho completo para o file
            full_path = os.path.join(CAMINHO_CAMPANHAS, caminho_campanha)
            
            # Verifica se o caminho é um arquivo
            if os.path.isfile(full_path) and full_path.endswith(".json"):
                # abrir arquivo
                f = open (full_path, "r")
                
                # ler arquivo como json
                data = json.loads(f.read())

                # fechar arquivo
                f.close()

                # verificar a data de lançamento da campanha
                try:
                    data_obj = parse_data(data['detail']['online_date'])
                except ValueError:
                    print(f"data original: {data['detail']['online_date']}")
                    raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

                if data_obj.year <= self._ano:
                    self._campanhas.append(data)
                else:
                    continue

                quantidade_campanhas = quantidade_campanhas + 1

                if self._verbose and ((quantidade_campanhas % 25) == 0):
                    print('.', end='', flush=True)

        print('.')
        log_verbose(self._verbose, f'Campanhas encontradas: {quantidade_campanhas}')
        return True
    
    def _garantir_pastas_normalizacao(self):
        log_verbose(self._verbose, f"Verificando pasta: {CAMINHO_NORMALIZADOS}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}"):
            log_verbose(self._verbose, f"\tCriando pasta: {CAMINHO_NORMALIZADOS}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}")
        log_verbose(self._verbose, f"Verificando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
        if not os.path.exists(f"{CAMINHO_NORMALIZADOS}/{self._ano}"):
            log_verbose(self._verbose, f"\tCriando pasta: {CAMINHO_NORMALIZADOS}/{self._ano}")
            os.mkdir(f"{CAMINHO_NORMALIZADOS}/{self._ano}")

        return True

    def _percorrer_campanhas(self, msg, funcao):
        log_verbose(self._verbose, msg)
        quantidade_campanhas = 0
        res = True
        for data in self._campanhas:

            res = funcao(data)
            if not res:
                break

            quantidade_campanhas = quantidade_campanhas + 1

            if self._verbose and ((quantidade_campanhas % 25) == 0):
                print('.', end='', flush=True)

        print('.')
        return res

    def _ajustar_valores_campanha(self, data):
        # verificar a data de lançamento da campanha
        try:
            data_obj = parse_data(data['detail']['online_date'])
        except ValueError:
            print(f"data original: {data['detail']['online_date']}")
            raise ValueError(f"Formato de data inválido. {data['detail']['online_date']}")

        # ajustar goal e pledged para valor presente
        data['detail']['goal_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['goal'], self._ano, 12)
        data['detail']['pledged_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, data['detail']['pledged'], self._ano, 12)

        # ajustar valores das recompensas
        for reward in data['rewards']:
            reward['minimum_value_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['minimum_value'], self._ano, 12)
            #reward['maximum_contributions_ajustado'] = self._ajustar_valor(data_obj.year, data_obj.month, reward['maximum_contributions'], self._ano, 12)
        return True

    def _ajustar_valor_about(self, data):
        # converter texto de about the HTML (com tags) para TEXT (texto puro, sem marcação)
        about_html = data['detail']['about_html']
        soup = BeautifulSoup(about_html, 'html.parser')
        about_txt = soup.get_text(separator=' ', strip=True)
        data['detail']['about_txt'] = about_txt

        return True
    
    def _testar_regex_hashtag(self, text, pattern):
        if not (pattern.search(text) is None):
            return True
        else:
            return False


    def _categorizar_hashtags(self, data):
        about_txt = data['detail']['about_txt'].lower()
        data["analises_categorias"]={}

        for k, r in self._carrapichos.items():
            data['analises_categorias'][k] = self._testar_regex_hashtag(about_txt, r)

        return True

    def _categorizar_recompensas(self, data):
        about_txt = data['detail']['about_txt'].lower()
        data["analises_recompensas"]={}

        menor_ajustado = 10000000000
        menor = menor_ajustado
        for reward in data['rewards']:
            valor_ajustado = float(reward['minimum_value_ajustado'])
            if valor_ajustado < menor_ajustado:
                menor_ajustado = valor_ajustado
            valor = float(reward['minimum_value'])
            if valor < menor:
                menor = valor

        data["analises_recompensas"]['menor_nominal'] = menor
        data["analises_recompensas"]['menor_ajustado'] = menor_ajustado

        return True

    def _gravar_json_campanhas(self, data):
        arquivo_dados = f"{CAMINHO_NORMALIZADOS}/{self._ano}/{data['detail']['project_id']}.json"
        with open(arquivo_dados, 'w') as arquivo_json:
            json.dump(data, arquivo_json)

        return True

    def executar(self):
        log_verbose(self._verbose, "Carregar regex de categorização")
        norm._carregar_carrapichos()

        log_verbose(self._verbose, "Carregar arquivos de apoio")
        result = (self._carregar_conversao_monetaria()
                and self._carregar_albuns()
                and self._carregar_municipios()
        )
        
        log_verbose(self._verbose, "Carregar campanhas")
        result = (result and self._carregar_campanhas()
                and self._garantir_pastas_normalizacao()
                and self._percorrer_campanhas(f'Ajustar valores das campanhas para dez/{self._ano}', self._ajustar_valores_campanha)
                and self._percorrer_campanhas(f'Texto de apresentação: HTML -> Texto', self._ajustar_valor_about)
                and self._percorrer_campanhas(f'Categorizar hashtags', self._categorizar_hashtags)
                and self._percorrer_campanhas(f'Gravar arquivos normalizados das campanhas', self._gravar_json_campanhas)
        )



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "normalizar",
        description='Padronizar os dados das campanhas para facilitar as análises')
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
    log_filename = f"log/aasp{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    if args.verbose:
        print(f"Processar campanhas até {args.ano}")
        print(f"ATENÇÃO, os valores monetários serão ajustados para dezembro/{args.ano}")

    norm = Normalizacao(args.ano, args.verbose)
    norm.executar()