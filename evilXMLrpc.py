#!/usr/bin/env python3
# Author: Juan García aka liandd
import signal
from termcolor import colored
import sys
import argparse


# Ctrl_c
def def_handler(sig, frame):
    print(colored("\n[!] Saliendo...", "red"))
    sys.exit(1)


# Ctrl_c
signal.signal(signal.SIGINT, def_handler)


def get_arguments():
    parser = argparse.ArgumentParser(
        description='evilXMLrpc passwd bruteforcing attack by liandd')
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


def main():
    URL, NAME, WORDLIST = get_arguments()
    print(colored(f"Los argumentos son {URL}, {NAME}, {WORDLIST}", "green"))
    sys.exit(0)


if __name__ == '__main__':
    main()
