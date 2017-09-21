import pickle
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from utils import Episode

# namedtuple 정의


# 기존 url에서 id 부분을 따로 받도록 변경을 하기 위해 id값 제거
webtoon_url = "http://comic.naver.com/webtoon/list.nhn?titleId="

# 유미의 세포들 id
webtoon_yumi = "651673"


def save_episode_list_to_file(webtoon_id, episode_list):
    filename = "{webtoon_id}_{first_episode_no}_{last_episode_no}.txt".format(
        webtoon_id=webtoon_id,
        first_episode_no=episode_list[0].no,
        last_episode_no=episode_list[-1].no,
    )
    with open(filename, 'wt') as f:
        for epi in episode_list:
            episode_info_string = (f"{epi.no}|{epi.image_url}|{epi.title}|{epi.rate}|{epi.date}")
            # f.write(','.join(epi) + "\n")
            f.write(episode_info_string + "\n")
    """
    episode_list로 전달된 Episode의 리스트를
    쉼표단위로 속성을 구분 라인 단위로 Episode를 구분해 저장

    ex)
    :param webtoon_id:
    :param episode_list:
    :return:
    """


def load_episode_list_from_file(path):
    """
    path에 해당 하는 file을 읽어 Episode리시트를 생성해 리턴

    :param path:
    :return:
    """
    # 리스트 형태로 담을 episode_list 정의

    with open(path, 'rt') as f:
        return [Episode._make(line.strip().split('|')) for line in f]


# webtoon_id값을 파라미터로
def get_webtoon_episode_list(webtoon_id, page=1):
    base_url = "http://comic.naver.com/webtoon/list.nhn?"
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


el = get_webtoon_episode_list(651673)
pickle.dump(el, open('yumi_pickle.txt', 'wb'))
# save_episode_list_to_file(651673, get_webtoon_episode_list(651673))
# load_episode_list_from_file("651673.txt")
