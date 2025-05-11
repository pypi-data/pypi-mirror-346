# -*- coding: utf-8 -*-
"""
@File    : crawler.py
@Time    : 2024/3/23 16:22:56
@Author  : lihao
@Contact : lihao2015@whu.edu.cn
"""

import os
import re
import logging
import argparse
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import aiohttp

try:
    from lh_tool.iterator import AsyncProcess, AsyncMultiProcess
except:
    from lh_tool.Iterator import AsyncProcess, AsyncMultiProcess


class Crawler:
    """
    Crawler

    Parameters:
        chunk_size(int): chunk size for download, default is 1024
        nprocs(int): nprocs for asynchronous multi-process download, default is 1, doesn't use multi-process
        concurrency(int): concurrency for asynchronous download, default is 0

    Example:
        .. code-block:: python

        url = "http://www.dili360.com/photo/column/6534.htm"
        name = "img"
        url_key = "src"
        pattern = "(.*.jpg)@!rw4"
        save_path = "images"
        crawler = Crawler()
        url_links = crawler.crawl(url, name, url_key, pattern)
        crawler.download(url_links, save_path)
    """

    def __init__(self, chunk_size=1024, nprocs=1, concurrency=0):
        self.chunk_size = chunk_size
        self.nprocs = nprocs
        self.concurrency = concurrency

    @staticmethod
    def check_url(url):
        """
        check url

        Args:
            url(str): url to check

        Returns:
            bool: True if url is valid, otherwise False
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            logging.error(e)
            return False

    @staticmethod
    def parse_url(
        url: str,
        name: str,
        url_key: str,
        pattern: str = ".*",
        attrs: Optional[Dict[str, str]] = {},
    ) -> List[str]:
        """
        parse url

        Args:
            url(str): url to parse
            name(str): tag name to find
            url_key(str): key to find download url
            pattern(str): pattern to match, default is ".*"
            attrs(dict, optinal): attrs to find

        Returns:
            url_links(list): list of url link
        """
        url_links = set()

        # compile pattern
        new_attrs = {url_key: pattern}
        new_attrs.update(attrs)
        for key, value in new_attrs.items():
            new_attrs[key] = re.compile(value)
        pattern = new_attrs[url_key]

        try:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "lxml")

            # find using attrs
            results = soup.find_all(name, new_attrs)
            for result in results:
                url_link = result.get(url_key)
                match = re.search(pattern, url_link)
                index = 1 if match.lastindex else 0
                url_link = match.group(index)
                if url_link:
                    url_links.add(url_link)

        except Exception as e:
            logging.error(e)

        return list(url_links)

    def crawl(
        self,
        url: str,
        name: str,
        url_key: str,
        pattern: str = ".*",
        attrs: Optional[Dict[str, str]] = {},
    ) -> List[str]:
        """
        crawl

        Args:
            url(str): url to crawl
            name(str): tag name to find
            url_key(str): key to find download url
            pattern(str): pattern to match, default is ".*"
            attrs(dict, optinal): attrs to find

        Returns:
            url_links(list): list of url link

        Exceprion:
            ValueError: when url is not valid
        """
        if not self.check_url(url):
            raise ValueError("url is not valid: {}".format(url))

        url_links = self.parse_url(url, name, url_key, pattern, attrs)
        url_links = [urljoin(url, url_link) for url_link in url_links]
        return url_links

    def download(self, url_links: List[str], save_path: str):
        """
        download

        Args:
            url_links(list[str]): list of url link to download
            save_path(str): path to save file

        Returns:
            save_file_list(list[str]): list of saved file
        """
        os.makedirs(save_path, exist_ok=True)
        save_file_list = [
            os.path.join(save_path, os.path.basename(url)) for url in url_links
        ]

        Process = AsyncMultiProcess if self.nprocs > 1 else AsyncProcess
        process = Process(
            self._download_single,
            nprocs=self.nprocs,
            concurrency=self.concurrency,
        )
        ret_list = process.run(url_links, save_file_list)
        logging.info(
            "total num: {}, finish num: {}".format(
                len(ret_list), sum(ret_list)
            )
        )
        save_file_list = [
            save_file
            for save_file, ret in zip(save_file_list, ret_list)
            if ret
        ]

        return save_file_list

    async def _download_single(self, url: str, save_file: str):
        """
        download single file asynchronously

        Args:
            url(str): url to download
            save_file(str): filename to save

        Returns:
            status(bool): download status
        """
        status = False
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    if res.status == 200:
                        with open(save_file, "wb") as f:
                            async for chunk in res.content.iter_chunked(
                                self.chunk_size
                            ):
                                f.write(chunk)
                            status = True
                    else:
                        logging.error(
                            "Failed to download file from {}. Status code: {}".format(
                                url, res.status
                            )
                        )
        except Exception as e:
            logging.error("Error occurred during download: {}".format(e))

        return status


def main():
    example = """
    example:
        crawler -u http://www.dili360.com/photo/column/6534.htm  -n img -k src -p "(.*.jpg)@\!rw4" -s images
    """
    parser = argparse.ArgumentParser(usage=example)
    parser.add_argument(
        "-u", "--url", type=str, help="url to crawl", required=True
    )
    parser.add_argument(
        "-n", "--name", type=str, help="tag name to find", required=True
    )
    parser.add_argument(
        "-k",
        "--url_key",
        type=str,
        help="key to find download url",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        help="pattern to match, default is '.*'",
        default=".*",
    )
    parser.add_argument(
        "-s", "--save_path", type=str, help="save path", required=True
    )
    opts = parser.parse_args()
    print(opts)

    import time

    start_time = time.time()

    url = opts.url
    name = opts.name
    url_key = opts.url_key
    pattern = opts.pattern
    save_path = opts.save_path
    crawler = Crawler()
    url_links = crawler.crawl(url, name, url_key, pattern)
    crawler.download(url_links, save_path)

    end_time = time.time()
    logging.info("total time: {}".format(end_time - start_time))


if __name__ == "__main__":
    main()
