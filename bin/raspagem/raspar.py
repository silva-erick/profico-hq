import os
import asyncio
import logging
from datetime import datetime, timedelta

import logs
import raspagem.apoio as apoio
import raspagem.aasp as aasp
import raspagem.guia_dos_quadrinhos as guia
import raspagem.catarse as catarse
import raspagem.apoiase as apoiase

async def executar_raspagem(args):
    """
    async def executar_raspagem(args)
    - raspagem de dados das seguintes fontes:
    -- aasp, para tabela de correção monetária
    -- guia dos quadrinhos: fontes
    -- catarse
    -- 
    """

    p1 = datetime.now()

    logs.verbose(args, 'Início')

    threads = list()

    logs.verbose(args, 'thread: raspar aasp')

    threads.append(asyncio.create_task(aasp.raspar_aasp(args)))

    hoje = datetime.today()
    ano = 2011
    mes = 1
    while ano <= hoje.year:
        logs.verbose(args, f'thread: raspar guia dos quadrinhos: {ano}')
        threads.append(asyncio.create_task(guia.raspar_guiaquadrinhos(args, ano)))
        ano = ano + 1

    logs.verbose(args,'thread: raspar catarse')
    threads.append(asyncio.create_task(catarse.raspar_catarse(args)))

    logs.verbose(args,'thread: raspar catarse categories')
    threads.append(asyncio.create_task(catarse.raspar_catarse_categories(args)))

    logs.verbose(args,'thread: raspar catarse cities')
    threads.append(asyncio.create_task(catarse.raspar_catarse_cities(args)))

    logs.verbose(args,'thread: raspar apoiase')

    threads.append(asyncio.create_task(apoiase.raspar_apoiase(args)))

    logs.verbose(args,'raspando dados da web')
    await asyncio.gather(*threads)

    p2 = datetime.now()
    delta = p2-p1
    tempo = delta.seconds + delta.microseconds/1000000

    logs.verbose(args, f'Tempo: {tempo}s')
