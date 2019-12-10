# -*- coding: utf-8 -*-

import json
import re
import sys
import traceback

import bs4
import requests

GlobalConfig = {}
DefaultConfig = {
    "DryRun": False,
    "NeedConfirm": True,
    "DeferCommit": True
}


def GetConfig(key):
    result = GlobalConfig.get(key, DefaultConfig[key])
    if result is None:
        raise RuntimeError("Invalid key {}.".format(key))
    return result


def loadCookie(sess):
    cookies = open("/".join([sys.path[0], "cookie.json"])
                   ).read().replace("\n", "")
    cookies = json.loads(cookies)
    sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    for cookie in cookies:
        sess.cookies[cookie["name"]] = cookie["value"]


def getTbs(sess):
    success = False
    while not success:
        try:
            res = sess.get("http://tieba.baidu.com/dc/common/tbs", timeout=5)
            success = True
        except Exception:
            traceback.print_exc()
            pass
    tbs = res.json()["tbs"]
    return tbs


def getThreadList(sess, startPageNumber, endPageNumber):
    threadList = list()
    tidExp = re.compile(r"/([0-9]{1,})")
    pidExp = re.compile(r"pid=([0-9]{1,})")

    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in thread page", number)
        url = "http://tieba.baidu.com/i/i/my_tie?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="a", attrs={"class": "thread_title"})
        for element in elements:
            thread = element.get("href")
            threadDict = dict()
            threadDict["tid"] = tidExp.findall(thread)[0]
            threadDict["pid"] = pidExp.findall(thread)[0]
            threadExtraDict = dict()
            threadExtraDict["title"] = element.contents[0] if len(
                element.contents) > 0 else ""
            threadList.append((threadDict, threadExtraDict))
    return threadList


def getReplyList(sess, startPageNumber, endPageNumber):
    replyList = list()
    tidExp = re.compile(r"/([0-9]{1,})")
    pidExp = re.compile(r"pid=([0-9]{1,})")  # 主题贴和回复都为 pid
    cidExp = re.compile(r"cid=([0-9]{1,})")  # 楼中楼为 cid

    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in reply page", number)
        url = "http://tieba.baidu.com/i/i/my_reply?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(
            name="a", attrs={"class": "for_reply_context"})
        for element in elements:
            reply = element.get("href")
            if reply.find("pid") != -1:
                tid = tidExp.findall(reply)
                pid = pidExp.findall(reply)
                cid = cidExp.findall(reply)
                replyDict = dict()
                replyExtraDict = dict()
                replyExtraDict["content"] = element.contents[0] if len(
                    element.contents) > 0 else ""
                replyDict["tid"] = tid[0]

                if cid and cid[0] != "0":  # 如果 cid != 0, 这个回复是楼中楼, 否则是一整楼的回复
                    replyDict["pid"] = cid[0]
                else:
                    replyDict["pid"] = pid[0]
                replyList.append((replyDict, replyExtraDict))
    return replyList


def getFollowedBaList(sess, startPageNumber, endPageNumber):
    baList = list()
    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in followed Ba page", number)
        url = "http://tieba.baidu.com/f/like/mylike?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        forum_table = html.find(
            name="div", attrs={"class": "forum_table"}).contents[0].contents
        for element in forum_table:
            if element.contents[0].name != "td":
                continue
            baDict = dict()
            baExtraDict = dict()
            baExtraDict["title"] = element.contents[0].contents[0].get("title")
            unfollow_button = element.contents[3].contents[0]
            baDict["fid"] = unfollow_button.get("balvid")
            baDict["tbs"] = unfollow_button.get("tbs")
            baDict["fname"] = unfollow_button.get("balvname")
            baList.append((baDict, baExtraDict))
    return baList


def getConcerns(sess, startPageNumber, endPageNumber):
    concernList = list()
    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in concern page", number)
        url = "http://tieba.baidu.com/i/i/concern?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_unfollow"})
        for element in elements:
            concernDict = dict()
            concernExtraDict = dict()
            concernDict["cmd"] = "unfollow"
            concernDict["tbs"] = element.get("tbs")
            concernDict["id"] = element.get("portrait")
            concernExtraDict["name"] = element.get("name")
            concernExtraDict["name_show"] = element.get("name_show")
            concernList.append((concernDict, concernExtraDict))
    return concernList


def getFans(sess, startPageNumber, endPageNumber):
    fansList = list()
    tbsExp = re.compile(r"tbs : '([0-9a-zA-Z]{16})'")  # 居然还有一个短版 tbs.... 绝了

    for number in range(startPageNumber, endPageNumber + 1):
        print("Now in fans page", number)
        url = "http://tieba.baidu.com/i/i/fans?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        tbs = tbsExp.findall(res.text)[0]
        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_follow"})
        for element in elements:
            fanDict = dict()
            fanDict["cmd"] = "add_black_list"
            fanDict["tbs"] = tbs
            fanDict["portrait"] = element.get("portrait")
            fanExtraDict = dict()
            fanExtraDict["name"] = element.get("name")
            fansList.append((fanDict, fanExtraDict))
    return fansList


def matchFeatures(obj, features):
    for k, v in features.items():
        pattern = re.compile(v)
        if k in obj and pattern.match(obj[k]) is None:
            return False
    return True


# 建议使用keep功能时先使用DryRun或者DeferCommit模式查看将会被删除的元素
def buildKeepFunction(matchKey):
    def resultFunction(elementList, keepPattern=None):
        if keepPattern is None:
            # 不提供keep之时直接返回
            return elementList
        elif type(keepPattern) is list:
            # "keep": ["(pid等根据实际情况选择的key)"]
            # 此时将会匹配整个key，保留完全匹配key的元素
            # keep中的key应全为字符串，否则无法匹配

            # fast path
            if len(keepPattern) == 0:
                return elementList
            return [element for element in elementList if {**element[0], **element[1]}[matchKey] not in keepPattern]
        elif type(keepPattern) is dict:
            # "keep": { "(pid等根据实际情况选择的key)": "(正则表达式)" }
            # 此时将会匹配符合特征的元素，保留匹配的元素，特征中没有的key及原元素没有的key将会被忽略

            # fast path
            if len(keepPattern) == 0:
                return elementList
            return [element for element in elementList if not matchFeatures({**element[0], **element[1]}, keepPattern)]
        elif type(keepPattern) is str:
            # "keep": "(合法的python表达式，类型是函数)"
            # 此时将会将pattern作为python表达式解析，将结果作为函数调用，将元素作为参数传入，返回True时保留此元素
            # 使用此功能时请不要使用其他人提供的config.json

            # 此确认可能导致删除行为被挂起
            user_confirm = input("Use user-defined keep matcher '{}', continue?\n"
                                 "Please reject if you are not sure it's safe to run in current environment. y/n: "
                                 .format(keepPattern))
            if user_confirm != "y":
                print("No filtering is performed due to user operation, returning.")
                return elementList

            keepMatcher = eval(keepPattern)

            def matcher(element):
                try:
                    return keepMatcher(element)
                except Exception as e:
                    print("Error occured while evaluating user-defined keep matcher '{}' for element {}, "
                          "ignored and assumed not matched.".format(keepPattern, element))
                    print("Error is '{}'".format(e))
                    return False

            return [element for element in elementList if not matcher({**element[0], **element[1]})]
        else:
            # 其他不支持的情况
            raise RuntimeError(
                "Unsupported keep pattern: '{}'.".format(keepPattern))
    return resultFunction

# 在keep为列表时，分别对以下情况选择以下的key进行匹配


# 使用pid作为帖子及回复的key进行匹配
keepThread = buildKeepFunction("pid")

# 使用fid作为关注的吧的key进行匹配
keepBa = buildKeepFunction("fid")

# 使用id作为要取关的人的key进行匹配
keepConcerns = buildKeepFunction("id")

# 使用portrait作为要拉黑的粉丝的key进行匹配
keepFans = buildKeepFunction("portrait")


def deleteThread(sess, threadList):
    url = "https://tieba.baidu.com/f/commit/post/delete"
    count = 0
    dry_run = GetConfig("DryRun")
    need_confirm = GetConfig("NeedConfirm")
    defer_commit = GetConfig("DeferCommit")

    if defer_commit:
        defer_commit_list = list()
        for threadDict in threadList:
            if need_confirm:
                user_input = input("Delete {}? [y]/n: ".format(threadDict))
                if user_input == "n":
                    continue
            print("Adding {} to deferred deleting.".format(threadDict))
            defer_commit_list.append(threadDict)

        print("Threads will be deleted:")
        for threadDict in defer_commit_list:
            print("\t{}".format(threadDict))

        if dry_run:
            print("In dry run mode, dropped.")
            return 0

        while True:
            user_input = input("Proceed? y/n: ")
            if user_input == "n":
                print("Operation is cancelled by user, dropped.")
                return 0
            elif user_input == "y":
                break
            else:
                print("{} is not a valid answer.".format(user_input))

        for threadDict in defer_commit_list:
            print("Now deleting", threadDict)
            postData = dict()
            postData["tbs"] = getTbs(sess)
            postData.update(threadDict[0])
            res = sess.post(url, data=postData)

            print(res.text)

            if res.json()["err_code"] == 220034:  # 达到上限
                print("Limit exceeded, exiting.")
                return count
            else:
                count += 1
    else:
        for threadDict in threadList:
            if need_confirm:
                user_input = input("Delete {}? [y]/n: ".format(threadDict))
                if user_input == "n":
                    continue
            print("Now deleting", threadDict)
            if not dry_run:
                postData = dict()
                postData["tbs"] = getTbs(sess)
                postData.update(threadDict[0])
                res = sess.post(url, data=postData)

                print(res.text)

                if res.json()["err_code"] == 220034:  # 达到上限
                    print("Limit exceeded, exiting.")
                    return count
                else:
                    count += 1

    return count


def deleteFollowedBa(sess, baList):
    url = "https://tieba.baidu.com/f/like/commit/delete"
    dry_run = GetConfig("DryRun")
    need_confirm = GetConfig("NeedConfirm")
    defer_commit = GetConfig("DeferCommit")

    if defer_commit:
        defer_commit_list = list()
        for ba in baList:
            if need_confirm:
                user_input = input("Unfollow {}? [y]/n: ".format(ba))
                if user_input == "n":
                    continue
            print("Adding {} to deferred unfollowing.".format(ba))
            defer_commit_list.append(ba)

        print("Bas will be unfollowing:")
        for ba in defer_commit_list:
            print("\t{}".format(ba))

        if dry_run:
            print("In dry run mode, dropped.")
            return 0

        while True:
            user_input = input("Proceed? y/n: ")
            if user_input == "n":
                print("Operation is cancelled by user, dropped.")
                return 0
            elif user_input == "y":
                break
            else:
                print("{} is not a valid answer.".format(user_input))

        for ba in defer_commit_list:
            print("Now unfollowing", ba)
            res = sess.post(url, data=ba[0])
            print(res.text)
    else:
        for ba in baList:
            if need_confirm:
                user_input = input("Unfollow {}? [y]/n: ".format(ba))
                if user_input == "n":
                    continue
            print("Now unfollowing", ba)
            if not dry_run:
                res = sess.post(url, data=ba[0])
                print(res.text)


def deleteConcern(sess, concernList):
    url = "https://tieba.baidu.com/home/post/unfollow"
    dry_run = GetConfig("DryRun")
    need_confirm = GetConfig("NeedConfirm")
    defer_commit = GetConfig("DeferCommit")

    if defer_commit:
        defer_commit_list = list()
        for concern in concernList:
            if need_confirm:
                user_input = input("Unfollow {}? [y]/n: ".format(concern))
                if user_input == "n":
                    continue
            print("Adding {} to deferred unfollowing.".format(concern))

        print("Concerns will be unfollowed:")
        for concern in defer_commit_list:
            print("\t{}".format(concern))

        if dry_run:
            print("In dry run mode, dropped.")
            return 0

        while True:
            user_input = input("Proceed? y/n: ")
            if user_input == "n":
                print("Operation is cancelled by user, dropped.")
                return 0
            elif user_input == "y":
                break
            else:
                print("{} is not a valid answer.".format(user_input))

        for concern in defer_commit_list:
            print("Now unfollowing", concern)
            res = sess.post(url, data=concern[0])
            print(res.text)

    else:
        for concern in concernList:
            if need_confirm:
                user_input = input("Unfollow {}? [y]/n: ".format(concern))
                if user_input == "n":
                    continue
            print("Now unfollowing", concern)
            if not dry_run:
                res = sess.post(url, data=concern[0])
                print(res.text)


def deleteFans(sess, fansList):
    url = "https://tieba.baidu.com/i/commit"
    dry_run = GetConfig("DryRun")
    need_confirm = GetConfig("NeedConfirm")
    defer_commit = GetConfig("DeferCommit")

    if defer_commit:
        defer_commit_list = list()
        for fans in fansList:
            if need_confirm:
                user_input = input("Block {}? [y]/n: ".format(fans))
                if user_input == "n":
                    continue
            print("Adding {} to deferred blocking.".format(fans))
            defer_commit_list.append(fans)

        print("Fans will be blocked:")
        for fans in defer_commit_list:
            print("\t{}".format(fans))

        if dry_run:
            print("In dry run mode, dropped.")
            return 0

        while True:
            user_input = input("Proceed? y/n: ")
            if user_input == "n":
                print("Operation is cancelled by user, dropped.")
                return 0
            elif user_input == "y":
                break
            else:
                print("{} is not a valid answer.".format(user_input))

        for fans in defer_commit_list:
            print("Now blocking fans", fans)
            res = sess.post(url, data=fans[0])
            print(res.text)
    else:
        for fans in fansList:
            if need_confirm:
                user_input = input("Block {}? [y]/n: ".format(fans))
                if user_input == "n":
                    continue
            print("Now blocking fans", fans)
            if not dry_run:
                res = sess.post(url, data=fans[0])
                print(res.text)


def check(obj):
    if obj is None:
        exit(0)


def main():
    global GlobalConfig

    config = open("/".join([sys.path[0], "config.json"])
                  ).read().replace("\n", "")
    config = json.loads(config)
    GlobalConfig = config["config"] or DefaultConfig
    sess = requests.session()
    loadCookie(sess)

    if GetConfig("DryRun"):
        print("In dry run mode, nothing will be deleted, your data is safe.")
    else:
        print("Not in dry run mode, your operation will be committed and may be not recoverable.")

    if config["thread"]["enable"]:
        threadList = getThreadList(
            sess, config["thread"]["start"], config["thread"]["end"])
        check(threadList)
        print("Collected", len(threadList), "threads", end="\n\n")
        filteredThreadList = keepThread(
            threadList, config["thread"].get("keep", None))
        print(len(threadList) - len(filteredThreadList),
              "threads filtered.", end="\n\n")
        count = deleteThread(sess, filteredThreadList)
        print(count, "threads has been deleted", end="")
        if len(filteredThreadList) != count:
            print(", left", len(filteredThreadList) - count,
                  "threads due to limit exceeded or in dry run mode, or cancelled by user operation.", end="\n\n")
        else:
            print(".", end="\n\n")

    if config["reply"]["enable"]:
        replyList = getReplyList(
            sess, config["reply"]["start"], config["reply"]["end"])
        check(replyList)
        print("Collected", len(replyList), "replys", end="\n\n")
        filteredReplyList = keepThread(
            replyList, config["reply"].get("keep", None))
        print(len(replyList) - len(filteredReplyList),
              "replies filtered.", end="\n\n")
        count = deleteThread(sess, filteredReplyList)
        print(count, "replys has been deleted", end="")
        if len(filteredReplyList) != count:
            print(", left", len(filteredReplyList) - count,
                  "replys due to limit exceeded or in dry run mode, or cancelled by user operation.", end="\n\n")
        else:
            print(".", end="\n\n")

    if config["followedBa"]["enable"]:
        baList = getFollowedBaList(
            sess, config["followedBa"]["start"], config["followedBa"]["end"])
        check(baList)
        print("Collected", len(baList), "followed Ba", end="\n\n")
        filteredBaList = keepBa(baList, config["followedBa"].get("keep", None))
        print(len(baList) - len(filteredBaList), "bas filtered.", end="\n\n")
        deleteFollowedBa(sess, filteredBaList)
        print(len(filteredBaList), "followed Ba has been deleted.", end="\n\n")

    if config["concern"]["enable"]:
        concernList = getConcerns(
            sess, config["concern"]["start"], config["concern"]["end"])
        check(concernList)
        print("Collected", len(concernList), "concerns", end="\n\n")
        filteredConcernList = keepConcerns(
            concernList, config["concern"].get("keep", None))
        print(len(concernList) - len(filteredConcernList),
              "bas filtered.", end="\n\n")
        deleteConcern(sess, filteredConcernList)
        print(len(filteredConcernList), "concerns has been deleted.", end="\n\n")

    if config["fans"]["enable"]:
        fansList = getFans(sess, config["fans"]
                           ["start"], config["fans"]["end"])
        check(fansList)
        print("Collected", len(fansList), "fans", end="\n\n")
        filteredFansList = keepFans(fansList, config["fans"].get("keep", None))
        print(len(fansList) - len(filteredFansList),
              "bas filtered.", end="\n\n")
        deleteFans(sess, filteredFansList)
        print(len(filteredFansList), "fans has been deleted.", end="\n\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit by user request.")
