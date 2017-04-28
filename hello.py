from Common.downloader import Downloader
import re
import lxml.html
url = "https://mp.weixin.qq.com/s?__biz=MjM5NzcwNzgyMA==&mid=2650088974&idx=1&sn=5c65bd78d432fb1ea9edbb45478d17d1&chksm=bed46f4d89a3e65b940d7ec0d19da2e6da369ed63521df3d7e0cb2151c3f4c0e929c4847de05&scene=0#rd"
D = Downloader()
results = lxml.html.fromstring(D(url))
title = results.cssselect('h2#activity-name')[0]
#title = results.css('h2#activity-name::text').extract()
content = results.cssselect('div#js_content p')
print(title.text_content())
print(len(content))
for line in range(len(content)):
    print(content[line].tostring())
    print(content[line].text_content())
