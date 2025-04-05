import os
import logging
from datetime import datetime, timedelta

def definir_log(args, comando):

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
    log_filename = f"log/{comando}_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)
    
    
def verbose(verbose, msg):
    logging.debug(msg)
    if verbose:
        print(msg, flush=True)
    
    
def verboseerror(msg, e = None):
    if e is None:
        logging.error(msg)
    else:
        logging.error(msg, exc_info=e)
    print(msg, flush=True)
