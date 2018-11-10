from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as _:
        return None
    try:
        bs = BeautifulSoup(html . read(), 'html.parser')
        title = bs . body . h1
    except AttributeError as _:
        return None
    return title


title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)
