import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from collections import namedtuple

Webtoon = namedtuple('Webtoon', ['title_id', 'image_url', 'title'])
webtoon_home = "http://comic.naver.com/webtoon/weekday.nhn"



def get_webtoon_list():
    webtoon_list = set()
    response = requests.get(webtoon_home)
    soup = BeautifulSoup(response.text, 'lxml')
    daily_all = soup.select_one('.list_area.daily_all')
    days =daily_all.select('div.col')

    for day in days:
        items = day.select('li')
        for item in items:
            img_url = item.select_one('div.thumb').a.img['src']
            title = item.select_one('a.title').get_text(strip=True)

            url_webtoon = item.select_one('a.title')['href']
            parse_result = urlparse(url_webtoon)
            queryset = parse_qs(parse_result.query)
            title_id = queryset['titleId'][0]

            webtoon = Webtoon(title_id=title_id, image_url=img_url, title=title)
            webtoon_list.add(webtoon)

    webtoon_list = list(webtoon_list)
    webtoon_list = sorted(list(webtoon_list), key=lambda x: x.title)


get_webtoon_list()