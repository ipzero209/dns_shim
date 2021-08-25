#!/usr/bin/python3



import os
import time
import queue
import socket
import threading
from dnslib import *
import dns.resolver


def dnsListener(ip, port):
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to port
    server_address = (ip, port)
    sock.bind(server_address)

    # Start listening/processing
    while True:
        data, address = sock.recvfrom(4096)
        if data:
            q_tuple = (data, address)
            # out_queue.put(q_tuple)
            return q_tuple





def decodeRequest(q_tuple):
    while True:

        req_data = q_tuple[0].strip()
        req_data = DNSRecord.parse(req_data)
        req_dict = {'addr' : q_tuple[1],
                    'req' : req_data}
        return req_dict





#TODO: Lookup against DNS Security and respnse/sinkhole logic




def buildResponse(req_dict):
    while True:
        req_data = req_dict['req']
        domain = ""
        for item in req_data.questions[0].qname.label:
            domain += (item.decode('utf-8') + ".")
        answer = ""
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
        req_data.add_answer(RR(domain, ttl=60, rdata=A(ip)))


        resp = req_data.pack()
        out = {'resp' : resp, 'addr': req_dict['addr']}
        return out


def dnsSender(ip, port, output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (ip, port)
    sock.bind(server_address)

    sock.sendto(output['resp'], output['addr'])
    return


def main():
    # req_queue = queue.Queue()
    # decoded_queue = queue.Queue()
    # xmit_queue = queue.Queue()
    #
    #
    # threads = []
    # threads.append(threading.Thread(target=dnsListener, args=('192.168.140.51', 1053, xmit_queue, req_queue)))
    # threads.append(threading.Thread(target=decodeRequest, args=(req_queue, decoded_queue)))
    # threads.append(threading.Thread(target=buildResponse, args=(decoded_queue, xmit_queue)))
    #
    # for thread in threads:
    #     thread.start()

    server = "192.168.140.51"
    port = 1053

    while True:
        req = dnsListener(server, port)
        decoded_req = decodeRequest(req)
        output = buildResponse(decoded_req)
        dnsSender(server, port, output)


    # while True:







if __name__ == "__main__":
    main()



