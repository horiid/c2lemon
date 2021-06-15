from app.threats import blueprint
from flask import redirect, url_for, render_template, render_template_string
import os, json, glob, re, collections, hashlib

# /threats redirects to root directory(/).
@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.id_list'))

@blueprint.route('/<string:threat_id>', methods=['GET'])
def threats(threat_id):
    return redirect(url_for('threats_blueprint.threat_summary', threat_id=threat_id))

@blueprint.route('/<string:threat_id>/summary', methods=['GET'])
def threat_summary(threat_id):
    # validate the config file
    is_valid=validate_dataset_path()
    if is_valid is not True:
        return redirect(url_for('base_blueprint.config'))
    
    # load file(s) from the path
    path=open(os.path.abspath('./config.json'), 'r')
    path=json.load(path)['dataset_path']
    path=glob.glob(path+'/*'+threat_id+'*')
    threat_file=open(path[0], 'r')
    threat_file=json.load(threat_file)
    
    # dataset to parse on html
    anonymized_hosts = list()
    pings   = list()
    s_codes = list()
    ports   = list()
    exedates= list()
    port80  = list()
    port443 = list()

    number_of_servers = 0
    active_servers = 0
    heatmap_data = dict()
    exedate = re.sub('_.*', '', threat_file['data'][0][0])
    
    for data in threat_file['data']:
        cur_exedate = re.sub('_.*', '', data[0])
        if exedate != cur_exedate:  # initialize counts by executed date
            heatmap_data[exedate] = active_servers / number_of_servers  # rate of activity of c2 servers
            exedate = cur_exedate   # set the latest exedate
            active_servers = 0
            number_of_servers = 0
        
        if data[1] == "80":
            port80.append(exedate)
        elif data[1] == "443":
            port443.append(exedate)
        
        string_anonymize = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        anony_idx = 0
        for c2server in data[2]:
            number_of_servers += 1
            anonymized_hosts.append("HOST " + string_anonymize[anony_idx])
            anony_idx += 1
            pings.append(c2server['ping'])
            s_codes.append(c2server['http_statuscode'])
            exedates.append(data[0])
            ports.append(data[1])
            # check if server is active
            if c2server['ping'] == 0 and c2server['http_statuscode'] != "Connection Refused":
                active_servers += 1
    print(heatmap_data)
    return render_template("summary.html",
    zipped_data=zip(anonymized_hosts, pings, s_codes, ports, exedates),
    threat_id=threat_id,
    s_codes=json.dumps(s_codes),
    heatmap_data=json.dumps(heatmap_data))

@blueprint.route('/idlist', methods=['GET'])
def id_list():
    # validate the config file
    is_valid=validate_dataset_path()
    if is_valid is not True:
        return redirect(url_for('base_blueprint.config'))
    
    # read filenames in the dataset folder
    path=open('./config.json', 'r')
    path=json.load(path)
    path=path['dataset_path']
    threat_info=get_threat_info(path)
    return render_template('idlist.html', threat_info=threat_info)

@blueprint.route('/statistics', methods=['GET'])
def statistics():
    return render_template('statistics.html')

def validate_dataset_path():
    # file does not exist
    if not os.path.isfile('./config.json'):
        print("The path is not found")
        return False
    
    # validate key and value in the file
    config=open(os.path.abspath('./config.json'), 'r')
    config=json.load(config)
    if 'dataset_path' in config:
        return True
    else:
        return False

def get_threat_info(path):
    id_list=[]
    last_updates=[]
    files=glob.glob(path+"/*")
    # extract a threat id and last updated date from file
    for filename in files:
        id_=re.sub('.json', '', filename)
        id_=os.path.split(id_)[1]
        id_list.append(id_)
        with open(filename, 'r') as readf:
            jsonf=json.load(readf)
            last_updates.append(jsonf["data"][-1][0])
    return zip(id_list, last_updates)

def validate_host(addr, uri, hostlist):
    arg = addr + uri
    hashed_host = hashlib.md5(arg)
    if not hashed_host in hostlist:
        hostlist.append(hashed_host)