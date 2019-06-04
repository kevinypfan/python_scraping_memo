import youtube_dl
import requests
from bs4 import BeautifulSoup
import re
import os
import glob
import time


start = time.time()


base_youtube_url = 'https://www.youtube.com/watch?v='
download_path = r'/Users/fanzhenzhe/Music/pytube_downloads'
search_term = 'violeta'
need_qty = 21


def search_populate(need_qty, term):
    new_list = []
    search_index = 0
    key_set = set()
    first_vedios = search_by_term(term)[0:3]
    for d in first_vedios:
        t = tuple(d.items())[0:2]
        if t not in key_set:
            key_set.add(t)
            new_list.append(d)
    while len(key_set) < need_qty:
        for d in search_by_key(new_list[search_index]['link_id']):
            if len(key_set) >= need_qty:
                break
            t = tuple(d.items())[0:2]
            if t not in key_set:
                key_set.add(t)
                new_list.append(d)
    return new_list


def search_by_term(term):
    vedio_list_of_dict = []
    response = requests.get(
        'https://www.youtube.com/results?search_query=' + term)
    html = response.text
    bs = BeautifulSoup(html, 'html.parser')
    all_video_tag = bs.find_all('a', {'href': re.compile('(\/watch)')})
    for link in all_video_tag:
        if 'href' in link.attrs:
            try:
                vedio_list_of_dict.append({'title': link.attrs['title'], 'link_id': link.attrs['href'].split(
                    '=')[-1], 'views': int(''.join(re.search('([\d,]+)次$', link.span.attrs['aria-label']).group(1).split(',')))})
            except:
                # Key is not present
                pass
    return vedio_list_of_dict


def search_by_key(key):
    vedio_list_of_dict = []
    response = requests.get(
        base_youtube_url + key)
    html = response.text
    bs = BeautifulSoup(html, 'html.parser')
    all_video_tag = bs.find_all('a', {'href': re.compile(
        '(\/watch)'), 'class': re.compile('content-link')})
    for link in all_video_tag:
        if 'href' in link.attrs:
            try:
                vedio_list_of_dict.append({'title': link.attrs['title'], 'link_id': link.attrs['href'].split('=')[-1], 'views': int(''.join(
                    re.search('([\d,]+)次$', link.find('span', {'class': re.compile('view-count')}).text).group(1).split(',')))})
            except:
                # Key is not present
                pass
    return vedio_list_of_dict


download_list = search_populate(need_qty=need_qty, term=search_term)
print(len(download_list))
link_list = ['https://www.youtube.com/watch?v=' + el['link_id']
             for el in download_list]
ydl_opts = {
    'outtmpl': '/Users/fanzhenzhe/Music/pytube_downloads/{}/%(title)s.%(ext)s'.format(search_term),
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(link_list)


end = time.time()
print(end - start)
