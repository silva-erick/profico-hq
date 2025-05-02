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

BATCH_SIZE = 9
URL_FINISHED_PROJECTS   = "https://api.catarse.me/finished_projects"
URL_CATEGORIES          = "https://api.catarse.me/categories"
URL_CITIES              = "https://api.catarse.me/cities"
URL_REWARD_DETAILS      = "https://api.catarse.me/reward_details"
URL_PROJECT_DETAILS     = "https://api.catarse.me/project_details"
URL_USER_DETAILS        = "https://api.catarse.me/user_details"

class BaseCatarseCollectionApi:
    batch_size = 9
    def __init__(self, args):
        self.batch_size = self._get_batch_size()
        self._args = args

    def _get_headers(self):
        headers = {
            "Accept":"application/json, text/*",
            "Accept-Encoding":"identity",
            "Accept-Language":"en-US,en;q=0.9,pt;q=0.8",
            "Origin":"https://www.catarse.me",
            "Prefer":"count=exact",
            "Range": "0-8",  # Define o intervalo de 9 itens
            "Range-Unit":"items",
            "Referer":"https://www.catarse.me/",
            "Sec-Ch-Ua":"\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Windows\"",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
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
    
    def execute(self):
        # allow headers starting with :
        http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch

        # allows logging
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logs.current_log_level)
        requests_log.propagate = True

        batch_size = self._get_batch_size()
        headers = self._get_headers()
        params = self._get_params()
        url = self._get_url()

        all_items = []
        offset = 0

        session = requests.Session()
        total_time = 0
        num_of_calls = 0
        longest_call = 0
        success = False

        result = apoio.ResultadoApi(False)

        try:
            logs.verbose(self._args, f"Ítens serão obtidos em lotes de {batch_size}")
            while True:

                p1 = datetime.now()
                headers["Range"] = f"{offset}-{offset+batch_size-1}"
                req = requests.Request("GET", url, headers=headers, params=params)
                prepped = session.prepare_request(req)
                prepped.headers[":Authority"] = "api.catarse.me"
                prepped.headers[":Method"] = "GET"
                prepped.headers[":Scheme"] = "https"
                prepped.headers[":Path"] = self._get_header_path()

                num_of_calls = num_of_calls + 1
                logs.verbose(self._args, f"{type(self)}: chamada {num_of_calls}")
                response = session.send(prepped, timeout=90)
                p2 = datetime.now()
                delta = p2-p1
                if delta.microseconds > longest_call:
                    longest_call = delta.seconds * 1000000 + delta.microseconds

                total_time = total_time + delta.microseconds

                logs.verbose(self._args, f"{type(self)}: chamada {num_of_calls} - status: {response.status_code}")

                # success or partial code
                if response.status_code == 200 or response.status_code == 206:
                    batch_campaigns = response.json()
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

        avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class CatarseCategories(BaseCatarseCollectionApi):
    def __init__(self, args):
        super().__init__(args)
        self._url = ''

    def _get_url(self):
        return URL_CATEGORIES
    
    def _get_params(self):
        params = {
            "order": "name.asc"
        }
        return params
    
    def _get_batch_size(self):
        return 99
    
    def _get_header_path(self):
        return '/categories?order=name.asc'

class CatarseCities(BaseCatarseCollectionApi):
    def __init__(self, args):
        super().__init__(args)
        self._url = ''

    def _get_url(self):
        return URL_CITIES
    
    def _get_params(self):
        params = {
            "order": "name.asc"
        }
        return params
    
    def _get_batch_size(self):
        return 99
    
    def _get_header_path(self):
        return '/cities?order=name.asc'

class CatarseFinishedProjects(BaseCatarseCollectionApi):
    def __init__(self, args):
        super().__init__(args)
        self._url = ''

    def _get_url(self):
        return URL_FINISHED_PROJECTS
    
    def _get_params(self):
        params = {
            "order": "state_order.asc,state.desc,pledged.desc",
            "category_id": "eq.7",
        }
        return params
    
    def _get_batch_size(self):
        return 99
    
    def _get_header_path(self):
        return '/finished?state_order.asc%2Cstate.desc%2Cpledged.desc&category_id=eq.7'
    
    def execute(self, threads, clear_cache):
        res = super().execute()
        if not res.sucesso:
            pass
        else:

            users_details = {}

            num_of_calls = 1
            for fin in res.resultado:
                project_id = fin['project_id']

                logs.verbose(self._args, f"{type(self)}: campanha: {num_of_calls} - {project_id}")
                threads.append(asyncio.create_task(catarse_campanha(self._args, project_id, users_details, clear_cache)))

                num_of_calls = num_of_calls + 1


        return res


class BaseCatarseUniqueApi:
    _param = {}
    def __init__(self, args):
        self._param = {}
        self._args = args

    def _get_headers(self):
        headers = {
            "Accept":"application/json, text/*",
            "Accept-Encoding":"identity",
            "Accept-Language":"en-US,en;q=0.9,pt;q=0.8",
            "Origin":"https://www.catarse.me",
            "Prefer":"count=none",
            "Range": "0-0",
            "Range-Unit":"items",
            "Referer":"https://www.catarse.me/",
            "Sec-Ch-Ua":"\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"\"Windows\"",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        return headers
    
    def _get_baseurl(self):
        return ''
    
    def _add_param(self, key, value):
        self._param[key] = value

    def _get_params(self):
        return self._param
    
    def _get_url(self):
        return ''
    
    def _get_header_path(self):
        full = ''
        for k,v in self._get_params().items():
            if full != '':
                full = full + "&"
            full = f"{k}={v}"
        if full == '':
            return self._get_baseurl()
        
        return f"{self._get_baseurl()}?{full}"
    
    def _execute(self, key, value):
        # allow headers starting with :
        http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch

        self._add_param(key, value)

        # allows logging
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logs.current_log_level)
        requests_log.propagate = True

        headers = self._get_headers()
        params = self._get_params()
        url = self._get_url()

        all_items = []
        offset = 0

        session = requests.Session()
        total_time = 0
        num_of_calls = 0
        longest_call = 0
        success = False

        result = apoio.ResultadoApi(False)

        try:
            p1 = datetime.now()
            req = requests.Request("GET", url, headers=headers, params=params)
            prepped = session.prepare_request(req)
            prepped.headers[":Authority"] = "api.catarse.me"
            prepped.headers[":Method"] = "GET"
            prepped.headers[":Scheme"] = "https"
            prepped.headers[":Path"] = self._get_header_path()

            response = session.send(prepped, timeout=90)
            p2 = datetime.now()
            delta = p2-p1
            if delta.microseconds > longest_call:
                longest_call = delta.seconds * 1000000 + delta.microseconds

            total_time = total_time + delta.microseconds
            num_of_calls = num_of_calls + 1

            if response.status_code == 200 or response.status_code == 206:
                batch_campaigns = response.json()
                all_items.extend(batch_campaigns)
                success = True
            else:
                result.add_request_error(response.status_code, response.text)
                logs.verbose_error(f"Request error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            logs.verbose_error(f"Request exception: {e}", e)
            return result

        avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class CatarseProjectDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_PROJECT_DETAILS
    
    def _get_baseurl(self):
        return '/project_details'

    def execute(self, project_id):
        return self._execute('project_id', project_id)
    

class CatarseRewardDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_REWARD_DETAILS
    
    def _get_baseurl(self):
        return '/reward_details'
    
    def execute(self, project_id):
        return self._execute('project_id', project_id)
    

class CatarseUserDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_USER_DETAILS
        
    def _get_baseurl(self):
        return '/user_details'

    def execute(self, user_id):
        return self._execute('id', user_id)

def catarse_base(args):

    if not os.path.exists("../dados/brutos/catarse"):
        os.makedirs("../dados/brutos/catarse")
    if not os.path.exists("../dados/brutos/catarse/campanhas"):
        os.makedirs("../dados/brutos/catarse/campanhas")

async def catarse_campanha(args, project_id, users_details, clear_cache):
    """
    coordenar chamada de api de detalhes das campanhas em catarse
    """

    project_details_api = CatarseProjectDetails(args)
    reward_details_api = CatarseRewardDetails(args)
    user_details_api = CatarseUserDetails(args)

    project_success = True


    project = {}

    log.verbose(args, f'verificando projeto: {project_id}')
    if clear_cache or not os.path.exists(f"../dados/brutos/catarse/campanhas/{project_id}.json"):
        pdr = project_details_api.execute(f"eq.{project_id}")
        if not pdr.sucesso:
            project_success = False
            logs.verbose_error(f"project_id: {project_id} - error on project details")
        else:
            for pr in pdr.resultado:
                project['detail'] = pr
                user_id = pr['user_id']
                if user_id in users_details:
                    project['user'] = users_details[user_id]
                else:
                    udr = user_details_api.execute(f"eq.{user_id}")
                    if not udr.sucesso:
                        project_success = False
                        logs.verbose_error(f"project_id: {project_id} - error on user details")
                    else:
                        for usr in udr.resultado:
                            users_details[user_id] = usr
                            project['user'] = usr
                            break
                break


        rdr = reward_details_api.execute(f"eq.{project_id}")
        if not rdr.sucesso:
            project_success = False
            logs.verbose_error(f"project_id: {project_id} - error on reward details")
        else:
            project['rewards'] = rdr.resultado

        if project_success:
            data_file = f"../dados/brutos/catarse/campanhas/{project_id}.json"
            # Using a JSON string
            with open(data_file, 'w') as json_file:
                json.dump(project, json_file)
    return

async def raspar_catarse(args):
    """
    coordenar chamada de api de campanhas em catarse
    """

    finished = CatarseFinishedProjects(args)

    logs.verbose(args, f"Preparando para acessar catarse.me")

    threads = list()
    res = finished.execute(threads, args.clear_cache)
    logs.verbose(args, f"\nChamadas executadas")

    data_file = f"../dados/brutos/catarse/finished.json"
    with open(data_file, 'w') as json_file:
        json.dump(res.resultado, json_file)

async def raspar_catarse_categories(args):
    """
    coordenar chamada de api de categorias em catarse
    """

    logs.verbose(args, 'Catarse - Categories')

    api_categories = CatarseCategories(args)
    res = api_categories.execute()
    categories_file = f"../dados/brutos/catarse/categories.json"
    with open(categories_file, 'w') as json_file:
        json.dump(res.resultado, json_file)

    logs.verbose(args, 'Catarse - Categories - Chamadas executadas')


async def raspar_catarse_cities(args):
    """
    coordenar chamada de api de municípios em catarse
    """

    logs.verbose(args, 'Catarse - Cities')

    api_cities = CatarseCities(args)
    res = api_cities.execute()
    cities_file = f"../dados/brutos/catarse/cities.json"
    with open(cities_file, 'w') as json_file:
        json.dump(res.resultado, json_file)

    logs.verbose(args, 'Catarse - Cities - Chamadas executadas')

