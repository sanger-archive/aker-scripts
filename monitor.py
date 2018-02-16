#!/usr/bin/env python3

"""A script to monitor all Aker services across each environment. Each service
is re-checked every ten minutes"""

import os
import http.client
import ssl
import threading
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

load_balancers = {"WIP": "dev.psd.sanger.ac.uk:9200",
                "UAT": "dev.psd.sanger.ac.uk:9100",
                "PROD": "lb-akerprod-01.internal.sanger.ac.uk:9000"}
paths = ["/dashboard/", "/submission/", "/work-orders/", "/set-shaper/",
        "/stamps/", "/study/", "/stamps_service/stamps", "/sets_service/sets",
        "/materials_service/", "/auth-service/"]

other_services = { "WIP": {"Billing Mock": ["dev.psd.sanger.ac.uk:3601", "/"],
                    "Fake eHMDMC": ["dev.psd.sanger.ac.uk:3501", "/validate?hmdmc=12_3456"]},
                "UAT": {"Billing Mock": ["dev.psd.sanger.ac.uk:3801", "/"],
                    "Fake eHMDMC": ["dev.psd.sanger.ac.uk:3701", "/validate?hmdmc=12_3456"]},
                "PROD": {"Billing Mock": ["lb-akerprod-01.internal.sanger.ac.uk:3601", "/"],
                    "Fake eHMDMC": ["lb-akerprod-01.internal.sanger.ac.uk:3501", "/validate?hmdmc=12_3456"]}}

def check_url(lb, path):
    try:
        conn = http.client.HTTPSConnection(lb, context=ssl._create_unverified_context())
        conn.request("GET", path)
        return conn.getresponse().status
    except Exception as ex:
        return "Exception: " + str(ex)

def print_status(service, status):
    if status in [200, 301, 302, 304]:
        print(Fore.GREEN + service + " is probably up")
    else:
        print(Fore.RED + service + " is down with: " + str(status))

def main():
    os.system('clear')
    threading.Timer(600.0, main).start()
    print(datetime.now())
    for lb in load_balancers:
        print ("** " + lb + " **")
        for path in paths:
            status = check_url(load_balancers[lb], path)
            print_status(path, status)
        for service in other_services[lb]:
            url = other_services[lb][service][0]
            path = other_services[lb][service][1]
            status = check_url(url, path)
            print_status(service, status)
        print("")

if __name__=='__main__':
    main()
