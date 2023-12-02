import requests
from bs4 import BeautifulSoup
import ssl
import urllib
import os
import shutil

from dateutil import parser

try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context


def get_page_id(url_str):
    url_str = url_str.split("/")[-2]
    page_id = url_str.split("/")[0]
    return page_id


def running_spider(data_dir="data", npr_url='https://www.npr.org/?refresh=true',
                   npr_text_only_path="https://text.npr.org/"):
    cookies = {'choiceVersion': "1", 'dateOfChoice': "1584369909889", 'trackingChoice': "true"}
    soup = BeautifulSoup(requests.get(npr_url, cookies=cookies).content, 'html.parser')
    with open(os.path.join(os.getcwd(), f'{data_dir}/news.txt'), "w") as f:
        n = 1
        for a in soup.select('a[href]:has(h3.title)'):
            title = a.h3.text
            page_id = get_page_id(a['href'])
            page_url = npr_text_only_path + page_id
            try:
                response = urlopen(page_url)
                htmlparser = etree.HTMLParser()
                tree = etree.parse(response, htmlparser)
                paragraphs = tree.xpath("/html/body/main/article/div/div[3]/p")
                paragraphs = [p.text for p in paragraphs]
                paragraphs = [p for p in paragraphs if p is not None]
                topic_type = tree.xpath("/html/body/main/article/div/p/a[2]")[0].text
                written_by = tree.xpath("/html/body/main/article/div/div[1]/p[1]")[0].text
                date_str = tree.xpath("/html/body/main/article/div/div[1]/p[2]")[0].text
                date_str = date_str.replace(" •", "")
                date_str = date_str.replace("Updated ", "")
                dt = parser.parse(date_str)

                date = dt.strftime("%m/%d/%Y")

                if paragraphs is not None:
                    try:
                        paragraphs = "".join(paragraphs)
                    except TypeError:
                        print(paragraphs)
                news_article = ""
                news_article += '""""""""""""""""""""""""""""""""\n\n' + \
                                f"Article {n}\n" +  f"tile: {title}\n" \
                                + f"topic type: {topic_type}\n" + \
                                f"written by: {written_by}\n" + \
                                f"date: {date}\n" + "content:" + paragraphs + "\n\n"
                n += 1
                f.write(news_article)
                f.write('\n')

            except urllib.error.HTTPError:
                pass
    date_path = date.replace('/', "-")
    shutil.copyfile(os.path.join(os.getcwd(), 'data/news.txt'), os.path.join(os.getcwd(), f'historical_news_articles/news_{date_path}.txt'),)
    return True

