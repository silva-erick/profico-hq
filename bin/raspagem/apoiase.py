import asyncio

import requests
import logging
import http.client
import re
from datetime import datetime
import json
import os

import argparse

import logs
import raspagem.apoio as apoio

BATCH_SIZE = 5

URL_QUADRINHOS = "https://apoia.se/explore/Quadrinhos"
URL_PROJECTS = "https://0hnipmgv3i.execute-api.us-east-1.amazonaws.com/prod/search"

class BaseApoiaseCollectionApi:
    """
    classe básica para chamada de API em apoia.se
    """
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
    
    def execute(self, threads, clear_cache):
        # allow headers starting with :
        http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch

        # allows logging
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logs.current_log_level)
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

                    threads.append(asyncio.create_task(apoiase_slug(batch_campaigns, cache_slug, clear_cache)))

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
                    logs.verbose_error(f"Request error: {response.status_code} - {response.text}")
                    break

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            logs.verbose_error(f"Request exception: {e}", e)

        if num_of_calls == 0:
            avg_call = 0
        else:
            avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class ApoiaseProjects(BaseApoiaseCollectionApi):
    """
    classe que implementa BaseApoiaseCollectionApi para obter dados das campanhas em apoia.se
    """
    def __init__(self):
        self._url = ''

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
    
    def execute(self, threads, clear_cache):
        res = super().execute(threads, clear_cache)

        return res

async def apoiase_slug(batch_campaigns, cache_slug, clear_cache):
    """
    percorrer um lote de campanhas em busca dos dados detalhados de cada uma
    """
    for camp in batch_campaigns:

        obter = clear_cache or not os.path.exists(f"../dados/brutos/apoiase/campanhas/{camp['_id']}.json")
        if not obter:
            continue

        slug = camp['slug']
        if slug in cache_slug:
            camp['complemento'] = cache_slug[slug]
        else:
            response2 = requests.get(url=f'https://apoia.se/api/v1/users/{slug}')
            cache_slug[slug] = json.loads(response2.text)
            camp['complemento'] = cache_slug[slug]

        if os.path.exists(f"../dados/brutos/apoiase/campanhas/{camp['_id']}.json"):
            os.remove(f"../dados/brutos/apoiase/campanhas/{camp['_id']}.json")
        data_file = f"../dados/brutos/apoiase/campanhas/{camp['_id']}.json"
        with open(data_file, 'w') as json_file:
            json.dump(camp, json_file)
    return False

async def raspar_apoiase(args):
    """
    coordenar raspagem de apoia.se
    """
    if not os.path.exists("../dados/brutos/apoiase"):
        os.makedirs("../dados/brutos/apoiase")
    if not os.path.exists("../dados/brutos/apoiase/campanhas"):
        os.makedirs("../dados/brutos/apoiase/campanhas")

    api_projetos = ApoiaseProjects()

    logging.debug(f"Preparing to access apoiase.me")
    threads = list()
    res = api_projetos.execute(threads, args.clear_cache)
    
    logging.info(f"\nData fetched")
