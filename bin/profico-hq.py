"""
Comandos disponíveis:
- raspar: obter dados nas fontes de dados
- normalizar: normalizar os dados, preparando para carga em banco de dados
- banco: montar o banco de dados em duckdb
- analisar: analisar os dados a partir do duckdb
"""

import asyncio
import argparse
import raspagem.raspar
import normalizacao.normalizar
import banco.bd
import analise.analisar
import logs

async def raspar(args):
    """
    async def raspar(args)
    - acionar o módulo de raspagem de dados
    """
    print("Executando o comando 'raspar'")
    logs.definir_log(args)

    await raspagem.raspar.executar_raspagem(args)

async def normalizar(args):
    """
    acionar o módulo de normalização de dados
    """
    print(f"Executando o comando 'normalizar' com o ano {args.ano}")
    logs.definir_log(args)

    await normalizacao.normalizar.executar_normalizacao(args)


async def montar_banco(args):
    """
    montar banco de dados
    """
    print(f"Executando o comando 'montar banco de dados' com o ano {args.ano}")
    logs.definir_log(args)

    await banco.bd.executar_montarbd(args)

async def analisar(args):
    """
    montar análises a partir de consultas no banco de dados
    """
    print(f"Executando o comando 'analisar' com o ano {args.ano}")
    logs.definir_log(args)

    await analise.analisar.executar_analise(args)


async def main():
    """
    executa o programa profico-hq:
    - parse da linha de comando
    - acionamento de um dos comandos do profico:
    -- raspar dados
    -- normalizar
    -- banco
    -- analisar
    """

    parser = argparse.ArgumentParser(
        prog = "profico-hq",
        description='Suite de processamento de campanhas de financiamento coletivo de histórias em quadrinhos')        
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando 'raspar'
    parser_raspar = subparsers.add_parser("raspar"
                    , help="Raspar os dados de fontes de dados na web")
    parser_raspar.add_argument('-v', '--verbose'
                    , action='store_true'
                    , help = 'opcional. modo verboso, registra atividade em console')  # on/off flag
    parser_raspar.add_argument('-l', '--loglevel'
                    , choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
                    , nargs='?'
                    , default='ERROR'
                    , help = 'opcional. nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL. default=ERROR')
    parser_raspar.add_argument('-c', '--clear-cache'
                    , action='store_true'
                    , help = 'opcional. forçar download de arquivos que já foram baixados em execuções anteriores')  # on/off flag
    parser_raspar.set_defaults(func=raspar)

    # Subcomando 'normalizar'
    parser_normalizar = subparsers.add_parser("normalizar"
                    , help="Normalizar os dados obtidos")
    parser_normalizar.add_argument('-v', '--verbose'
                    , action='store_true'
                    , help = 'opcional. modo verboso, registra atividade em console')  # on/off flag
    parser_normalizar.add_argument('-l', '--loglevel'
                    , choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
                    , nargs='?'
                    , default='ERROR'
                    , help = 'opcional. nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL. default=ERROR')
    parser_normalizar.add_argument("-a", "--ano"
                    , type=int
                    , required=True
                    , help="obrigatório. informe o ano limite para realizar a normalização dos dados.")
    parser_normalizar.set_defaults(func=normalizar)


    # Subcomando 'banco'
    parser_banco = subparsers.add_parser("banco"
                    , help="Montar banco de dados")
    parser_banco.add_argument('-v', '--verbose'
                    , action='store_true'
                    , help = 'opcional. modo verboso, registra atividade em console')  # on/off flag
    parser_banco.add_argument('-l', '--loglevel'
                    , choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
                    , nargs='?'
                    , default='ERROR'
                    , help = 'opcional. nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL. default=ERROR')
    parser_banco.add_argument("-a", "--ano"
                    , type=int
                    , required=True
                    , help="obrigatório. informe o ano limite para a construção do banco de dados.")
    parser_banco.set_defaults(func=montar_banco)


    # Subcomando 'analisar'
    parser_analisar = subparsers.add_parser("analisar"
                    , help="Gerar um relatório.")
    parser_analisar.add_argument('-v', '--verbose'
                    , action='store_true'
                    , help = 'opcional. modo verboso, registra atividade em console')  # on/off flag
    parser_analisar.add_argument('-l', '--loglevel'
                    , choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
                    , nargs='?'
                    , default='ERROR'
                    , help = 'opcional. nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL. default=ERROR')
    parser_analisar.add_argument("-a", "--ano"
                    , type=int
                    , required=True
                    , help="obrigatório. informe o ano limite para a geração do relatório.")
    parser_analisar.set_defaults(func=analisar)

    args = parser.parse_args()

    await args.func(args)

if __name__ == "__main__":
    asyncio.run(main())
