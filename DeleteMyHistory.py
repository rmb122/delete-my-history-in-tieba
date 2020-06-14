# -*- coding: utf-8 -*-

import json
import re
import sys
import traceback

import bs4
import requests


def load_cookie(sess):
    cookies = open("/".join([sys.path[0], "cookie.json"])).read().replace("\n", "")
    cookies = json.loads(cookies)
    sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    for cookie in cookies:
        sess.cookies[cookie["name"]] = cookie["value"]


def get_tbs(sess):
    success = False
    res = None

    while not success:
        try:
            res = sess.get("http://tieba.baidu.com/dc/common/tbs", timeout=5)
            success = True
        except Exception:
            traceback.print_exc()
            pass

    tbs = res.json()["tbs"]
    return tbs


def get_thread_list(sess, start_page_number, end_page_number):
    thread_list = list()
    tid_exp = re.compile(r"/([0-9]+)")
    pid_exp = re.compile(r"pid=([0-9]+)")

    for number in range(start_page_number, end_page_number + 1):
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
            thread_dict = dict()
            thread_dict["tid"] = tid_exp.findall(thread)[0]
            thread_dict["pid"] = pid_exp.findall(thread)[0]
            thread_list.append(thread_dict)
    return thread_list


def get_reply_list(sess, start_page_number, end_page_number):
    reply_list = list()
    tid_exp = re.compile(r"/([0-9]+)")
    pid_exp = re.compile(r"pid=([0-9]+)")  # 主题贴和回复都为 pid
    cid_exp = re.compile(r"cid=([0-9]+)")  # 楼中楼为 cid

    for number in range(start_page_number, end_page_number + 1):
        print("Now in reply page", number)
        url = "http://tieba.baidu.com/i/i/my_reply?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="a", attrs={"class": "b_reply"})
        for element in elements:
            reply = element.get("href")
            if reply.find("pid") != -1:
                tid = tid_exp.findall(reply)
                pid = pid_exp.findall(reply)
                cid = cid_exp.findall(reply)
                reply_dict = dict()
                reply_dict["tid"] = tid[0]

                if cid and cid[0] != "0":  # 如果 cid != 0, 这个回复是楼中楼, 否则是一整楼的回复
                    reply_dict["pid"] = cid[0]
                else:
                    reply_dict["pid"] = pid[0]
                reply_list.append(reply_dict)
    return reply_list


def get_followed_ba_list(sess, start_page_number, end_page_number):
    ba_list = list()
    for number in range(start_page_number, end_page_number + 1):
        print("Now in followed Ba page", number)
        url = "http://tieba.baidu.com/f/like/mylike?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expired, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="span")
        for element in elements:
            ba_dict = dict()
            ba_dict["fid"] = element.get("balvid")
            ba_dict["tbs"] = element.get("tbs")
            ba_dict["fname"] = element.get("balvname")
            ba_list.append(ba_dict)
    return ba_list


def get_concerns(sess, start_page_number, end_page_number):
    concern_list = list()
    for number in range(start_page_number, end_page_number + 1):
        print("Now in concern page", number)
        url = "http://tieba.baidu.com/i/i/concern?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expried, Please update it")
            return

        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_unfollow"})
        for element in elements:
            concern_dict = dict()
            concern_dict["cmd"] = "unfollow"
            concern_dict["tbs"] = element.get("tbs")
            concern_dict["id"] = element.get("portrait")
            concern_list.append(concern_dict)
    return concern_list


def get_fans(sess, start_page_number, end_page_number):
    fans_list = list()
    tbs_exp = re.compile(r"tbs : '([0-9a-zA-Z]{16})'")  # 居然还有一个短版 tbs.... 绝了

    for number in range(start_page_number, end_page_number + 1):
        print("Now in fans page", number)
        url = "http://tieba.baidu.com/i/i/fans?pn=" + str(number)
        res = sess.get(url)

        if res.url == "http://static.tieba.baidu.com/tb/error.html?ErrType=1":
            print("Cookie has been expired, Please update it")
            return

        tbs = tbs_exp.findall(res.text)[0]
        html = bs4.BeautifulSoup(res.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_follow"})
        for element in elements:
            fan_dict = dict()
            fan_dict["cmd"] = "add_black_list"
            fan_dict["tbs"] = tbs
            fan_dict["portrait"] = element.get("portrait")
            fans_list.append(fan_dict)
    return fans_list


def delete_thread(sess, thread_list):
    url = "https://tieba.baidu.com/f/commit/post/delete"
    count = 0

    for thread_dict in thread_list:
        print("Now deleting", thread_dict)
        post_data = dict()
        post_data["tbs"] = get_tbs(sess)
        for idName in thread_dict:
            post_data[idName] = thread_dict[idName]
        res = sess.post(url, data=post_data)

        print(res.text)

        if res.json()["err_code"] == 220034:  # 达到上限
            print("Limit exceeded, exiting.")
            return count
        else:
            count += 1

    return count


def delete_followed_ba(sess, ba_list):
    url = "https://tieba.baidu.com/f/like/commit/delete"

    for ba in ba_list:
        print("Now unfollowing", ba)
        res = sess.post(url, data=ba)
        print(res.text)


def delete_concern(sess, concern_list):
    url = "https://tieba.baidu.com/home/post/unfollow"

    for concern in concern_list:
        print("Now unfollowing", concern)
        res = sess.post(url, data=concern)
        print(res.text)


def delete_fans(sess, fans_list):
    url = "https://tieba.baidu.com/i/commit"

    for fans in fans_list:
        print("Now blocking fans", fans)
        res = sess.post(url, data=fans)
        print(res.text)


def check(obj):
    if obj is None:
        exit(0)


def main():
    config = open("/".join([sys.path[0], "config.json"])).read().replace("\n", "")
    config = json.loads(config)
    sess = requests.session()
    load_cookie(sess)

    if config["thread"]["enable"]:
        thread_list = get_thread_list(sess, config["thread"]["start"], config["thread"]["end"])
        check(thread_list)
        print("Collected", len(thread_list), "threads", end="\n\n")
        count = delete_thread(sess, thread_list)
        print(count, "threads has been deleted", end="")
        if len(thread_list) != count:
            print(", left", len(thread_list) - count, "threads due to limit exceeded.", end="\n\n")
        else:
            print(".", end="\n\n")

    if config["reply"]["enable"]:
        reply_list = get_reply_list(sess, config["reply"]["start"], config["reply"]["end"])
        check(reply_list)
        print("Collected", len(reply_list), "replies", end="\n\n")
        count = delete_thread(sess, reply_list)
        print(count, "replies has been deleted", end="")
        if len(reply_list) != count:
            print(", left", len(reply_list) - count, "replies due to limit exceeded.", end="\n\n")
        else:
            print(".", end="\n\n")

    if config["followed_ba"]["enable"]:
        ba_list = get_followed_ba_list(sess, config["followed_ba"]["start"], config["followed_ba"]["end"])
        check(ba_list)
        print("Collected", len(ba_list), "followed Ba", end="\n\n")
        delete_followed_ba(sess, ba_list)
        print(len(ba_list), "followed Ba has been deleted.", end="\n\n")

    if config["concern"]["enable"]:
        concern_list = get_concerns(sess, config["concern"]["start"], config["concern"]["end"])
        check(concern_list)
        print("Collected", len(concern_list), "concerns", end="\n\n")
        delete_concern(sess, concern_list)
        print(len(concern_list), "concerns has been deleted.", end="\n\n")

    if config["fans"]["enable"]:
        fans_list = get_fans(sess, config["fans"]["start"], config["fans"]["end"])
        check(fans_list)
        print("Collected", len(fans_list), "fans", end="\n\n")
        delete_fans(sess, fans_list)
        print(len(fans_list), "fans has been deleted.", end="\n\n")


if __name__ == "__main__":
    main()
