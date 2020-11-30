# -*- coding: UTF-8 -*-
import os
from aes128 import Aes128
import requests
from contextlib import closing
import m3u8


class Downloader:
    def __init__(self, temp_dir="./tmp", dest_dir='./data'):
        self.temp_dir = temp_dir
        self.dest_dir = dest_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir, exist_ok=True)

    def download_all(self, list_filename):
        index = 0
        with open(list_filename, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.replace('\n', '')
                url = url.replace('\r', '')
                items = url.split('|')
                
                if len(items) != 4:
                    continue
                self.download(items[0], items[1], items[2], items[3], index)
                index += 1
                break

    def download_m3u8(self, name, url, referer_url, index=None, progress=None):
        m3u8_obj = m3u8.load(url)
        seg = m3u8_obj.segments[-1]
        return self.download(name, seg.absolute_uri, seg.key.absolute_uri, referer_url,
                             index=index,
                             progress=progress)

    def download(self, name, url, key_url, referer_url, index=None, progress=None):
        if key_url == "" and 'm3u8' in url:
            return self.download_m3u8(name, url, referer_url, index=index, progress=progress)
            
        if index is not None:
            filename_tmp = os.path.join(self.temp_dir, "{:03}.{}.tmp".format(index, name))
            filename_key = os.path.join(self.temp_dir, "{:03}.{}.key".format(index, name))
            filename_dst = os.path.join(self.dest_dir, "{:03}.{}.ts".format(index, name))
        else:
            filename_tmp = os.path.join(self.temp_dir, "{}.tmp".format(name))
            filename_key = os.path.join(self.temp_dir, "{}.key".format(name))
            filename_dst = os.path.join(self.dest_dir, "{}.ts".format(name))
        if not os.path.exists(filename_key) or os.path.getsize(filename_key) <= 0:
            self._download(filename_key, key_url, referer_url)

        if not os.path.exists(filename_tmp):
            begin = url.index('start=')
            end = url.index('&', begin)
            start = url[begin:end]
            url = url.replace(start, 'start=0')

            self._download(filename_tmp, url, referer_url, progress)

        if not os.path.exists(filename_dst):
            file_size = self.decode(filename_tmp, filename_dst, filename_key)
        else:
            file_size = os.path.getsize(filename_dst)
        return filename_dst, file_size

    @staticmethod
    def decode(src, dst, key):
        with open(key, 'rb') as f:
            key = f.read()
        data = None
        with open(src, 'rb') as f:
            data = f.read()
        aes = Aes128(key)
        data = aes.decrypt(data)
        with open(dst, 'w+b') as f:
            f.write(data)
        return len(data)

    @staticmethod
    def _download(dst, url, referer=None, progress=None):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'}
        if referer is not None:
            headers["Referer"] = referer
        with open(dst, 'w+b') as f:
            if progress is None:
                response = requests.get(url, headers=headers)
                f.write(response.content)
                content_size = len(response.content)
            else:
                with closing(requests.get(url, headers=headers, stream=True)) as response:
                    chunk_size = 1024  # 单次请求大小
                    print(response.headers)
                    content_size = int(response.headers['content-length'])  # 总大小
                    finish_size = 0
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        finish_size += len(data)
                        if progress is not None:
                            progress(url, dst, finish_size, content_size)

        return content_size
