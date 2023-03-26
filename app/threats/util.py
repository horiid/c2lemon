import os, json, hashlib, re
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def validate_dataset_path():
    # file does not exist
    if not os.path.isfile('./dataset_conf.json'):
        print("The path is not found")
        return False
    
    # validate key and value in the file
    config=open(os.path.abspath('./dataset_conf.json'), 'r')
    config=json.load(config)
    if 'dataset_path' in config:
        return True
    else:
        return False

def validate_host(addr, uri, hostlist):
    arg = addr + uri
    hashed_host = hashlib.md5(arg)
    if not hashed_host in hostlist:
        hostlist.append(hashed_host)

def get_threat_info(path):
    id_list=[]
    last_updates=[]
    files=os.listdir(path)
    # extract a threat id and last updated date from file
    for filename in files:
        id_=re.sub('.json', '', filename)
        id_=os.path.split(id_)[1]
        id_list.append(id_)
        with open(filename, 'r') as readf:
            jsonf=json.load(readf)
            last_updates.append(jsonf["data"][-1][0])
    return zip(id_list, last_updates)

def list_ids(path):
    dirs = os.listdir(path)
    if os.name == 'nt':
        id_list = [id_.rsplit('\\', 1)[-1] for id_ in dirs]
    else:
        id_list = [id_.rsplit('/', 1)[-1] for id_ in dirs] 
    return id_list

def extract_values(filename):
    input = ""
    ping = dict()
    http = dict()
    with open(filename) as f:
        jsoned = json.load(f)
        if 'x-ict-isac.jp' in jsoned:
            monitoring = jsoned['x-ict-isac.jp']['monitoring']
        elif 'monitoring' in jsoned:
            monitoring = jsoned['monitoring']
        else: return None
        input = monitoring['input']
        if 'observe-time' in monitoring: observed_time = monitoring['observe-time']
        elif 'monitored_date' in jsoned: observed_time = jsoned['monitored_date']

        if 'ping-ext'in monitoring: ping = monitoring['ping-ext']
        elif 'ping_ext'in monitoring: ping = monitoring['ping_ext']
        
        if 'http-response-ext' in monitoring: http = monitoring['http-response-ext']
        elif 'http_response_ext' in monitoring: http = monitoring['http_response_ext']
    return {"input": input, "observed-time": observed_time, "ping-ext": ping, "http-response-ext": http}

# Use this to get full paths returned from os.listdir()
def resolve_to_full_path(dirpath, filenames: list):
    for filename in filenames:
        yield os.path.abspath(os.path.join(dirpath, filename))
