#!/usr/bin/env python
# encoding: utf-8

import requests
import json
import bs4

capturePicUrl = 'http://select.pdgzf.com/ValidationImage.aspx'
url = 'http://select.pdgzf.com/'

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Cookie':'ASP.NET_SessionId=sn4l0ou1h4cmcieay1kkszsa',
    'Host':'select.pdgzf.com',
    'Origin':'http://select.pdgzf.com',
    'Referer':'http://select.pdgzf.com/',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
# 这一步比较重要, 建立一个全局session,以后所有的访问都通过这个session
session = requests.session()

def get_captcha():
    t = session.get(capturePicUrl, headers=headers)
    with open('image.jpg', 'wb') as f:
        f.write(t.content)

    try:
        from PIL import Image
        im = Image.open('image.jpg')
        im.show()
        im.close()
    except:
        print 'error'

    captcha = raw_input('输入验证码：')
    return captcha

def login(username, password):
    SecretCode = get_captcha()
    print SecretCode

    datas = {
        '__VIEWSTATE':'/wEPDwUJMTkyNjA2OTMxZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUOVmFsaWRhdGlvbkNvZGUFEUNvbVZhbGlkYXRpb25Db2RlhF4Jy70OuT/FKbJLGYS1axQnuYoSgk10/s4UoUgsYGU=',
        '__EVENTVALIDATION':'/wEWCwKWpYLFDQKvruq2CAKyxeCRDwLuh+HJAwLx/pfKBALLt6XeCAKU+MiVBwLArL9oAtfawfcCAvKV8L0OAqLT2SEMB+8L3R3/d9hfdaxN/fHkasWnj5ytRsm7SVg9s1VTBQ==',
        'UserName':username,
        'PassWord':password,
        'Vercode':SecretCode,
        'EmpLogin':u'登录'.encode('gb2312'),
        'ComName':'',
        'ComPassWord':'',
        'ComVercode':'',
    }

    session.post(url, data=datas, headers=headers)

def processPage(url, index, f):
    data = {
        'qy':'',
        'page':index
    }

    html = session.get(url, data=data, headers=headers)
    soup = bs4.BeautifulSoup(html.text)
    icount = 0
    strlist = []
    for ol in soup.ol.find_all('p'):
        for s in ol.stripped_strings:
            if -1 == s.find(u'配套设备'):
                strlist.append(s)
            icount += 1
        if icount % 8 == 0:
            # 每行的数据格式已|分格
            f.write('|'.join(strlist).encode('utf-8'))
            f.write('\n')
            # 清空list
            strlist[:] = []


if __name__ == '__main__':
    login('yourusername','yourpassword')
    with open('result.txt', 'w') as f:
        for i in range(38):
            processPage(url+'Admin/personalUser.aspx',i+1, f)
