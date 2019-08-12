import concurrent.futures

import requests
from lxml import etree


class ThreadPoolCrawler:
    """线程池爬虫

    继承该类实现 parse_response 方法从HTML中提取信息
    实例属性：
    - urls: 需要爬取的url
    - concurrency: 线程池数量，默认为10

    """
    def __init__(self, urls, concurrency=10, **kwargs):
        self.urls = urls
        self.concurrency = concurrency
        self.results = []

    def parse_response(self, url, response):
        raise NotImplemented

    def get(self, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        if 'headers' not in kwargs:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            }
            kwargs['headers'] = headers

        return requests.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            future_to_url = {
                executor.submit(self.get, url): url for url in self.urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response = future.result()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                else:
                    self.parse_response(url, response)


class KKCrawler(ThreadPoolCrawler):
    def parse_response(self, url, response):
        dom = etree.HTML(response.text)
        results = dom.xpath('//h3[@class="card-title"]/a/text()')
        print(results)


def main():
    urls = ['https://liyuankun.cn/blog']
    spider = KKCrawler(urls)
    spider.run()

if __name__ == '__main__':
    main()