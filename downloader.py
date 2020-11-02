# -*- coding: UTF-8 -*-
import os
from aes128 import Aes128
import requests


class Downloader:
    def __init__(self, temp_dir="./tmp"):
        self.temp_dir = temp_dir
        self.dest_dir = "."
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

    def download_all(self, list_filename, dest_dir="./dst"):
        self.dest_dir = dest_dir
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir, exist_ok=True)
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

    def download(self, name, url, key_url, referer_url, index=None):
        if index is not None:
            src = os.path.join(self.temp_dir, "{:03}.{}.tmp".format(index, name))
            key = os.path.join(self.temp_dir, "{:03}.{}.key".format(index, name))
            dst = os.path.join(self.dest_dir, "{:03}.{}.ts".format(index, name))
        else:
            src = os.path.join(self.temp_dir, "{}.tmp".format(name))
            key = os.path.join(self.temp_dir, "{}.key".format(name))
            dst = os.path.join(self.dest_dir, "{}.ts".format(name))
        if not os.path.exists(key):
            key_data = self._download(key_url, referer_url)
            with open(key, 'w+b') as f:
                f.write(key_data)

        if not os.path.exists(src):
            begin = url.index('start=')
            end = url.index('&', begin)
            start = url[begin:end]
            url = url.replace(start, 'start=0')

            data = self._download(url, referer_url)
            with open(src, 'w+b') as f:
                f.write(data)

        if not os.path.exists(dst):
            self.decode(src, dst, key)
        return dst

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

    @staticmethod
    def _download(url, referer=None):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
        if referer is not None:
            header["Referer"] = referer
        response = requests.get(url, headers=header)
        return response.content
