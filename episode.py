# Episode = namedtuple('Episode', ['no', 'img_url', 'title', 'rating', 'created_date'])
import os
from urllib.parse import urlencode

import pickle
import requests
from bs4 import BeautifulSoup


class Episode:
    """
    namedtuple 'Episode'와 같은 역할을 할 수 있도록 생성
    """
    def __init__(self, webtoon, no, url_thumbnail, title, rating, created_date):
        self._webtoon = webtoon
        self._no = no
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._created_date = created_date

        self.thumbnail_dir = f'webtoon/{self.webtoon.title_id}_thumbnail'
        self.image_dir = f'webtoon/{self.webtoon.title_id}_images/{self.no}'
        # ex) webtoon/669233_images/1/01.jpg
        # ex) webtoon/669233_images/1/02.jpg
        # ex) webtoon/669233_images/1/03.jpg
        self.save_thumbnail()
        print(f"{self._no}{self._title}")

    @property
    def webtoon(self):
        return self._webtoon

    @property
    def no(self):
        return self._no

    @property
    def url_thumbnail(self):
        return self._url_thumbnail

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def created_date(self):
        return self._created_date

    @property
    def has_thumbnail(self):
        """
        현재경로/webtoon/{self.webtoon.title_id}_thumbnail/{self.no}.jpg
          파일이 있는지 검사 후 리턴
        :return:
        """
        path = f'{self.thumbnail_dir}/{self.no}.jpg'
        return os.path.exists(path)

    def save_thumbnail(self, force_update=True):
        """
        Episode자신의 img_url에 있는 이미지를 저장한다
        :param force_update:
        :return:
        """
        if not self.has_thumbnail or force_update:
            # webtoon/{self.webtoon.title_id}에 해당하는 폴더 생성
            os.makedirs(self.thumbnail_dir, exist_ok=True)
            response = requests.get(self.url_thumbnail)
            filepath = f'{self.thumbnail_dir}/{self.no}.jpg'
            if not os.path.exists(filepath):
                with open(filepath, 'wb') as f:
                    f.write(response.content)

    def save_contents(self):
        """

        :return:
        """

    def _save_images(self):
        """
        자기자신 페이지 (각 episode페이지)의 img들을 다운로드
        webtoon
            /{self.webtoon.title_id}_images
                /{self.episode.no}
                    /{각 loop index}.jpg
        :return:
        """
        os.makedirs(self.image_dir, exist_ok=True)

        # 웹툰 본문 페이지 (url_contents)
        params = {
            'titleId': self.webtoon.title_id,
            'no': self.no
        }
        url_contents = 'http://comic.naver.com/webtoon/detail.nhn?'\
                       + urlencode(params)
        # 본문 페이지에 대한 HTTP요청 응답
        response = requests.get(url_contents)
        # 응답의 text를 이용해 Soup객체 생성
        soup = BeautifulSoup(response.text)
        # soup객체에서 img tag들의 목록을 찾아내기
        img_list = soup.select_one('.wt_viewer').find_all('img')
        # img tag들에서 'src'속성만 가져와 url_img_list리스트를 생성
        url_img_list = [img['src'] for img in img_list]

        # 리스트를 순회하며 (각 item은 img의 src가 된다)
        for index, url in enumerate(url_img_list):
            # img에 대한 각 requests.get에는 url_contents가 Referer인 header가 필요
            headers = {
                'Referer': url_contents
            }
            # requests.get요청을 보냄
            response = requests.get(url, headers=headers)
            # 파일을 저장
            with open(f'{self.image_dir}/{index + 1}.jpg', 'wb') as f:
                f.write(response.content)

    def _make_html(self):



if __name__ == '__main__':
    el = pickle.load(open('db/697680.txt', 'rb'))
    for e in el:
        e._save_images()
        e.save_thumbnail()