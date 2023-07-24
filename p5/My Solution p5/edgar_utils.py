import re, netaddr
from bisect import bisect
import pandas as pd

    
class Filing:
    def __init__(self, html):
        # print(html, "this is the html\n") 
        correct_dates = re.findall(r"((19|20)\d{2}-\d{2}-\d{2})", html)
        # print(correct_dates)
        self.dates = [m[0] for m in correct_dates]

        sic = re.findall(r"SIC=(\d+)", html)
        if sic == []:
            self.sic = None
        else:
            self.sic = int(sic[0])
        
        self.addresses = []
        
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                lines.append(line.strip())
                #print(line.strip())
            if lines != []:
                self.addresses.append("\n".join(lines))

    def state(self):
        for address in self.addresses:
            #print(address)
            place = re.findall(r"([A-Z][A-Z]) \d{5}", address)
            
            if place:
                return place[0]
        else:
            return None

ips = pd.read_csv("ip2location.csv")
           
a=list(ips["low"])
def lookup_region(ip_address):
    ip_address = re.sub(r"[^\d\.]", "0",ip_address)
    ip_int = int(netaddr.IPAddress(ip_address))
    idx = bisect(a, ip_int)
    region = ips.at[idx-1,"region"]
    return region
