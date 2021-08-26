#!/usr/bin/python3



import os
import time
import queue
import socket
import threading
import cloudcheck
from dnslib import *
import dns.resolver





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
        print(request)

        # Extract requested domain as str
        domain = ""
        for item in request.questions[0].qname.label:
            domain += (item.decode('utf-8') + ".")

        # Check DNS Security Service for action (may not need rstrip for actual service)
        action = cloudcheck.checkRequest(domain.rstrip('.'))

        # Set response IP according to response from checkRequest()
        if action == "sinkhole":
            ip = "127.0.0.1"
        elif action == "resolve":
            try:
                answer = dns.resolver.resolve(domain, 'A')
            except dns.resolver.NoAnswer:
                ip = "255.255.255.255"
            except dnslib.buffer.BufferError:
                ip = "255.255.255.255"
            except dnslib.dns.DNSError:
                ip = "255.255.255.255"
            except:
                ip = "1.1.1.1"
            if answer != "":
                for rr in answer:
                    print('======================')
                    print(rr)
                    print('======================')
                    ip = rr.address
        else:
            ip = "1.1.1.1"

        # Add answer to request and pack for transmission
        request.add_answer(RR(domain, ttl=60, rdata=A(ip)))
        response = request.pack()

        # Send response
        sock.sendto(response, address)




if __name__ == "__main__":
    main()



