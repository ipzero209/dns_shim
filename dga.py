#!/usr/bin/python3


import os
import datetime
from time import sleep



def genDomain(day, hour, minute):
    domain = ""

    for i in range(24):
        day = ((day ^ 8 * day) >> 11) ^ ((day & 0xFFFFFFF0) << 17)
        hour = ((hour ^ 4 * hour) >> 25) ^ 16 * (hour & 0xFFFFFFF8)
        minute = ((minute ^ (minute << 13)) >> 19) ^ ((minute & 0xFFFFFFFE) << 12)
        domain += chr(((day ^ hour ^ minute) % 25) + 97)
    domain = domain + ".haxor"
    return domain



def main():
    count = 0
    while count < 1440:
        now = datetime.datetime.now()
        minute = now.minute
        hour = now.hour
        day = now.hour
        m_domain = genDomain(day, hour, minute)
        os.system('dig {}'.format(m_domain))
        count += 1
        sleep(60)


if __name__ == "__main__":
    main()