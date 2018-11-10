from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.find_all(lambda tag: len(tag.attrs) == 2))
# print(bs.find('table', {'id': 'giftList'}).children)

# for child in bs.find('table', {'id': 'giftList'}).children:
#     print(child.find('img'))
