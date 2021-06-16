import argparse, datetime, pprint, json, csv, sys
sys.path.append("../")
from json.decoder import JSONDecodeError, JSONDecoder
from monitorutils import CsvParser, monitor
from monitorutils import CsvParseIndex as csvidx
from models.schema import ProcessStat, MonitoringStat, X_ICT_Isac_Cti
from random import randint

def insert_monitor_data(mon: MonitoringStat=None):
    if mon is None:
        mon = MonitoringStat.empty_map()
    
    pass


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Sends ping and http request")
    parser.add_argument('c2list', help="CSV file lists c2 servers")
    parser.add_argument('port', type=int, help="Port Number")
    args = parser.parse_args()

    # get the executed time and set it to the filename
    observe_time = datetime.datetime.now()
    observe_time = observe_time.strftime('%Y-%m-%dT%H:%M:%S')
    print("Observed at:", observe_time, "\n")
    
    # list of threats in csv file
    rows = CsvParser(filename=args.c2list)
    for row in rows.readline():
        # print(row)
        # get data from row for Monitoring class initialization
        input = row[csvidx.HOST].replace('[', '').replace(']', '')
        domain_name = [row[csvidx.DOMAIN].replace('[', '').replace(']', '')]
        ipv4_addr = [row[csvidx.HOST].replace('[', '').replace(']', '')]
        
        # parse row[file type] and if there are multiple files, store data to 'files'
        is_file_single = False
        file_list = row[csvidx.FILE_TYPE].split(',')
        print("file list: {}".format(file_list))
        if len(file_list) == 1: is_file_single = True

        # Get hashes
        hashes = row[csvidx.HASH]
        try:
            json_decoder = JSONDecoder()
            hashes, i= json_decoder.raw_decode(hashes)
        except JSONDecodeError:
            pass # if there's no hashes, pass.
        # src_port is client port number 
        # randomly selected from Dynamic port numbers.
        src_port = randint(49152, 65535)
        dst_port = int(row[csvidx.PORT]) if not row[csvidx.PORT] == '' else 80
        network_traffic = {'src-port': src_port, 'dst-port': dst_port}

        # send ping and http GET method
        ping, mon = monitor(host=input, src_port=src_port, dst_port=dst_port)
        print(ping, mon)

        
        if mon.raw.version == 11:
            http_version = 'http/1.1' 
        elif mon.version == 10:
            http_version = 'http/1.0'
        http_request_ext = {'request-method': 'get', 'request-value': '',
        'request-version': http_version, 'request-header': {
            ""
        }}
        monitor_ = MonitoringStat()
        # Append data to MonitoringStat instance
        monitor_.input = input
        monitor_.domain_name = [row[csvidx.DOMAIN].replace('[', '').replace(']', '')]
        monitor_.ipv4_addr = [row[csvidx.HOST].replace('[', '').replace(']', '')]
        monitor_.observe_time = observe_time
        monitor_.network_traffic = network_traffic
        monitor_.ping_ext = {'lost': ping['loss'], 'ttl': ping['ttl'], 'rtt': ping['rtt']+"ms"}
        # monitor_['file']
        # monitor_['files']
        pprint.pprint(monitor_.monitoring)

if __name__ == '__main__':
    main()
