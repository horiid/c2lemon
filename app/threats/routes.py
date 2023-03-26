from pprint import pprint
from app.threats import blueprint
from flask import redirect, url_for, render_template, current_app
from app.threats.util import *

# access to /threats/ are redirected to /threats/idlist 
@blueprint.route('/')
def route_default():
    return redirect(url_for('threats_blueprint.id_list'))

# list up threat IDs
@blueprint.route('/idlist', methods=['GET'])
def id_list():
    # validate the config file
    is_valid=validate_dataset_path()
    if is_valid is not True:
        return redirect(url_for('base_blueprint.config'))
    
    # read filenames in the dataset folder
    id_list=list_ids(current_app.config['dataset_path'] + "\\ISL01")
    return render_template('idlist.html', id_list=id_list)

# shows monitored year & month of the selected threat ID
@blueprint.route('/<string:threat_id>', methods=['GET'])
def threats(threat_id):
    year_path = current_app.config['dataset_path'] + "\\ISL01\\" + threat_id
    if not os.path.isdir(year_path):
        return render_template("404.html"), 404
    
    year_months = {year: os.listdir(year_path+'/'+year) for year in os.listdir(year_path)}
    # return render_template_string('<p>' + str(year_months) + '<p>')
    return render_template('year_months.html', year_months=year_months, threat_id=threat_id)

# visualization page
@blueprint.route('/<string:threat_id>/<string:year>/<string:month>', methods=['GET'])
def visualize(threat_id, year, month):
    # get all files from each monitor_location
    # data_paths = {"folder path": "monitor location"}
    path_loc = dict()
    root = current_app.config['dataset_path']
    for path in os.listdir(root):
        # path = *-c2monitor
        # identify the folders where the monitor data is stored
        if os.path.isdir(root + "/" + path):
            for tid in os.listdir(root + "/" + path):
                path_to_files = root + "/" + path + "/" +threat_id + "/" + year + "/" + month
                if os.path.exists(path_to_files): path_loc[path_to_files] = path
            print(path_to_files)

    # file IO threading
    future_list = dict()
    with ThreadPoolExecutor() as executor:
        for path, loc in path_loc.items():
            for file in os.listdir(path):
                zip_input_ping_http = executor.submit(extract_values, path + "/" + file)
                future_list[zip_input_ping_http] = loc
    hosts = dict()
    for future, loc in future_list.items():
        # input: ip addr, domain, url
        if future.result() is None: continue
        input = future.result()['input'].replace('http://', '')
        # if hosts[input] is not created hosts[input][loc] is not created too
        if not input in hosts:
            hosts[input] = dict()
            hosts[input][loc] = list()
            hosts[input][loc].append({"observed-time": future.result()['observed-time'], "ping-ext": future.result()['ping-ext'], "http-response-ext": future.result()['http-response-ext']})
        # hosts[input] is created but loc is a new location
        elif loc not in hosts[input]:
            hosts[input][loc] = list()
            hosts[input][loc].append({"observed-time": future.result()['observed-time'], "ping-ext": future.result()['ping-ext'], "http-response-ext": future.result()['http-response-ext']})
        # hosts[input] is created and loc already exists
        else: hosts[input][loc].append({"observed-time": future.result()['observed-time'], "ping-ext": future.result()['ping-ext'], "http-response-ext": future.result()['http-response-ext']})

    monitor_info={"threat_id": threat_id, "year": year, "month": month}
    with open("dump.txt", "w") as f: json.dump(hosts, f, indent=4)
    return render_template('detail.html', inputs=list(hosts.keys()), hosts=json.dumps(hosts), monitor_info=monitor_info)

@blueprint.route('/<string:threat_id>/summary', methods=['GET'])
def threat_summary(threat_id):
    # load file(s) from the path
    path_loc = dict()
    root = current_app.config['dataset_path']
    heatmap_datapath = current_app.config['heatmap_datapath']
    for path in os.listdir(root):
        # path = *-c2monitor
        # identify the folders where the monitor data is stored
        if "c2monitor" in path:
            for location in os.listdir(root + "/" + path):
                print(root + "/" + path + "/" + location + "/" +threat_id)
                path_to_files = root + "/" + path + "/" + location + "/" +threat_id
    with open(heatmap_datapath + "/" + threat_id + ".json", 'r') as f:
        data = json.load(f)
    return render_template('summary.html', data=data)
@blueprint.route('/statistics', methods=['GET'])
def statistics():
    return render_template('statistics.html')


threat_summary_prototype='''
def threat_summary(threat_id):
    # load file(s) from the path
    path=os.listdir(current_app.config['dataset_path']+'/*'+threat_id+'*')
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
'''