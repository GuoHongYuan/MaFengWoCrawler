# 马蜂窝当季城市top5景点爬虫
# -*- coding:utf-8 -*-
import re
import time
from bs4 import BeautifulSoup
import json
import threading
import requests
import openpyxl
from openpyxl.workbook import Workbook
from lxml import etree
from Setting import UserAgent,IpFilter
from Setting.IpFilter import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class FengWo_crawler:

    def __init__(self):
        self.monthList = [113,116,119,122,125,128,131,134,137,140,143,146]
        self.pageList = [1,2,3]
        self.time = time.localtime(time.time())
        self.monthNum = self.monthList[self.time[1]-1]
        self.CityID = []
        self.url_ = 'http://www.mafengwo.cn/mdd/base/filter/getlist'

        self.mdd_urlList = []
        self.gonglve_url = {}

        self.timewait = 0

        self.SheetName = []

        self.dict = UserAgent.MY_USER_AGENT
        self.ipf = IpFilter('1')
        self.proxies = {'HTTP': 'localhost:8080'}

        self.headers = {
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Referer': 'http://www.mafengwo.cn/mdd/filter-tag-1400.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.headers_Common = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
        }
        self.outwb = Workbook()
        self.wo = self.outwb.active

    def initialization(self):
        self.headers['User-Agent'] = random.sample(self.dict, 1)[0]
        self.headers_Common['User-Agent'] = random.sample(self.dict, 1)[0]
        print self.headers['User-Agent']
        self.proxies = self.ipf.getIp()
        #self.proxies = {'HTTP': 'localhost:8080'}
        #s设置请求头和ip

    def getSheet(self,name,site):
        careerSheet = self.outwb.create_sheet(name,site)
        careerSheet.append(['名称', '电话', '网址', '用时参考', '交通', '门票', '开放时间', '景点位置', '概况'])
        return careerSheet

    def getNum(self,url_str,):
        pattern = re.compile(r'\d+')
        m = pattern.findall(url_str)
        return int(m[0])

    def getCountryID(self):
        for item in self.pageList:
            form_data = 'tag%5B%5D=' + str(self.monthNum) + '&page=' + str(item)
            time.sleep(self.timewait)
            self.initialization()

            req = requests.post(url=self.url_,data=form_data,headers=self.headers,proxies=self.proxies,verify=False).json()
            data1 = json.dumps(req, ensure_ascii=False)
            value = json.loads(data1)

            html = value['list']
            soup = BeautifulSoup(html, 'html.parser')
            for li in soup.find_all('li'):
                a = li.find('div',class_="img").find('a')
                self.CityID.append(self.getNum(a['href']))
        #print self.CityID
    def getNewMddUrl(self):
        for cityId in self.CityID:
            url = 'http://www.mafengwo.cn/jd/'+str(cityId)+'/gonglve.html'
            self.mdd_urlList.append(url)
        #print self.mdd_urlList
    def getGonglveUrl(self):
        for item in self.mdd_urlList:
            url = item
            #url = 'http://www.mafengwo.cn/jd/10183/gonglve.html'
            self.headers_Common['Referer'] = url
            time.sleep(self.timewait)
            self.initialization()

            req = requests.get(url=url,headers=self.headers_Common, proxies=self.proxies, verify=False)

            html = req.text
            html_ = etree.HTML(html)
            a = html_.xpath('/html/head/title')[0].text
            self.SheetName.append(a)
            soup = BeautifulSoup(html, 'html.parser')
            list = []
            try:
                for div in soup.find('div',class_='row row-top5').find_all('div',class_='info'):
                    href = div.find('div',class_='middle').find('h3').find('a')['href']
                    list.append('http://www.mafengwo.cn'+href)
                self.gonglve_url[item] = list
            except:
                print 'error'
        #print self.gonglve_url

    def getPoi(self):
        sheet = 0
        for Key,Value in self.gonglve_url.items():
            careerSheet = self.getSheet(self.SheetName[sheet],sheet)
            self.headers_Common['Referer'] = Key
            for url in Value:
                self.initialization()
                time.sleep(self.timewait)

                req = requests.get(url=url, headers=self.headers_Common, proxies=self.proxies, verify=False).text

                html = etree.HTML(req)
                try:
                    A = html.xpath('/html/body/div[2]/div[2]/div/div[3]/h1')[0].text
                except:
                    A = 'data Non-existent'
                try:
                    B = html.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[1]/div[2]')[0].text
                except:
                    B = 'data Non-existent'
                try:
                    C = html.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[2]/div[2]/a')[0].text
                except:
                    C = 'data Non-existent'
                try:
                    D = html.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[3]/div[2]')[0].text
                except:
                    D = 'data Non-existent'
                try:
                    E = html.xpath('/html/body/div[2]/div[3]/div[2]/dl[1]/dd')[0].text
                except:
                    E = 'data Non-existent'
                try:
                    F = html.xpath('/html/body/div[2]/div[3]/div[2]/dl[2]/dd/div')[0].text
                except:
                    F = 'data Non-existent'
                try:
                    G = html.xpath('/html/body/div[2]/div[3]/div[2]/dl[3]/dd')[0].text
                except:
                    G = 'data Non-existent'
                try:
                    H = html.xpath('/html/body/div[2]/div[3]/div[3]/div[1]/p')[0].text
                except:
                    H = 'data Non-existent'
                try:
                    I = html.xpath('/html/body/div[2]/div[3]/div[2]/div')[0].text
                except:
                    I = 'data Non-existent'
                careerSheet.append([A,B,C,D,E,F,G,H,I])
            sheet = sheet+1

    def SaveExcel(self):
        self.outwb.save("C:\DataAnalysis\\tools\python\project\GodAntData\MFO.xlsx")

    def test(self):
        self.headers_Common['Referer'] = 'http://www.mafengwo.cn/jd/10183/gonglve.html'
        self.initialization()
        request = urllib2.Request(url='http://www.mafengwo.cn/poi/7518.html', headers=self.headers_Common,proxies = self.proxies, verify=False)
        response = urllib2.urlopen(request)
        html = etree.HTML(response.read())
        a = html.xpath('/html/body/div[2]/div[3]/div[2]/ul/li[2]/div[2]/a')[0].text
        print a
fc = FengWo_crawler()
fc.getCountryID()
fc.getNewMddUrl()
fc.getGonglveUrl()
fc.getPoi()
fc.SaveExcel()
#fc.test()
