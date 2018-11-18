import time
import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
           }

# pre-defined parameters
session = requests.Session()
stock = 44278
nCourts = 15

def Login_sup():
    login_url = "https://cas.sysu.edu.cn/cas/login"
    captcha_url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    self_url = "http://gym.sysu.edu.cn/yyuser/personal.html"
    login_form = {"username": "",
                "password": "",
                "captcha": "",
                "_eventId": "submit",
                "geolocation": "",
                }

    r = session.get(captcha_url)
    with open('captcha.png', 'wb') as file:
        file.write(r.content)
    capt = input('Please input captcha: ')
    login_form['captcha'] = capt

    r = session.get(login_url)
    soup = BeautifulSoup(r.text, features="html.parser")
    exec = soup.select("input[name='execution']")[0]['value']
    login_form['execution'] = exec

    with open("config.json", "r") as file:
        conf = json.load(file)
        login_form["username"] = conf["NetID"]
        login_form["password"] = conf["password"]

    r = session.post(login_url, headers = headers, data = login_form)
    r = session.get(self_url, headers = headers)
    return r.url == self_url

def login():
    while (not Login_sup()):
        print("Wrong captcha or password")
    print("Login success.")
    init()

def ckd(stock, stockdetailids):
    south_book_url = "http://gym.sysu.edu.cn/order/show.html?id=61"
    east_book_url = "http://gym.sysu.edu.cn/order/show.html?id=35"

    part0 = '{"stock":{"'
    part1 = '":"1"},"istimes":"1","stockdetailids":"'
    part2 = '"}'
    param = part0 + str(stock) + part1 + str(stockdetailids) + part2

    book_form = {"param": param}
    r = session.post(south_book_url, headers = headers, data = book_form)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, features="html.parser")
    ls = soup.select("td")
    if len(ls) == 0:
        rt = "ERROR"
    else:
        rt = ls[0].get_text() + ' ' + ls[1].get_text() + ' ' + ls[2].get_text()
    return rt

def bkd(stock, stockdetailids):
    confirm_url = "http://gym.sysu.edu.cn/order/book.html"
    part0 = '{"activityPrice":0,"activityStr":null,"address":null,"dates":null,"extend":null,"flag":"0","isbookall":"0","isfreeman":"0","istimes":"1","merccode":null,"order":null,"orderfrom":null,"remark":null,"serviceid":null,"shoppingcart":"0","sno":null,"stock":{"'
    part1 = '":"1"},"stockdetail":{"'
    part2 = '":"'
    part3 = '"},"stockdetailids":"'
    part4 = '","subscriber":"0","time_detailnames":null,"userBean":null}'
    param = part0 + str(stock) + part1 + str(stock) + part2 + str(stockdetailids)
    param = param + part3 + str(stockdetailids) + part4

    confirm_form = {"param": param,
                 "json": "true",
                 }
    r = session.post(confirm_url, headers = headers, data = confirm_form)
    r.encoding = "utf-8"
    jsn = json.loads(r.text)
    return jsn["message"]

def init():
    # pre-defined parameters
    check_sdid = 334330
    print("Please wait while updating config.json...")
    res_str = ""
    global stock
    with open("config.json", "r") as file:
        conf = json.load(file)
        weekday_stock = int(conf["weekday_stock"])
        weekend_stock = int(conf["weekend_stock"])
        nCourts = int(conf["nCourts"])
    
    s1 = bkd(weekday_stock, check_sdid)
    s2 = bkd(weekend_stock, check_sdid)
    ok_str = "预订失败，座位已被预订"
    ori_weekday_stock = weekday_stock
    ori_weekend_stock = weekend_stock
    while s1 != ok_str and s2 != ok_str:
        weekday_stock += 1
        s1 = bkd(weekday_stock, check_sdid)
        weekend_stock += 1
        s2 = bkd(weekend_stock, check_sdid)
    if s1 == ok_str:
        conf["weekday_stock"] = str(weekday_stock)
        stock = weekday_stock
        res_str = "weekday_stock: " + str(ori_weekday_stock) + " -> " + str(weekday_stock)
    else:
        conf["weekend_stock"] = str(weekend_stock)
        stock = weekend_stock
        res_str = "weekdend_stok: " + str(ori_weekend_stock) + " -> " + str(weekend_stock)

    if ori_weekday_stock == weekday_stock and ori_weekend_stock == weekend_stock:
        res_str = "Already up-to-date."
    else:
        with open("config.json", "w") as file:
            json.dump(conf, file)
    print("Updating done. " + res_str)
