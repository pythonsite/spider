
import requests

import http.cookiejar as cookielib

import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Referer":"https://www.zhihu.com/"
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")

try:
    session.cookies.load("cookie.txt",ignore_discard=True)
except:
    print("cookie未能加载")

def get_index():

    response = session.get("http://www.zhihu.com",headers=headers)
    return response.text

def get_xsrf():
    html = get_index()
    soup = BeautifulSoup(html,'lxml')
    res = soup.find("input",attrs={"name":"_xsrf"}).get("value")
    return res


def get_index2():
    response = session.get("http://www.zhihu.com",headers=headers)
    with open("index_page.html",'wb') as f:
        f.write(response.text.encode("utf-8"))

    print("ok")

def zhihu_login(account,password):
    '''
    知乎登录
    :param account:
    :param password:
    :return:
    '''
    _xsrf = get_xsrf()
    post_url = "https://www.zhihu.com/login/phone_num"
    post_data = {
        "_xsrf":_xsrf,
        "phone_num":account,
        "password":password,
        'captcha_type':'cn'
    }
    response = session.post(post_url,data=post_data,headers=headers)
    print(response.text)
    session.cookies.save()



zhihu_login('13121210484','ru10105417521')

# get_index2()