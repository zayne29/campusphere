#coding=utf-8
import json
import execjs
import requests
from bs4 import BeautifulSoup as bs
import os

ua = 'Mozilla/5.0 (Linux; Android 11; M2102J2SC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36'

def getLogin(username,password):
    url="https://auth.sziit.edu.cn/authserver/login?service=https://sziit.campusphere.net/iap/loginSuccess"
    global session
    session=requests.session()
    g_response=session.get(url)
    # print(g_response.text)
    soup = bs(g_response.text, 'html.parser')
    dt=soup.find_all('input',type="hidden")

    # scripttxt = soup.find_all("script")
    # # print(scripttxt)
    # pattern = re.compile('var pwdDefaultEncryptSalt = "(.*)";')
    # pwdDefaultEncryptSalt = pattern.findall(str(scripttxt))
    # print(dt)
    d=[]
    for x in dt:
        d.append(x.get('value'))

    pd = execjs.compile(open(r"encrypt.js").read()).call('encryptAES',password,d[5])

    data={
        "username":username,
        "password":pd,
        "captchaResponse":"",
        "lt":d[0],
        "dllt":d[1],
        "execution":d[2],
        "_eventId":d[3],
        "rmShown":d[4],
        "rememberMe":"on"
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; SM-N9300 Build/R2MZBS) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.6985.79 Mobile Safari/537.36 okhttp/3.12.4'
               }
    session.post(url,data=data,headers=headers)








def getInfos():
    url = "https://sziit.campusphere.net/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay"


    response = session.post(url, headers={'Content-Type': 'application/json;charset=UTF-8'}, data="{}")
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
