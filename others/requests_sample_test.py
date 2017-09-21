import requests
from bs4 import BeautifulSoup
import collections

webtoon_url = "http://comic.naver.com/webtoon/list.nhn?titleId=651673"

source = requests.get(webtoon_url)
soup = BeautifulSoup(source.text, 'lxml')
# print(soup.prettify())

# with open('sample.txt', 'wt') as f:
#     f.write(soup.prettify())



# 이미지 주소
# 에피소드 제목
# 에피소드 별점
# 에피소드 등록일

webtoon_table = soup.select_one('table.viewList')
tr_list = webtoon_table.find_all('tr', recursive=False)

# List 정의
episode_list = []
Episode = collections.namedtuple('Episode', ['image_url', 'title', 'rate', 'date'])
for tr in tr_list:
    image = tr.select_one('img')['src']
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
    p = Episode(image, title, rate, date)
    episode_list.append(p)



for epi in episode_list:
    print(epi)
    print("===============================================")
