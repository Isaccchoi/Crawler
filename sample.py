import re
f = open('sample.txt', 'rt')
source = f.read().strip().replace('\t', '')

# print(source)


p = re.compile(r'<td.*?class="title".*?>.*?<a.*?>\w+.*?</td>', re.DOTALL)

result = re.findall(p, source)


for index, item in enumerate(result):
    print('==index %s ==' %index)
    # item = re.sub(r'>[\s\b\W]?<', " ", item)
    # print(item)
    cur_strip_item = re.sub(r'>[\s]*?<','>\n<', item, flags=re.DOTALL)
    # print(cur_strip_item)
    # inner_a = re.findall(r'(?<=<a.*?>$)\d+화.*?\w+.*?(?=</a>)', cur_strip_item)
    # inner_a = re.findall(r'\d+화.*?\w+', cur_strip_item)
    cur_title = re.sub(r'.*?<a.*?>(.*?)</a>.*?', r'\g<1>', cur_strip_item)
    print(cur_title)
    # print(inner_a)
print('Total items: ', len(result))
# print(result)
