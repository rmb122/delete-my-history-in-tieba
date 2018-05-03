import json
import re
import sys

import bs4
import requests

startPageNumber = 1
endPageNumber = 3


def loadCookie(sess):
    cookies = open("/".join([sys.path[0], "cookie.json"])).read().replace("\n", "")
    cookies = json.loads(cookies)
    sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    for cookie in cookies:
        sess.cookies[cookie["name"]] = cookie["value"]


def getTbs(sess):
    success = False
    while not success:
        try:
            res = sess.get("http://tieba.baidu.com/dc/common/tbs", timeout=5)
            success = True
        except Exception as e:
            print(e)
            pass
    tbs = res.json()["tbs"]
    return tbs


def getReplyList(sess, startPageNumber, endPageNumber):
    replyList = list()
    tidExp = r"/([0-9]{1,})"
    pidExp = r"pid=([0-9]{1,})"
    cidExp = r"cid=([0-9]{1,})"

    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in page", number)

        url = "http://tieba.baidu.com/i/i/my_reply?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            exit(0)

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="a", attrs={"class": "b_reply"})
        for element in elements:
            reply = element.get("href")
            if reply.find("pid") != -1:

                tid = re.findall(tidExp, reply)
                pid = re.findall(pidExp, reply)
                cid = re.findall(cidExp, reply)

                replyDict = dict()
                replyDict["tid"] = tid[0]         
                if cid and cid[0] != "0":
                    replyDict["pid"] = cid[0]
                else:
                    replyDict["pid"] = pid[0]

                replyList.append(replyDict)

    return replyList


def deleteReply(sess, replyList):
    for replyDict in replyList:
        print("Now deleting", replyDict)

        url = "https://tieba.baidu.com/f/commit/post/delete"
        postData = dict()
        postData["tbs"] = getTbs(sess)
        for idName in replyDict:
            postData[idName] = replyDict[idName]
        res = sess.post(url, data=postData)

        print(res.text)

        if res.json()["err_code"] == 220034: #达到上限
            return


try:
    sess = requests.session()
    loadCookie(sess)
    replyList = getReplyList(sess, startPageNumber, endPageNumber)
    print("Collected", len(replyList), "replys")
    deleteReply(sess, replyList)

except Exception as e:
    print(e)
