# -*- coding:UTF-8 -*-
import subprocess as sp
from lxml import etree
import requests
import random
import re
import random
import json

class IpFilter():  #过滤IP
    def __init__(self,str):
        self.str = str
        self.ip = ''
        self.file1 = open('C:\DataAnalysis\\tools\python\project\GodAntData\Setting\ip.json', 'r')  # 打开文件
        self.jsonDict = json.load(self.file1)  # 加载json
        self.file1.close()  # 关闭连接

    def check_ip(self):
        cmd = "ping -n 3 -w 3 %s" # 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
        p = sp.Popen(cmd %self.ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)  # 执行命令
        lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
        out = p.stdout.read().decode("gbk") # 获得返回结果并解码
        #print (out)
        lose_time = lose_time.findall(out) # 丢包数
        # 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
        if len(lose_time) == 0:
            print "----------------LOST IP PACKET---------------------"
            return False
        else:
            lose = int(lose_time[0])
            if lose > 1:
                return False
            else:
                return True

    def getIp(self):
        jsonDict = self.jsonDict

        index = random.randint(0, len(jsonDict)-1)  # 随机下角标
        ipRandom = jsonDict[index]["ip"]  # 随机IP
        print '----random IP IS----------:%s' % str(ipRandom)
        # 测试ip
        self.ip = ipRandom
        if self.check_ip():
            print '-----------------Good IP--------------'
            return {jsonDict[index]["protocol"] : jsonDict[index]["ip"]+':'+jsonDict[index]["port"]}
        else:
            print '-----------------Bad IP----------------'
            return self.getIp()


if __name__ == '__main__':
    ipf = IpFilter('1')
    print ipf.getIp()
