import asyncio
import argparse
import raspagem.raspar

async def raspar(args):
    print("Executando o comando 'raspar'")

    await raspagem.raspar.executar_raspagem(args)

async def normalizar(args):
    print(f"Executando o comando 'normalizar' com o ano {args.ano}")

async def reportar(args):
    print(f"Executando o comando 'reportar' com o ano {args.ano}")



async def main():
    parser = argparse.ArgumentParser(
        prog = "profico-hq",
        description='Suite de processamento de campanhas de financiamento coletivo de histórias em quadrinhos')        
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando 'raspar'
    parser_raspar = subparsers.add_parser("raspar", help="Raspar os dados de fontes de dados na web")
    parser_raspar.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser_raspar.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'], nargs='?', default='ERROR')
    parser_raspar.add_argument('-c', '--clear-cache',
                    action='store_true')  # on/off flag
    parser_raspar.set_defaults(func=raspar)

    # Subcomando 'normalizar'
    parser_normalizar = subparsers.add_parser("normalizar", help="Normalizar os dados obtidos")
    parser_normalizar.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser_normalizar.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    parser_normalizar.add_argument("-a", "--ano", type=int, required=True, help="Ano para normalizar os dados.")
    parser_normalizar.set_defaults(func=normalizar)

    # Subcomando 'reportar'
    parser_reportar = subparsers.add_parser("reportar", help="Gerar um relatório.")
    parser_reportar.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser_reportar.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    parser_reportar.add_argument("-a", "--ano", type=int, required=True, help="Ano para gerar o relatório.")
    parser_reportar.set_defaults(func=reportar)

    args = parser.parse_args()
    await args.func(args)

if __name__ == "__main__":
    #main()
    asyncio.run(main())


    # if not os.path.exists("log"):
    #     os.makedirs("log")
    # log_filename = f"log/normalizar_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    # logging.basicConfig(
    #     format='%(asctime)s %(levelname)-8s %(message)s',
    #     level=log_level,
    #     filename=log_filename,
    #     datefmt='%Y-%m-%d %H:%M:%S')
    # logging.getLogger().setLevel(log_level)

    # if args.verbose:
    #     print(f"Processar campanhas até {args.ano}")
    #     print(f"ATENÇÃO, os valores monetários serão ajustados para dezembro/{args.ano}")

    # norm = Normalizacao(args.ano, args.verbose)
    # norm.executar()