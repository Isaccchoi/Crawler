from bs4 import BeautifulSoup

f = open('sample.txt', 'rt')
source = f.read()
soup = BeautifulSoup(source, 'lxml')


# print(soup.prettify())

webtoon_table = soup.select_one('table.viewList')
tr_list = webtoon_table.find_all('tr', recursive=False)
for tr in tr_list:
    # tr.contets[1]
    td_title = tr.select_one('td.title')
    title = td_title.get_text(strip=True)
    print(title)
