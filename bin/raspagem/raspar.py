import asyncio
import logging

import raspagem.aasp as aasp
import raspagem.guia_dos_quadrinhos as guia
import raspagem.catarse as catarse
import raspagem.apoiase as apoiase

from datetime import datetime
#import raspagem.catarse

async def executar_raspagem(args):

    if args.verbose:
        print('preparando threads de raspagem', flush=True)
    threads = list()

    if args.verbose:
        print('thread: raspar aasp (A)', flush=True)
    threads.append(asyncio.create_task(aasp.raspar_aasp(args)))

    hoje = datetime.today()
    ano = 2011
    mes = 1
    while ano <= hoje.year:
        if args.verbose:
            print(f'thread: raspar guia dos quadrinhos: {ano} (B{ano})', flush=True)
        threads.append(asyncio.create_task(guia.raspar_guiaquadrinhos(args, ano)))
        ano = ano + 1

    if args.verbose:
        print('thread: raspar catarse (C)', flush=True)
    threads.append(asyncio.create_task(catarse.raspar_catarse(args)))

    if args.verbose:
        print('thread: raspar catarse categories', flush=True)
    threads.append(asyncio.create_task(catarse.raspar_catarse_categories(args)))

    if args.verbose:
        print('thread: raspar catarse cities', flush=True)
    threads.append(asyncio.create_task(catarse.raspar_catarse_cities(args)))

    if args.verbose:
        print('thread: raspar apoiase (D)', flush=True)
    threads.append(asyncio.create_task(apoiase.raspar_apoiase(args)))

    if args.verbose:
        print('raspando dados da web', flush=True)
    await asyncio.gather(*threads)
    print('\ndados raspados', flush=True)