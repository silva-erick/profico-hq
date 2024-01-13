import requests
import logging
import http.client
import re
from datetime import datetime
import json
import os

import argparse

import apoio

BATCH_SIZE = 9
URL_FINISHED_PROJECTS   = "https://api.catarse.me/finished_projects"
URL_CATEGORIES          = "https://api.catarse.me/categories"
URL_CITIES              = "https://api.catarse.me/cities"
URL_REWARD_DETAILS      = "https://api.catarse.me/reward_details"
URL_PROJECT_DETAILS     = "https://api.catarse.me/project_details"
URL_USER_DETAILS        = "https://api.catarse.me/user_details"

class BaseCatarseCollectionApi:
    batch_size = 9
    def __init__(self):
        self.batch_size = self._get_batch_size()

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
            logging.debug(f"Items will be fetched in batches of {batch_size}")
            while True:
            # success = True
            # for _ in range(1):
                if verbose:
                    print(":", end='', flush=True)

                p1 = datetime.now()
                headers["Range"] = f"{offset}-{offset+batch_size-1}"
                req = requests.Request("GET", url, headers=headers, params=params)
                prepped = session.prepare_request(req)
                prepped.headers[":Authority"] = "api.catarse.me"
                prepped.headers[":Method"] = "GET"
                prepped.headers[":Scheme"] = "https"
                prepped.headers[":Path"] = self._get_header_path()

                num_of_calls = num_of_calls + 1
                response = session.send(prepped, timeout=90)
                p2 = datetime.now()
                delta = p2-p1
                if delta.microseconds > longest_call:
                    longest_call = delta.seconds * 1000000 + delta.microseconds

                total_time = total_time + delta.microseconds

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
                    if verbose:
                        print("")
                        print(f"Request error: {response.status_code} - {response.text}")
                    break

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            if verbose:
                print("")
                print(f"Request exception: {e}")

        avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class CatarseCategories(BaseCatarseCollectionApi):
    def __init__(self):
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
    def __init__(self):
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
    def __init__(self):
        self._url = ''

    def _get_url(self):
        return URL_FINISHED_PROJECTS
    
    def _get_params(self):
        params = {
            "order": "state_order.asc,state.desc,pledged.desc",
            #"mode": "not.eq.sub",
            "category_id": "eq.7",
        }
        return params
    
    def _get_batch_size(self):
        return 99
    
    def _get_header_path(self):
        #return '/finished?state_order.asc%2Cstate.desc%2Cpledged.desc&mode=not.eq.sub&category_id=eq.7'
        return '/finished?state_order.asc%2Cstate.desc%2Cpledged.desc&category_id=eq.7'
    
    def execute(self, verbose=False, log_level=logging.WARNING):
        res = super().execute(verbose, log_level)
        if not res.sucesso:
            print("?", end='')
        else:
            project_details_api = CatarseProjectDetails()
            reward_details_api = CatarseRewardDetails()
            user_details_api = CatarseUserDetails()

            users_details = {}

            for fin in res.resultado:
                project_success = True

                project_id = fin['project_id']
                project = {}

                if not os.path.exists(f"../../dados/brutos/catarse/campanhas/{project_id}.json"):
                    pdr = project_details_api.execute(f"eq.{project_id}", verbose, log_level)
                    if not pdr.sucesso:
                        print("?", end='')
                        project_success = False
                        logging.error(f"project_id: {project_id} - error on project details")
                    else:
                        #print("#", end='')
                        for pr in pdr.resultado:
                            project['detail'] = pr
                            user_id = pr['user_id']
                            if user_id in users_details:
                                #print('#', end='')
                                project['user'] = users_details[user_id]
                            else:
                                udr = user_details_api.execute(f"eq.{user_id}")
                                if not udr.sucesso:
                                    print("?", end='')
                                    project_success = False
                                    logging.error(f"project_id: {project_id} - error on user details")
                                else:
                                    #print('#', end='')
                                    for usr in udr.resultado:
                                        users_details[user_id] = usr
                                        project['user'] = usr
                                        break
                            break


                    rdr = reward_details_api.execute(f"eq.{project_id}", verbose, log_level)
                    if not rdr.sucesso:
                        print("?", end='')
                        project_success = False
                        logging.error(f"project_id: {project_id} - error on reward details")
                    else:
                        project['rewards'] = rdr.resultado
                        #print('#', end='')

                    if project_success:
                        data_file = f"../../dados/brutos/catarse/campanhas/{project_id}.json"
                        # Using a JSON string
                        with open(data_file, 'w') as json_file:
                            json.dump(project, json_file)


        return res


class BaseCatarseUniqueApi:
    _param = {}
    def __init__(self):
        self._param = {}

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
    
    def _execute(self, key, value, verbose = False, log_level = logging.WARNING):
        # allow headers starting with :
        http.client._is_legal_header_name = re.compile(rb'[^\s][^:\r\n]*').fullmatch

        self._add_param(key, value)

        # if verbose:
        #     http.client.HTTPConnection.debuglevel = 1

        # allows logging
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(log_level)
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
            if verbose:
                print(".", end='', flush=True)

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
                if verbose:
                    print("")
                    print(f"Request error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            result.add_request_error(-1, e)
            if verbose:
                print("")
                print(f"Request exception: {e}")
            return result

        avg_call = total_time / num_of_calls

        result.add_summary(success, all_items, len(all_items), total_time, avg_call, longest_call)

        return result

class CatarseProjectDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_PROJECT_DETAILS
    
    def _get_baseurl(self):
        return '/project_details'

    def execute(self, project_id, verbose = False, log_level = logging.WARNING):
        return self._execute('project_id', project_id, verbose, log_level)
    

class CatarseRewardDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_REWARD_DETAILS
    
    def _get_baseurl(self):
        return '/reward_details'
    
    def execute(self, project_id, verbose = False, log_level = logging.WARNING):
        return self._execute('project_id', project_id, verbose, log_level)
    

class CatarseUserDetails(BaseCatarseUniqueApi):
    def _get_url(self):
        return URL_USER_DETAILS
        
    def _get_baseurl(self):
        return '/user_details'

    def execute(self, user_id, verbose = False, log_level = logging.WARNING):
        return self._execute('id', user_id, verbose, log_level)
    

def collect_catarse(verbose):
    if not os.path.exists("../../dados/brutos/catarse"):
        os.makedirs("../../dados/brutos/catarse")
    if not os.path.exists("../../dados/brutos/catarse/campanhas"):
        os.makedirs("../../dados/brutos/catarse/campanhas")

    apiset = {}
    apiset['finished'] = CatarseFinishedProjects()

    for k, api in apiset.items():
        logging.debug(f"Preparing to access catarse.me: {k}")
        if verbose:
            print(f"{k}: ", end='')
        res = api.execute(verbose, log_level)
        logging.info(f"Data fetched")

        if verbose:
            print("")
            print("summary:")
            print(f"\tsuccess: {res.sucesso}")
            print(f"\titems: {res.itens}")
            print(f"\ttotal time: {res.tempo_total}us")
            print(f"\taverage call: {res.tempo_medio}us")
            print(f"\tlongest_call: {res.chamada_mais_longa}")

            data_file = f"../../dados/brutos/catarse/{k}.json"
            with open(data_file, 'w') as json_file:
                json.dump(res.resultado, json_file)

    api_categories = CatarseCategories()
    res = api_categories.execute()
    categories_file = f"../../dados/brutos/catarse/categories.json"
    with open(categories_file, 'w') as json_file:
        json.dump(res.resultado, json_file)

    api_cities = CatarseCities()
    res = api_cities.execute()
    cities_file = f"../../dados/brutos/catarse/cities.json"
    with open(cities_file, 'w') as json_file:
        json.dump(res.resultado, json_file)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog = "raspar_catarse.py",
        description='Obtém dados de campanhas de financiamento coletivo de quadrinhos dos sites monitorados')
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
    log_filename = f"log/catarse_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

    if not os.path.exists("raw"):
        os.makedirs("raw")

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        filename=log_filename,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)

    collect_catarse(args.verbose)
