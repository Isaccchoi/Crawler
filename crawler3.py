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
import utils

webtoon_p = 696617

class NaverWebtoonCrawler:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.episode_list = list()
        self.load(init=True)

    @property
    def total_episode_count(self):
        """
        webtoon_id에 해당하는 실제 웹툰의 총 episode수를 리턴
        requests를 사용
        :return: 총 episode수 (int)
        """
        el = utils.get_webtoon_episode_list(self.webtoon_id)
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
        # cur_episode_count = utils.get_last_episode_local(self.webtoon_id)
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
        print('-Update episode list start(Recent episode no: %s)'% recent_episode_no)
        page = 1
        new_list = list()
        while True:
            print('Get webtoon episode list(Loop %s)' % page)
            # 게속해서 증가하는 'page'를 이용해 다음 episode 리스트들을 가져옴
            el = utils.get_webtoon_episode_list(self.webtoon_id, page)
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
                #계속해서 진행해야 하므로 page값을 증가 시키고 continue로 처음으로 돌아감
                page += 1
                continue
            # el의  for문에서 break가 호출될 경우(더 이상 추가할 episode가 없다.)
            # while문을 빠져 나가기 위해 break 실행
            break
        self.episode_list = new_list + self.episode_list
        return len(new_list)

    def get_last_page_episode_list(self):
        el = utils.get_webtoon_episode_list(self.webtoon_id, 99999)
        self.episode_list = el
        return len(self.episode_list)

    def load(self, path=None, init=False):
        """
        현재폴더를 기준으로 db/<webtoon_id>.txt 파일의 내용을 불러와
        pickle로 self.episode_list를 복원
        :return:
        """
        try:
            if not path:
                path = f"./db/{self.webtoon_id}.txt"
            self.episode_list = pickle.load(open(path, 'rb'))
        except FileNotFoundError:
            if not init:
                print('파일이 없습니다')


    def save(self, path=None):
        """
        현재폴더를 기준으로 db/<webtoon_id>.txt 파일에
        pickle로 self.episode_list를 저장
        :return: 성공여부
        """
        if not path:
            path = "db"
        if not os.path.isdir(path):
            os.mkdir(path)
        pickle.dump(self.episode_list, open(f"./{path}/{self.webtoon_id}.txt", 'wb'))




nwc = NaverWebtoonCrawler(webtoon_p)
print(nwc.episode_list)
# print(nwc.up_to_date)
# print(nwc.get_last_page_episode_list())
# print(nwc.update_episode_list())
# print(nwc.save())
# nwc.episode_list = list()
# print(nwc.load())
# print(nwc.episode_list)
