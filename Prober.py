#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request, ssl, argparse, sys, re
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx = ssl.check_hostname = False
ctx = ssl.CERT_NONE

Header = {"User-agent":"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

def Request(Url):
    try:
        if Argv.SSL:
            Url = "https://"+Url.strip()+"/"
        else:
            Url = "http://"+Url.strip()+"/"
        Req = urllib.request.Request(url=Url,headers=Header)
        Resp = urllib.request.urlopen(Req,context=ctx,timeout=Argv.Timeout)
        if Resp.code != 404:
            print(f"{Url} [{Resp.code}] [{re.findall(r'<title[^>]*>([^<]+)</title>', Resp.read().decode())[0]}]  [{len(Resp.read())}]")
    except:
        pass

if __name__ == "__main__":
    Parser = argparse.ArgumentParser(description="Aporlorxl23 HTTP Fuzzer")
    Parser.add_argument("-d","--domains",dest="Domains",required=True,default="Domains.txt",type=str,help="Domains File Path [Domains.txt]")
    Parser.add_argument("-c","--concurrent",dest="Concurrent",required=False,type=int,default=25,help="Concurrent Count [25]")
    Parser.add_argument("-t","--timeout",dest="Timeout",required=False,type=int,default=5,help="Timeout [5]")
    Parser.add_argument("-s","--ssl",dest="SSL",required=False,type=bool,default=False,help="SSL [False]")
    Argv = Parser.parse_args()
    try:
        with open(Argv.Domains,"r") as inputdata:
            Urls = inputdata.readlines()
    except:
        print(f"[-] {Argv.Domains} Not Found!")
        sys.exit(1)
    print(f"Domains: {Argv.Domains} Concurrent: {Argv.Concurrent} Timeout: {Argv.Timeout} SSL: {Argv.SSL}")
    executor = ThreadPoolExecutor(max_workers=Argv.Concurrent)
    executor.map(Request, Urls)
