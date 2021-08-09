#!/usr/bin/python

from urllib.request import urlopen
import sys

def main(url):
    page = urlopen(url)
    html = page.read().decode('utf-8')
    print(html)

if __name__ == "__main__":
    main(sys.argv[1])