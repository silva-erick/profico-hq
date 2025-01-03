import logging
import os
from datetime import datetime


import threading

import raspagem.aasp
import raspagem.guia_dos_quadrinhos
import raspagem.catarse

def executar_raspagem(args):
    if not os.path.exists("../log"):
        os.makedirs("../log")
    log_filename = f"../log/raspar_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"


    threads = list()

    funcoes = [
        raspagem.aasp.raspar_aasp
        , raspagem.guia_dos_quadrinhos.raspar_guiaquadrinhos
        , raspagem.catarse.raspar_catarse
    ]

    for index, funcao in enumerate(funcoes):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=funcao, args=(args,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)