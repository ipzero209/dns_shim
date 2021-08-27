#!/usr/bin/python3



import time
import socket
import cloudcheck
from dnslib import *
import externalcheck


"""
file locations
/tmp
names

$sinkholefile="/tmp/sinkhole.txt";
$categoryfile="/tmp/categories.txt";
$customdomains="/tmp/custdomain.txt";



"""

def loadSettings():

    domains = set()
    sinkhole_ip = ""
    categories = set()

    try:
        domain_file = open('/tmp/customdomains.txt')
        for line in domain_file:
            domains.add(line.strip())
        domain_file.close()
    except:
        return None

    try:
        sinkhole_file = open('/tmp/sinkhole.txt')
        sinkhole_ip = sinkhole_file.readline().strip()
        sinkhole_file.close()
    except:
        return None

    try:
        category_file = open('/tmp/categories.txt')
        for line in category_file:
            categories.add(line.strip())
        category_file.close()
    except:
        return None

    settings_dict = {'domains' : domains,
                     'sinkhole' : sinkhole_ip,
                     'categories'  categories}
    return settings_dict









def main():

    #Define IP and port - Will need to read IP from environment
    server = "192.168.140.51"
    port = 1053

    # Import settings

    settings = loadSettings()

    while settings == None:
        settings = loadSettings()
        time.sleep(5)

    # Start resolver loop
    while True:

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to port
        server_address = (server, port)
        sock.bind(server_address)

        # Start listening/processing

        data, address = sock.recvfrom(4096)
        print("==========================")
        print(address)
        print("==========================")

        # Parse request - only handling A records at this time
        request = DNSRecord.parse(data)


        # Extract requested domain as str
        domain = str(request.get_q().qname)


        # Check DNS Security Service for action (may not need rstrip for actual service)
        results = cloudcheck.checkRequest(domain.rstrip('.'))

        action = ""
        for result in results:
                if result in settings['domains']:
                    action = "sinkhole"
                elif result in settings['categories']:
                    action = "sinkhole"
                else:
                    action = "resolve"

        # Set response IP according to response from checkRequest()
        if action == "sinkhole":
            ip = settings['sinkhole']
        elif action == "resolve":
            ip = externalcheck.externalResolver(domain)
        else:
            ip = "timeout"

        if ip == "timeout":
            pass
        else:
            # Add answer to request and pack for transmission
            request.add_answer(RR(domain, ttl=60, rdata=A(ip)))

            response = request.pack()

            # Send response
            sock.sendto(response, address)
        # Reload settings
        settings = loadSettings()




if __name__ == "__main__":
    main()



