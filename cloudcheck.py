#!/usr/bin/python




import requests





def checkRequest(domain):
    #TODO add api calls for DNS Security

    #Temp code for checking resolver flow
    if domain == "www.reddit.com":
        return "resolve"
    elif domain == "www.malware.hax":
        return "sinkhole"
    elif domain == "tunneling.steal":
        return "sinkhole"
    else:
        return "resolve"