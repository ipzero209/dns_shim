#!/usr/bin/python3




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



def main():

    #Define IP and port - Will need to read IP from environment
    server = "192.168.140.51"
    port = 1053

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
        action = cloudcheck.checkRequest(domain.rstrip('.'))

        # Set response IP according to response from checkRequest()
        if action == "sinkhole":
            ip = "127.0.0.1"
        elif action == "resolve":
            ip = externalcheck.externalResolver(domain)
        else:
            ip = "1.1.1.1"

        if ip == "timeout":
            pass
        else:
            # Add answer to request and pack for transmission
            request.add_answer(RR(domain, ttl=60, rdata=A(ip)))
            response = request.pack()

            # Send response
            sock.sendto(response, address)




if __name__ == "__main__":
    main()



