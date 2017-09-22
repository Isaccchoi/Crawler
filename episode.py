# Episode = namedtuple('Episode', ['no', 'image_url', 'title', 'rate', 'date'])
import os

class Episode():
    def __init__(self, webtoon, no, image_url, title, rate, date):
        self._webtoon = webtoon
        self._no = no
        self._image_url = image_url
        self._title = title
        self._rate = rate
        self._date = date


    @property
    def webtoon(self):
        return self._webtoon

    @property
    def no(self):
        return self._no

    @property
    def image_url(self):
        return self._image_url

    @property
    def title(self):
        return self._title

    @property
    def rate(self):
        return self._rate

    @property
    def date(self):
        return self._date

    @property
    def has_thumbnail(self):
        path = f"webtoon/{self.webtoon.titld_id}_thumbnail/"
        if not os.path.isdir(path):
            os.mkdir(path)
        if os.path.isfile(path+f"{self.no}.jpg"):
            return True
        return False