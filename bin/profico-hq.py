import asyncio
import argparse
import raspagem.raspar

'''
async def raspar(args)
- acionar o módulo de raspagem de dados
'''
async def raspar(args):
    print("Executando o comando 'raspar'")

    await raspagem.raspar.executar_raspagem(args)

'''
async def normalizar(args)
- normalizar dados
'''
async def normalizar(args):
    print(f"Executando o comando 'normalizar' com o ano {args.ano}")

'''
async def reportar(args)
- reportar
'''
async def reportar(args):
    print(f"Executando o comando 'reportar' com o ano {args.ano}")


'''
async def main()
- parse da linha de comando
- acionamento de um dos comandos do profico:
-- raspar dados
-- normalizar
-- reportar
'''
async def main():
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

    # Subcomando 'reportar'
    parser_reportar = subparsers.add_parser("reportar"
                    , help="Gerar um relatório.")
    parser_reportar.add_argument('-v', '--verbose'
                    , action='store_true'
                    , help = 'opcional. modo verboso, registra atividade em console')  # on/off flag
    parser_reportar.add_argument('-l', '--loglevel'
                    , choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
                    , nargs='?'
                    , default='ERROR'
                    , help = 'opcional. nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL. default=ERROR')
    parser_reportar.add_argument("-a", "--ano"
                    , type=int
                    , required=True
                    , help="obrigatório. informe o ano limite para a geração do relatório.")
    parser_reportar.set_defaults(func=reportar)

    args = parser.parse_args()
    await args.func(args)

if __name__ == "__main__":
    asyncio.run(main())
