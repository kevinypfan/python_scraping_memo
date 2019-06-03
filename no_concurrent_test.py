from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import asyncio
import time

loop = asyncio.get_event_loop()

start = time.time()
tasks = []


def download_normal(url, file):
    with urlopen(url) as u, open(file, 'wb') as f:
        f.write(u.read())


async def download_async(url, file):
    with urlopen(url) as u, open(file, 'wb') as f:
        f.write(u.read())


urls = [
    'https://openhome.cc/Gossip/Encoding/',
    'https://openhome.cc/Gossip/Scala/',
    'https://openhome.cc/Gossip/JavaScript/',
    'https://openhome.cc/Gossip/Python/'
]

filenames = [
    'Encoding.html',
    'Scala.html',
    'JavaScript.html',
    'Python.html'
]

# for url, filename in zip(urls, filenames):
#     download_normal(url, filename)


for url, filename in zip(urls, filenames):
    task = loop.create_task(download_async(url, filename))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
# with ThreadPoolExecutor(max_workers=4) as executor:
#     for url, filename in zip(urls, filenames):
#         executor.submit(download_normal, url, filename)


end = time.time()
print(end - start)
