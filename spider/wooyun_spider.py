#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate, compress',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}

# 获取总页数
url = "http://wooyun.org/bugs/new_public/page/%d"
r = requests.get(url % 1, headers=headers)
reg = r'<p class="page">[^x00-xff]\s\d*\s[^x00-xff]*,\s(\d*)\s[^x00-xff]'
pattern = re.compile(reg)
match = pattern.search(r.text)
page = int(match.group(1))

# 获取每一个bug的信息
for x in xrange(1, 2):
    r = requests.get(url % 2, headers=headers)
    reg2 = r'<tr>\s*<th>.*</th>\s*<td>' \
           r'<a href="(.*)">(.*)</a>\s*.*\s*</td>\s*<th>' \
           r'<a title=".*".*">(\d*)/(\d*)</a></th>\s*<th>' \
           r'<a title=".*" href=".*">(.*)</a></th>\s*</tr>'
    pattern = re.compile(reg2)
    match = pattern.findall(r.text)
    for i in xrange(0, len(match[x])):
        bug_url = match[i][0]
        bug_title = match[i][1]
        bug_comment = match[i][2]
        bug_concern = match[i][3]
        bug_author = match[i][4]
        if bug_concern >= 10:
            print(bug_title)
