import requests
from bs4 import BeautifulSoup, element
import re
import os
import glob
import youtube_dl
from concurrent.futures import ThreadPoolExecutor


class Spy_tube():
    def __init__(self,  unit_num=3, need_qty=10, time_le=5, view_reverse=False):
        self.base_youtube_url = 'https://www.youtube.com/watch?v='
        self.need_qty = need_qty
        self.view_reverse = view_reverse
        self.unit_num = unit_num
        self.time_le = time_le
        self.spyder_videos = None

    def search_populate(self, search_term):
        if type(search_term) != str:
            raise 'error'
        new_list = []
        search_index = 0
        key_set = set()
        first_vedios = self.search_by_term(search_term)[0:self.unit_num]
        for d in first_vedios:
            t = tuple(d.items())[0:2]
            print(t)
            if t not in key_set:
                key_set.add(t)
                new_list.append(d)
        while len(new_list) < self.need_qty:
            print(len(new_list))
            try:
                print(search_index)
                for d in self.search_by_key(new_list[search_index]['link_id'])[0:self.unit_num]:
                    if len(new_list) >= self.need_qty:
                        break
                    t = tuple(d.items())[0:2]
                    if t not in key_set:
                        key_set.add(t)
                        new_list.append(d)
            except IndexError:
                print(IndexError)
                break
            search_index += 1
        self.spyder_videos = new_list
        return new_list

    def search_by_term(self, search_term):
        vedio_list_of_dict = []
        response = requests.get(
            'https://www.youtube.com/results?search_query=' + search_term)
        html = response.text
        bs = BeautifulSoup(html, 'html.parser')
        all_video_tag = bs.find_all('div', {'class': 'yt-lockup-dismissable'})
        for link in all_video_tag:
            if type(link.find('a', {'class': 'yt-uix-tile-link'})) == element.Tag:
                try:
                    dict_data = {
                        'title': link.find('a', {'class': 'yt-uix-tile-link'}).attrs['title'],
                        'link_id': link.find('a', {'class': 'yt-uix-tile-link'}).attrs['href'].split('=')[-1],
                        'time': link.find('span', {'class': 'video-time'}).string,
                        'views': int(''.join(re.search('([\d,]+)次$', link.find('a', {'class': 'yt-uix-tile-link'}).span.attrs['aria-label']).group(1).split(',')))
                    }
                    vedio_list_of_dict.append(dict_data)
                except:
                    print('search_by_term error!')
                    # Key is not present
                    pass
        filtered_list = list(filter(lambda d: True if len(d['time'].split(':')) == 2 and int(
            d['time'].split(':')[0]) <= self.time_le else False, vedio_list_of_dict))
        return sorted(filtered_list, key=lambda k: k['views'], reverse=True) if self.view_reverse else filtered_list

    def search_by_key(self, key):
        vedio_list_of_dict = []
        response = requests.get(
            self.base_youtube_url + key)
        html = response.text
        bs = BeautifulSoup(html, 'html.parser')
        all_video_tag = bs.find_all('li', {'class': 'video-list-item'})
        for link in all_video_tag:
            content_link = link.find('a', {'class': 'content-link'}) if type(
                link.find('a', {'class': 'content-link'})) == element.Tag else None
            if content_link == None:
                continue
            if 'href' in content_link.attrs:
                try:
                    dict_data = {
                        'title': content_link.attrs['title'],
                        'link_id': content_link.attrs['href'].split('=')[-1],
                        'time': link.find('span', {'class': 'video-time'}).string,
                        'views': int(''.join(re.search('([\d,]+)次$', link.find('span', {'class': re.compile('view-count')}).text).group(1).split(',')))
                    }
                    vedio_list_of_dict.append(dict_data)
                except:
                    print('search_by_key error!')
                    # Key is not present
                    pass
        filtered_list = list(filter(lambda d: True if len(d['time'].split(':')) == 2 and int(
            d['time'].split(':')[0]) <= self.time_le else False, vedio_list_of_dict))
        return sorted(filtered_list, key=lambda k: k['views'], reverse=True) if self.view_reverse else filtered_list

    def download_all(self, max_workers=None, download_path=r'/tmp'):
        if self.spyder_videos == None:
            raise 'spyder_videos must be use search_populate function!'
        link_list = ['https://www.youtube.com/watch?v=' + el['link_id']
                     for el in self.spyder_videos]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for link in link_list:
                print(link)
                ydl_opts = {
                    'outtmpl': '{}/%(title)s.%(ext)s'.format(download_path),
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    executor.submit(ydl.download, [link])
