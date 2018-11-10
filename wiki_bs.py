from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl

# option 1
context = ssl._create_unverified_context()
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon", context=context)

# option 2
# ssl._create_default_https_context = ssl._create_unverified_context
# html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')

bs = BeautifulSoup(html, 'html.parser')
# 這邊可以拿到所有 link
# for link in bs.find_all('a'):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])

# 透過這裡可以過濾掉不需要的 link 只拿 /wiki/ ........
for link in bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])
