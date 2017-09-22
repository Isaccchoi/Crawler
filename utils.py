import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from collections import namedtuple

from episode import Episode


# Episode = namedtuple('Episode', ['no', 'image_url', 'title', 'rate', 'date'])
Webtoon = namedtuple('Webtoon', ['title_id', 'image_url', 'title'])
base_url = "http://comic.naver.com/webtoon/list.nhn?"
webtoon_home = "http://comic.naver.com/webtoon/weekday.nhn"

def get_webtoon_episode_list(webtoon, page=1):
    params = {
        'titleId': webtoon.title_id,
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
        p = Episode(webtoon, no, image, title, rate, date)
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
    return webtoon_list


LIST_HTML_HEAD = '''<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <style>
        body {
            padding-top: 10px;
        }
        img {
            height: 34px;
        }
        .table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {
            font-size: 11px;
            height: 34px;
            line-height: 34px;
        }
        .table>thead>tr>td, .table>thead>tr>th {
            height: 20px;
            line-height: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
<table class="table table-stripped">
<colgroup>
    <col width="99">
    <col width="*">
    <col width="141">
    <col width="76">
</colgroup>
<thead>
    <tr>
        <th>이미지</th>
        <th>제목</th>
        <th>별점</th>
        <th>등록일</th>
    </tr>
</thead>
'''

LIST_HTML_TR = '''<tr>
    <td><img src="{image_url}"></td>
    <td>{title}</td>
    <td>{rate}</td>
    <td>{date}</td>
</tr>
'''

LIST_HTML_TAIL = '''</table>
</div>
</body>
</html>
'''

