#!/usr/bin/python



import json
import requests





def checkRequest(domain):

    host = "dns.service.paloaltonetworks.com"
    cert = "./device.pem"
    query_endpoint = "dns/query"

    q_body = {
        "query-data": [
            {
                "fqdn": f"{domain}"
            }
        ],
        "sn": "023001000306"
    }

    q_headers = {'Content-Type' : 'application/json'}
    q_params = {'json' : 'yes'}
    q_req = requests.post(f"https://{host}/{query_endpoint}",
                          headers=q_headers, params=q_params,
                          json=q_body, cert=cert)

    response = q_req.content.decode('utf-8')
    response = json.loads(response)
    category_list = []
    for x in range(len(response['sig-data'])):
        category_list.append(response['sig-data'][x]['final_category'])
    print(category_list)

    #Temp code for checking resolver flow
    # if domain == "www.reddit.com":
    #     return "resolve"
    # elif domain == "www.malware.hax":
    #     return "sinkhole"
    # elif domain == "tunneling.steal":
    #     return "sinkhole"
    # else:
    #     return "resolve"