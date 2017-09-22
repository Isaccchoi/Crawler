"""
class NaverWebtoonCrawler생성
    초기화메서드
        webtoon_id
        episode_list (빈 list)
            를 할당

    인스턴스 메서드
        def get_episode_list(self, page)
            해당 페이지의 episode_list를 생성, self.episode_list에 할당

        def clear_episode_list(self)
            자신의 episode_list를 빈 리스트로 만듬

        def get_all_episode_list(self)
            webtoon_id의 모든 episode를 생성

        def add_new_episode_list(self)
            새로 업데이트된 episode목록만 생성

"""
import os

import pickle

import requests

import utils

webtoon_p = 696617


class NaverWebtoonCrawler:
    def __init__(self, webtoon_title=None):
        """
        1. webtoon_title이 주어지면
            1-1 해당 웹툰 검색결과를 가져와서
            1-2 검색결과가 1개면 해당 웹툰을
                self.webtoon에 할당
            1-3 검색 결과가 2개 이상이면 선택 가능하도록 목록을 보여주고
                input으로 입력 받음
            1-4 검색 결과가 없으면 다시 웹툰 검색하도록 함
        2. webtoon_title이 주어지지 않으면
            2-1. 웹툰 검색을 할 수 있는 input을 띄워줌
            2-1 이후는 1-2, 1-3을 따라감

        3. webtoon_id를 쓰던 코드를 전부 수정 (self.webtoon)을 사용
            self.webtoon은 webtoon타입 namedtuple
        """
        if webtoon_title:
            while True:
                find_result = self.find_webtoon(webtoon_title)
                if len(find_result) < 1:
                    webtoon_title = input("결과가 없습니다. 다시 입력하세요.: ")
                    continue
                elif len(find_result) == 1:
                    self.webtoon = find_result[0]
                    break
                else:
                    for i, webtoon in enumerate(find_result):
                        print(f"{i+1}번. 제목: {webtoon.title}")
                    print("결과가 어려개 입니다 번호를 골라 입력하시오.")
                    sel_num = input()
                    self.webtoon = find_result[int(sel_num)-1]
                    break
        self.episode_list = list()
        self.load(init=True)
        print(f"{self.webtoon}")

    @property
    def total_episode_count(self):
        """
        webtoon_id에 해당하는 실제 웹툰의 총 episode수를 리턴
        requests를 사용
        :return: 총 episode수 (int)
        """
        el = utils.get_webtoon_episode_list(self.webtoon.title_id)
        return int(el[0].no)

    @property
    def up_to_date(self):
        """
        현재 가지고있는 episode_list가 웹상의 최신 episode까지 가지고 있는지
        :return: boolean값
        """
        # total_episode_count = 웹상에 올라와 있는 갯수
        # total_episode_count = self.total_episode_count
        # cur_episode_count = 로컬상에 있는 갯수
        # cur_episode_count = utils.get_last_episode_local(self.webtoon.title_id)
        # 로컬상과 웹상이 같으면 True, 다르면 False
        # return total_episode_count == cur_episode_count
        return self.total_episode_count == len(self.episode_list)

    def update_episode_list(self, force_update=False):
        """
        1. recent_episode_no = self.episode_list에서 가장 최산화의 no
        2. while문 또는 for문 내부에서
            utils.get_webtoon_episode_list를 호출
            반환된 list(episode)들을 해당 episode의 no가
            recent_episoe_no보다 클때 까지만 self.episode_list에 추가

        self.episode_list에 존재하지 않는 episode들을 self.episode_list에 추가
        :param force_update: 이미 존재하는 episode도 강제로 업데이트
        :return: 추가된 episode의 수 (int)
        """
        # recent_episode_no = self.episode_list[0].split('|')[0]
        recent_episode_no = self.episode_list[0].no if self.episode_list else 0
        print('-Update episode list start(Recent episode no: %s)' % recent_episode_no)
        page = 1
        new_list = list()
        while True:
            print('Get webtoon episode list(Loop %s)' % page)
            # 게속해서 증가하는 'page'를 이용해 다음 episode 리스트들을 가져옴
            el = utils.get_webtoon_episode_list(self.webtoon.title_id, page)
            for episode in el:
                # 각 episode의 no가 recent episode_no보다 클 경우
                # self.episode_list에 추가
                if int(episode.no) > int(recent_episode_no):
                    new_list.append(episode)
                    if int(episode.no) == 1:
                        break
                else:
                    break
            # break가 호출되지 않았을 경우
            else:
                # 계속해서 진행해야 하므로 page값을 증가 시키고 continue로 처음으로 돌아감
                page += 1
                continue
            # el의  for문에서 break가 호출될 경우(더 이상 추가할 episode가 없다.)
            # while문을 빠져 나가기 위해 break 실행
            break
        self.episode_list = new_list + self.episode_list
        return len(new_list)

    def find_webtoon(self, title):
        """
        title에 주어진 문자열로 get_webtoon_list로 받아온 웹툰 목록에서
        일치하거나 문자열이 포함되는 Webtoon목록을 리턴
        :param title: 찾을 웹툰 제목
        :return: List(Webtoon)
        """
        webtoon_list = self.get_webtoon_list()
        try:
            return [webtoon for webtoon in webtoon_list if title in webtoon.title]
        except IndexError:
            return None
        # print("검색한 웹툰이 존재하지 않습니다")

    def get_webtoon_list(self):
        """
        네이버 웹툰의 모든 웹툰들을 가져온다.
        :return:
        """
        return utils.get_webtoon_list()

    def get_last_page_episode_list(self):
        el = utils.get_webtoon_episode_list(self.webtoon.title_id, 99999)
        self.episode_list = el
        return len(self.episode_list)

    def load(self, path=None, init=False):
        """
        현재폴더를 기준으로 db/<webtoon.title_id>.txt 파일의 내용을 불러와
        pickle로 self.episode_list를 복원
        :return:
        """
        try:
            if not path:
                path = f"./db/{self.webtoon.title_id}.txt"
            self.episode_list = pickle.load(open(path, 'rb'))
        except FileNotFoundError:
            if not init:
                print('파일이 없습니다')

    def make_list_html(self):
        """
        self.episode_list를 HTML파일로 만들어준다
        webtoon/{webtoon.title_id}.html
        1. webtoon폴더 있는지 검사 후 생성
        2. webtoon/{webtoon.title_id}.html 파일객체 할당 또는 with문으로 open
        3. open한 파일에 HTML앞부분 작성
        4. episode_list를 for문돌며 <tr>...</tr>부분 반복작성
        5. HTML뒷부분 작성
        6. 파일닫기 또는 with문 빠져나가기
        7. 해당파일 경로 리턴
        """
        """
        ex)
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            <table>
                <!-- 이부분을 episode_list의 길이만큼 반복 -->
                <tr>
                    <td><img src="...."></td>
                    <td>제목</td>
                    <td>별점</td>
                    <td>날짜</td>
                </tr>
            </table>
        </body>
        </html>
        :return: 파일의 경로
        """
        # webtoon/ 폴더 존재하는지 확인 후 없으면 생성
        if not os.path.isdir('webtoon'):
            os.mkdir('webtoon')
        filename = f'webtoon/{self.webtoon.title_id}.html'
        with open(filename, 'wt') as f:
            # HTML 앞부분 작성
            f.write(utils.LIST_HTML_HEAD)

            # episode_list순회하며 나머지 코드 작성
            for e in self.episode_list:
                f.write(utils.LIST_HTML_TR.format(
                    image_url=f'./{self.webtoon.title_id}_thumbnail/{e.no}.jpg',
                    title=e.title,
                    rate=e.rate,
                    date=e.date
                ))
            # HTML 뒷부분 작성
            f.write(utils.LIST_HTML_TAIL)
        return filename

    def save_list_thumbnail(self):
        """
        webtoon/{webtoon.title_id}_thumbnail/<episode_no>.jpg
        1. webtoon/{webtoon.title_id}_thumbnail이라는 폴더가 존재하는지 확인 후 생성
        2. self.episode_list를 순회하며 각 episode의 img_url경로의 파일을 저장
        :return: 저장한 thumbnail개수
        """
        # webtoon/{self.webtoon.title_id}에 해당하는 폴더 생성
        thumbnail_dir = f'webtoon/{self.webtoon.title_id}_thumbnail'
        os.makedirs(thumbnail_dir, exist_ok=True)

        # 각 episode의 img_url속성에 해당하는 이미지를 다운로드
        for episode in self.episode_list:
            response = requests.get(episode.image_url)
            filepath = f'{thumbnail_dir}/{episode.no}.jpg'
            if not os.path.exists(filepath):
                with open(filepath, 'wb') as f:
                    f.write(response.content)

    def save(self, path=None):
        """
        현재폴더를 기준으로 db/<webtoon.title_id>.txt 파일에
        pickle로 self.episode_list를 저장
        :return: 성공여부
        """
        if not path:
            path = "db"
        if not os.path.isdir(path):
            os.mkdir(path)
        pickle.dump(self.episode_list, open(f"./{path}/{self.webtoon.title_id}.txt", 'wb'))


nwc = NaverWebtoonCrawler("피에는 피피피")
# print(nwc.episode_list)
# nwc.update_episode_list()
# nwc.save_list_thumbnail()
# nwc.make_list_html()
# print(nwc.find_webtoon("선"))

# print(nwc.load())
# print(nwc.episode_list)
