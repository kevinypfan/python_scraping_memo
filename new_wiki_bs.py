from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl
pages = set()


def getLinks(pageUrl):
    global pages
    ssl._create_default_https_context = ssl._create_unverified_context
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks('')
