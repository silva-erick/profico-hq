import os
import asyncio
import logging
from datetime import datetime, timedelta

import raspagem.apoio as apoio
import raspagem.aasp as aasp
import raspagem.guia_dos_quadrinhos as guia
import raspagem.catarse as catarse
import raspagem.apoiase as apoiase


async def executar_raspagem(args):

    apoio.definir_log(args, 'raspar')

    apoio.verbose(args.verbose, f'Início: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}')

    threads = list()

    apoio.verbose(args.verbose, 'thread: raspar aasp (A)')

    threads.append(asyncio.create_task(aasp.raspar_aasp(args)))

    hoje = datetime.today()
    ano = 2011
    mes = 1
    while ano <= hoje.year:
        apoio.verbose(args.verbose, f'thread: raspar guia dos quadrinhos: {ano} (B{ano})')
        threads.append(asyncio.create_task(guia.raspar_guiaquadrinhos(args, ano)))
        ano = ano + 1

    apoio.verbose(args.verbose,'thread: raspar catarse (C)')
    threads.append(asyncio.create_task(catarse.raspar_catarse(args)))

    apoio.verbose(args.verbose,'thread: raspar catarse categories')
    threads.append(asyncio.create_task(catarse.raspar_catarse_categories(args)))

    apoio.verbose(args.verbose,'thread: raspar catarse cities')
    threads.append(asyncio.create_task(catarse.raspar_catarse_cities(args)))

    apoio.verbose(args.verbose,'thread: raspar apoiase (D)')

    threads.append(asyncio.create_task(apoiase.raspar_apoiase(args)))

    apoio.verbose(args.verbose,'raspando dados da web')
    await asyncio.gather(*threads)

    apoio.verbose(args.verbose, f'Fim: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}')

