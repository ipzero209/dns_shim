#!/usr/bin/python3
import binascii
import time
import queue
import socket
import random
import threading
from dnslib import *


def dnsListener(ip, port, in_queue, out_queue):
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to port
    server_address = (ip, port)
    sock.bind(server_address)

    # Start listening/processing
    while True:
        if in_queue.empty():
            data, address = sock.recvfrom(4096)
            if data:
                q_tuple = (data, address)
                out_queue.put(q_tuple)
        else:
            resp = in_queue.get()
            sock.sendto(resp['resp'], resp['addr'])

def decodeRequest(in_queue, out_queue):
    while True:
        req = in_queue.get()
        req_data = req[0].strip()
        req_data = DNSRecord.parse(req_data)
        req_dict = {'addr' : req[1],
                    'req' : req_data}
        out_queue.put(req_dict)
        print(req_dict)




#TODO: Lookup against DNS Security and respnse/sinkhole logic




def buildResponse(in_queue, out_queue):
    while True:
        req = in_queue.get()
        req_data = req['req']
        print(req_data)
        domain = ""
        for item in req_data.questions[0].qname.label:
            domain += (item.decode('utf-8') + ".")
        ip = "1.1.1.1"
        req_data.add_answer(RR(domain, ttl=60, rdata=A(ip)))
        print('======================')
        print('======================')
        resp = req_data.pack()
        out = {'resp' : resp, 'addr': req['addr']}
        out_queue.put(out)



        # out_queue.put(out)


        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # server_address = (ip, random.randint(1025, 65535))
        # sock.bind(server_address)
        # msg = resp.pack()
        # print("============================")
        # print(msg)
        # print("============================")
        # msg = bytes(msg)
        # print("============================")
        # print(msg)
        # print("============================")

        # sock.sendto(msg, req['addr'])



def main():
    req_queue = queue.Queue()
    decoded_queue = queue.Queue()
    xmit_queue = queue.Queue()


    threads = []
    threads.append(threading.Thread(target=dnsListener, args=('192.168.140.51', 1053, xmit_queue, req_queue)))
    threads.append(threading.Thread(target=decodeRequest, args=(req_queue, decoded_queue)))
    threads.append(threading.Thread(target=buildResponse, args=(decoded_queue, xmit_queue)))

    for thread in threads:
        thread.start()






if __name__ == "__main__":
    main()



