import requests
import logging
import http.client
import re
from datetime import datetime
import json
import os

import argparse

import apoio

BATCH_SIZE = 5

URL_QUADRINHOS = "https://apoia.se/explore/Quadrinhos"
URL_PROJECTS = "https://0hnipmgv3i.execute-api.us-east-1.amazonaws.com/prod/search"

class BaseApoiaseCollectionApi:
    batch_size = 9
    def __init__(self):
        self.batch_size = self._get_batch_size()

    def _get_headers(self):
        headers = {
            #':authority': '0hnipmgv3i.execute-api.us-east-1.amazonaws.com',
            #':method': 'POST',
            #':path': '/prod/search',
            #':scheme': 'https',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,en-GB;q=0.6',
            'Content-Length': '332',
            'Content-Type': 'application/json',
            'Origin': 'https://apoia.se',
            'Referer': 'https://apoia.se/',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'X-Api-Key': 'P77Evmby047IuFW5M8C8N9eTSCsGlk7I6xGnqcvm',
        }
        return headers
    
    def _get_url(self):
        return ''
    
    def _get_params(self):
        return {}
    
    def _get_batch_size(self):
        return BATCH_SIZE
    
    def _get_header_path(self):
        return ''
    
    def execute(self, verbose = False, log_level = logging.WARNING):
        # allow headers starting with :
        http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch

        # if verbose:
        #     http.client.HTTPConnection.debuglevel = 1

        # allows logging
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(log_level)
        requests_log.propagate = True

        batch_size = self._get_batch_size()
        headers = self._get_headers()
        params = self._get_params(1, 0)
        url = self._get_url()

        all_items = []
        offset = 0

        #session = requests.Session()
        total_time = 0
        num_of_calls = 0
        longest_call = 0
        success = False

        result = apoio.ResultadoApi(False)

        cache_slug = {}

        try:
            logging.debug(f"Items will be fetched in batches of {batch_size}")
            while True:
                if verbose:
                    print(":", end='', flush=True)

                p1 = datetime.now()
                params = self._get_params(num_of_calls+1, (num_of_calls+1)*BATCH_SIZE)
                payload=json.loads(params)
                response = requests.post(url=url, headers=headers, json=payload)
                num_of_calls = num_of_calls + 1
                p2 = datetime.now()
                delta = p2-p1
                if delta.microseconds > longest_call:
                    longest_call = delta.seconds * 1000000 + delta.microseconds

                total_time = total_time + delta.microseconds

                if response.status_code == 200 or response.status_code == 206:
                    batch_campaigns_temp = response.json()
                    if not batch_campaigns_temp:
                        success = True
                        break  # no items found

                    batch_campaigns = batch_campaigns_temp['message']['campaigns']
                    for camp in batch_campaigns:
                        slug = camp['slug']
                        if slug in cache_slug:
                            camp['complemento'] = cache_slug[slug]
                        else:
                            response2 = requests.get(url=f'https://apoia.se/api/v1/users/{slug}')
                            cache_slug[slug] = json.loads(response2.text)
                            camp['complemento'] = cache_slug[slug]

                    all_items.extend(batch_campaigns)
                    offset += batch_size
                    if len(batch_campaigns) < batch_size:
                        success = True
                        break
                    if not batch_campaigns:
                        success = True
                        break  # no items found
                elif response.status_code == 416:
                    success = True
                    break
                else:
                    result.add_request_error(response.status_code, response.text)
                    if verbose:
                        print("")
                        print(f"Request error: {response.status_code} - {response.text}")
                    break

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            if verbose:
                print("")
                print(f"Request exception: {e}")

        if num_of_calls == 0:
            avg_call = 0
        else:
            avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class ApoiaseProjects(BaseApoiaseCollectionApi):
    def __init__(self, verbose=False, log_level=logging.WARNING):
        self._url = ''
        self._verbose = verbose
        self._log_level = log_level

    def _get_url(self):
        return URL_PROJECTS
    
    def _get_params(self, page, start):
        res = '{"page":$(page),"category":"Quadrinhos","limit":$(batchsize),"count":true,"fields":{"_id":1,"name":1,"fundingFrequency":1,"fundingModel":1,"slug":1,"username":1,"about":1,"categories":1,"goals":1,"isScheduledSupport":1,"supports":1,"privateValues":1,"privateSupportersNumber":1,"linkedCampaigns":1,"social":1,"dueDate":1,"users":1,"status":1},"start":$(start)}'
        res = res.replace('$(page)', str(page))
        res = res.replace('$(start)', str(start))
        res = res.replace('$(batchsize)',str(BATCH_SIZE))
        return res
        
    
    def _get_batch_size(self):
        return 5
    
    def _get_header_path(self):
        return '/prod/search'
    
    def execute(self):
        res = super().execute(self._verbose, self._log_level)
        if not res.sucesso:
            print("?", end='')
        else:
            pass

        return res

def collect_apoiase(verbose):
    if not os.path.exists("../../dados/brutos/apoiase"):
        os.makedirs("../../dados/brutos/apoiase")
    if not os.path.exists("../../dados/brutos/apoiase/campanhas"):
        os.makedirs("../../dados/brutos/apoiase/campanhas")

    api_projetos = ApoiaseProjects(verbose, log_level)

    logging.debug(f"Preparing to access apoiase.me")
    res = api_projetos.execute()
    
    logging.info(f"Data fetched")

    if verbose:
        print("")
        print("summary:")
        print(f"\tsuccess: {res.sucesso}")
        print(f"\titems: {res.itens}")
        print(f"\ttotal time: {res.tempo_total}us")
        print(f"\taverage call: {res.tempo_medio}us")
        print(f"\tlongest_call: {res.chamada_mais_longa}")

    for it in res.resultado:
        if os.path.exists(f"../../dados/brutos/apoiase/resumocampanhas/{it['_id']}.json"):
            os.remove(f"../../dados/brutos/apoiase/resumocampanhas/{it['_id']}.json")
        data_file = f"../../dados/brutos/apoiase/resumocampanhas/{it['_id']}.json"
        with open(data_file, 'w') as json_file:
            json.dump(it, json_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "raspar_apoiase.py",
        description='Obtém dados de campanhas de financiamento coletivo dos sites monitorados')
    parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
    parser.add_argument('-l', '--loglevel', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    
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
    log_filename = f"log/apoiase_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    if not os.path.exists("raw"):
        os.makedirs("raw")

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    collect_apoiase(args.verbose)
