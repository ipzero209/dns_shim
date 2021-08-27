import dnslib
import dns.resolver



def externalResolver(domain):
    answer = ""
    try:
        answer = dns.resolver.resolve(domain, 'A')
    except dns.resolver.NoAnswer:
        ip = "timeout5"
    except dnslib.buffer.BufferError:
        ip = "timeout"
    except dnslib.dns.DNSError:
        ip = "timeout"
    except dns.exception.Timeout:
        ip = "timeout"
    except:
        ip = "timeout"
    if answer != "":
        for rr in answer:
            print('======================')
            print(rr)
            print('======================')
            ip = rr.address

    return ip