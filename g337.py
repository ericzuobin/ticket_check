#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/20 下午2:52
# @Author  : Sahinn
# @File    : g337.py
import re
import urllib
import urllib2
import ssl
import json
mail_reciever = "sahinn@xxx.com"
mail_url = 'http://172.16.3.145:82/LeheQ'
config_url = "http://localhost:12306/config.json"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=TJP&purpose_codes=ADULT"
ssl._create_default_https_context = ssl._create_unverified_context


def url_get(url, timeout=30, encoding="utf8"):
    i_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                 "Referer": 'https://kyfw.12306.cn/otn/leftTicket/init'}
    req = urllib2.Request(url, headers=i_headers)
    result = urllib2.urlopen(req, timeout=timeout)
    content = result.read()
    if encoding != "utf8":
        content = unicode(content, encoding).encode("utf8")
    return content


def check():
    config_str = url_get(config_url)
    config = json.loads(config_str)
    status = False
    mail_content = u""
    for date in config['date']:
        url = ticket_url % (date)
        data = url_get(url)
        reg = u'\"data\":{.*?\".*\",(\".*?G337.*?\"),.*\".*?\"}'
        div_group = re.findall(reg, data, re.S | re.M)
        for d in div_group:
            info = d.split("|")
            temp = u'' + info[3] + u"[" + info[13] + u'],' + info[8] + u'-' + info[9] + u',特等座[' + unicode(info[30], 'utf-8') + u'],一等座[' \
                   + unicode(info[31], 'utf-8') + u'],二等座[' + unicode(info[32], 'utf-8') + u']\n'
            if not ("无" == info[30] and "无" == info[32] and "无" == info[31]):
               mail_content += temp
            status = True
    if not status:
        mail_content = u'没有获取到数据、请检查'
    if not mail_content:
        return
    send_mail(mail_content)


def send_mail(content):
    message = {"content": content, "encoding": "", "fromAddress": "qa@xxx.com", "fromDisplay": "", "htmlStyle": True,
               "mailType": "",
               "mailto": mail_reciever, "subject": u"12306买票提醒"}
    request = urllib2.Request(mail_url)
    message = json.dumps(message)
    data = {"q": "mailqueue", "p": "10001", "data": message, "datatype": 'json', "callback": ""}
    try:
        urllib2.urlopen(request, urllib.urlencode(data))
    except:
        return


def main():
    check()


if __name__ == "__main__":
    main()