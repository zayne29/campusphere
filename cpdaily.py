#coding=utf-8
import json
import execjs
import requests
from bs4 import BeautifulSoup as bs
import os
from fake_useragent import UserAgent

ua = UserAgent()

def getLogin(username,password):
    url="https://auth.sziit.edu.cn/authserver/login?service=https://sziit.campusphere.net/iap/loginSuccess"
    global session
    session=requests.session()
    g_response=session.get(url)

    soup = bs(g_response.text, 'html.parser')
    dt=soup.find_all('input',type="hidden")
    # print(dt)
    d=[]
    for x in dt:
        d.append(x.get('value'))


    pd = execjs.compile(open(r"encrypt.js").read()).call('encryptAES',password,d[5])

    data={
        "username":username,
        "password":pd,
        "lt":d[0],
        "dllt":d[1],
        "execution":d[2],
        "_eventId":d[3],
        "rmShown":d[4],
        "rememberMe":"on"
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': ua.random
               }
    session.post(url,data=data,headers=headers)







def getInfos():
    url = "https://sziit.campusphere.net/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay"


    response = session.post(url, headers={'Content-Type': 'application/json;charset=UTF-8'}, data="{}")
    # print(response.text)
    d = json.loads(response.text)


    global signInstanceWid
    global signWid
    signInstanceWid=d["datas"]["unSignedTasks"][0]["signInstanceWid"]
    signWid=d["datas"]["unSignedTasks"][0]["signWid"]



def getForm(signInstanceWid,signWid):
    url = "https://sziit.campusphere.net/wec-counselor-sign-apps/stu/sign/detailSignInstance"
    payload = "\"signInstanceWid\": \"{a}\",\"signWid\": \"{b}\"".format(a=signInstanceWid,b=signWid)
    payload="{"+payload+"}"

    response = session.post(url, headers={'Content-Type': 'application/json;charset=UTF-8'}, data=payload)
    # print(response.text)
    d = json.loads(response.text)


    global awid
    global bwid
    awid=d["datas"]["extraField"][0]["extraFieldItems"][1]["wid"]
    bwid=d["datas"]["extraField"][1]["extraFieldItems"][1]["wid"]

    # print(awid)
    # print(bwid)


def submitForm(signInstanceWid,awid,bwid,extension):
    url = "https://sziit.campusphere.net/wec-counselor-sign-apps/stu/sign/submitSign"
    header= {
    'Content-Type': 'application/json;charset=UTF-8',
    'Cpdaily-Extension':extension
    }
    payload={"longitude":114.222966,"latitude":22.691566,"isMalposition":0,"abnormalReason":"","signPhotoUrl":"","isNeedExtra":1,"position":"中国广东省深圳市龙岗区龙格路301号","uaIsCpadaily":"true","signInstanceWid":str(signInstanceWid),"signVersion":"1.0.0","extraFieldItems":[{"extraFieldItemValue":"否","extraFieldItemWid":str(awid)},{"extraFieldItemValue":"否","extraFieldItemWid":str(bwid)}]}
    response = session.post(url, headers=header, json=payload)
    # print(payload)
    print(response.text)


if __name__ == '__main__':
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    extension = os.environ["CPDAILY_EXTENSION"]
    getLogin(username,password)
    getInfos()
    getForm(signInstanceWid,signWid)
    submitForm(signInstanceWid,awid,bwid,extension)

# print(m_signInstanceWid, m_signWid, awid, bwid)
