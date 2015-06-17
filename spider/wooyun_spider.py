#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def getbugs(page):
    """

    得到wooyun的关注数大于10的bugs
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Encoding': 'gzip, deflate, compress',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
    }
    url = "http://wooyun.org/bugs/new_public/page/%d"

    if page == 'all':
        # 获取总页数
        r = requests.get(url % 1, headers=headers)
        reg = r'<p class="page">[^x00-xff]\s\d*\s[^x00-xff]*,\s(\d*)\s[^x00-xff]'
        pattern = re.compile(reg)
        match = pattern.search(r.text)
        page = int(match.group(1))

    # 生成一个html文件来保存
    bug_file = open('bug.html', 'w+')
    bug_file.write(r'<html><head>')
    bug_file.write(r'<meta http-equiv="content-type" content="text/html; charset=utf-8" /><br />')
    bug_file.write(r'<style>a:link {color: #FF4500; text-decoration:none;}'
                   r'a:active:{color: red; text-decoration:underline;}'
                   r'a:visited {color:black;text-decoration:none;}'
                   r'a:hover {color: blue; text-decoration:underline;}'
                   r'body{ font:12px "Trebuchet MS", Arial, Helvetica, sans-serif;}</style>')
    bug_file.write(r"<title>WooYun' s Bug List!!</title>")
    bug_file.write(r'</head>')
    bug_file.write(r"<h2 style='text-align:center;font-size:27px'>WooYun' s Bug List!!<h2><br />")


# 获取每一个bug的信息
    for x in xrange(1, int(page) + 1):
        r = requests.get(url % x, headers=headers)
        reg2 = r'<tr>\s*<th>.*</th>\s*<td>' \
               r'<a href="(.*)">(.*)</a>\s*.*\s*</td>\s*<th>' \
               r'<a title=".*".*">(\d*)/(\d*)</a></th>\s*<th>' \
               r'<a title=".*" href=".*">(.*)</a></th>\s*</tr>'
        pattern = re.compile(reg2)
        match = pattern.findall(r.text)
        for i in xrange(0, len(match)):
            bug_url = match[i][0]
            bug_title = match[i][1]
            bug_concern = int(match[i][3])
            if bug_concern > 10:
                bug_url = r'http://wooyun.org' + bug_url
                bug = r'<a class="link" href="%s" target="_blank">%s</a>' % (bug_url, bug_title)
                bug_file.write(bug)
                bug_file.write('<br />')
    bug_file.write(r'</html>')
    bug_file.close()


if __name__ == '__main__':
    filename = sys.argv[0].split('/')[-1]
    page = sys.argv[1]
    if len(sys.argv) > 2:
        print "usage: python %s page" % filename
    else:
        getbugs(page)
