# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import string
import json

#从西刺网爬取id
def ipCrawl(page):
    #requests的Session可以自动保持cookie,不需要自己维护cookie内容
    filename = 'C:\DataAnalysis\\tools\python\project\GodAntData\Setting\ip.json'  # 储存位置
    count = 0

    for i in range(1,page+1):
        reqSession = requests.Session()
        url = 'http://www.xicidaili.com/nt/%d' % i  # 普通ip
        headers = {'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Referer': 'http://www.xicidaili.com/nn/',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   }
        response_text = reqSession.get(url = url, headers = headers)
        response_text.encoding = 'utf-8'
        rephtml = response_text.text
        mainForm = BeautifulSoup(rephtml, 'lxml')
        tableForm = BeautifulSoup(str(mainForm.find_all(id='ip_list')), 'lxml')
        List_ip = tableForm.table.contents

        pattern1 = re.compile(r'\d.\d')
        pattern2 = re.compile(r'u.*')
        pattern3 = re.compile(r'\d+')
        _json = dict()


        for index in range(len(List_ip)):
            if index % 2 == 1 and index != 1:
                dom = etree.HTML(str(List_ip[index]))
                LiveTime = dom.xpath('//td[9]')[0].text
                LiveTime1 = pattern2.search(LiveTime).group()
                ConSpeed = dom.xpath('//td[7]/div/@title')[0]
                ConSpeed1 = pattern1.search(ConSpeed).group()
                if LiveTime1 == "u5929" :
                    if string.atof(ConSpeed1) <0.3:  #取掉生存天数过小和响应时间过长的ip
                        count = count+1
                        _json["ip"] = dom.xpath('//td[2]')[0].text
                        _json["port"] = dom.xpath('//td[3]')[0].text
                        _json["protocol"] = dom.xpath('//td[6]')[0].text
                        _json["LiveTime"] = pattern3.search(LiveTime).group()+'天'
                        _json["ConSpeed"] = ConSpeed1+'秒'
                        with open(filename, 'a') as outfile:  # 追加模式
                            json.dump(_json, outfile, ensure_ascii=False)
                        with open(filename, 'a') as outfile:
                            outfile.write(',\n')
        print "第%d页爬取完成，总计%d条ip" %(i,count)


if __name__ == '__main__':
    ipCrawl(2)  #爬取的页数


'''
scrapy startproject name


    for tr in mainForm.find('div',id="wrapper").find('div',class_="clearfix proxies").find('table', id="ip_list").find_all('tr'):
        for td in tr.find_all('td'):
           print td
        print '-----------------------------'

'''

