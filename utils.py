import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from collections import namedtuple

Episode = namedtuple('Episode', ['no', 'image_url', 'title', 'rate', 'date'])
base_url = "http://comic.naver.com/webtoon/list.nhn?"


def get_webtoon_episode_list(webtoon_id, page=1):
    params = {
        'titleId': webtoon_id,
        'page': page,
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    webtoon_table = soup.select_one('table.viewList')
    tr_list = webtoon_table.find_all('tr', recursive=False)

    # List 정의
    episode_list = list()

    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list) < 4:
            continue
        image = tr.select_one('img')['src']
        # Episode 고유의 no
        url_episode = tr.a.get('href')
        parse_result = urlparse(url_episode)
        queryset = parse_qs(parse_result.query)
        no = queryset['no'][0]
        # image_url = td_image['src']s
        # print(image_url)
        title = tr.select_one('td.title').get_text(strip=True)
        # title = td_title.get_text(strip=True)
        # print(title)
        rate = tr.select_one('div.rating_type').get_text(strip=True)
        # rate = td_rate.get_text(strip=True)
        # print(rate)
        date = tr.select_one('td.num').get_text(strip=True)
        # date = td_date.get_text(strip=True)
        # print(date)
        p = Episode(no, image, title, rate, date)
        episode_list.append(p)
    return episode_list


def get_total_episode_count(webtoon_id):
    params = {
        'titleID': webtoon_id,
        'page': 1
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    webtoon_table = soup.select_one('table.viewList')
    tr_list = webtoon_table.find_all('tr', recursive=False)
    url_episode = tr_list[0].a.get('href')
    parse_result = urlparse(url_episode)
    queryset = parse_qs(parse_result.query)
    no = queryset['no'][0]
    return no


def get_last_episode_local(webtoon_id):
    path = f"{webtoon_id}.txt"
    with open(path, 'rt') as f:
        return int(f.readline().split('|')[0])

# get_last_episode_local(651673)
