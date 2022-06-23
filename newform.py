import argparse, os, json, pprint, re, uuid, concurrent.futures, random
from http.client import responses

parser = argparse.ArgumentParser()
parser.add_argument('dirpath')
parser.add_argument('newformat')
args = parser.parse_args()


def get_path(path: str,
             threat_id: str,
             observe_time: str,
             filename: str,
             create_path: bool = False):
    '''Get a path for storing monitoring results

    Get a path accordingly, referencing observation time and threat ID.
    The directory for storing logs looks like this:
    root/
      ├ THREAT_1/
      |     └2021
      |        ├01
      |        | └2021-01-31T12:00:00.json
      |        | └2021-01-31T16:00:00.json
      |        | └2021-01-31T20:00:00.json
      |        | └...
      |        └02
      |         └...
      ├ THREAT_2/
      |     ├2020
      |     └2021
      ...

    Args:
        root (str): Root of the directory to store logs.
        observe_time (str): observation time in format: "%Y-%m-%dT%H:%M:%S".
        threat_id (str): ID assigned at the CSV file.
    
    Returns:

    '''
    # if directory does not exist, create
    observe_time_parsed = observe_time.split('-')
    try:
        year = observe_time_parsed[0]
        month = observe_time_parsed[1]
    except IndexError:
        print(
            "observe_time format seems broken. It must be separated with -(hyphens)."
        )
        return None
    path_list = [path, threat_id, year, month]
    abs_path = os.path.abspath("/".join(path_list))

    if not (os.path.isdir(abs_path)) and create_path:
        os.makedirs(abs_path)
        print("created the path:", abs_path)
    path_list.append(filename)
    return_val = os.path.join(abs_path, filename.replace(':', '_'))
    if os.path.exists(return_val):
        val = int(return_val[-7:-5])
        val += 1
        print(val)
        return_val = return_val[:-7] + "{0}".format(str(val).zfill(2)) + "_" + str(random.randint(0,1000000000)) +".json"
        
    return return_val


files = os.listdir(args.dirpath)
files = [f for f in files if os.path.isfile(os.path.join(args.dirpath, f))]
empty = dict()
with open('schema/empty.json') as f:
    empty = json.load(f)

for file in files:
    path = args.dirpath + "/" + file
    date = re.sub("port[0-9]*.json", "", file.replace('_', ":"))[:-5]
    with open(path, 'r') as f:
        jsoned = json.load(f)
        threat_ids = jsoned.keys()
        for threat_id in threat_ids:
            count = 0
            for monitor in jsoned[threat_id]:
                if count == 0 or count == 1:
                    #print(monitor)
                    print(type(monitor))
                    count+=1
                ipv4 = []
                ipv4.append(monitor["host"])

                domain = []
                domain.append(monitor["uri"].split("/")[0])

                uri = monitor["uri"]
                s_code = int(monitor["http_statuscode"]) \
                    if monitor["http_statuscode"] != "Connection Refused" else 0
                input = uri if uri != "" else ipv4[0]
                phrase = responses[int(s_code)] if s_code != 0 else ""
                ping = monitor["ping"]
                with open('schema/empty.json') as f:
                    cti = json.load(f)
                cti["x-ict-isac.jp"]["id"] = str(uuid.uuid4())
                cti["x-ict-isac.jp"]["monitoring"]["observe-time"] = date
                cti["x-ict-isac.jp"]["monitoring"]["input"] = input
                cti["x-ict-isac.jp"]["monitoring"]["http-response-ext"][
                    "status_code"] = s_code
                cti["x-ict-isac.jp"]["monitoring"]["http-response-ext"][
                    "reason_phrase"] = phrase
                cti["x-ict-isac.jp"]["monitoring"]["ipv4-addr"] = ipv4
                cti["x-ict-isac.jp"]["monitoring"]["ping-ext"]["loss"] = "0%" if  monitor['ping'] == 0 else "100%"
                path_to_storage = get_path(path=args.newformat,
                                            threat_id=threat_id,
                                            observe_time=date,
                                            filename=file,
                                            create_path=True)
                print(path_to_storage)
                with open(path_to_storage, "w", encoding='utf-8') as f:
                    json.dump(cti, f, indent=4)
                    