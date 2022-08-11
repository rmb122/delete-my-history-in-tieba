import abc
import copy
import logging
import re
import sys
import traceback
import typing

import bs4
import requests
import toml

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def load_cookie(session: requests.Session, raw_cookie: str) -> requests.Session:
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    for cookie in raw_cookie.split(';'):
        cookie = cookie.strip()

        if '=' in cookie:
            name, value = cookie.split('=', 1)
            session.cookies[name] = value
    return session


def validate_cookie(session: requests.Session):
    resp = session.get('https://tieba.baidu.com/i/i/my_tie', allow_redirects=False)
    return resp.status_code == 200


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Module:
    _name: str
    _session: requests.Session

    def __init__(self, session: requests.Session):
        self._session = session

    @property
    def name(self):
        return self._name

    @property
    def session(self):
        return self._session

    def _get_tbs(self):
        success = False
        resp = None

        while not success:
            try:
                resp = self._session.get("https://tieba.baidu.com/dc/common/tbs", timeout=5)
                success = True
            except Exception:
                traceback.print_exc()
                pass

        tbs = resp.json()["tbs"]
        return tbs

    def run(self):
        def remove_tbs(temp_entity: typing.Dict[str, str]) -> typing.Dict[str, str]:
            # tbs 是随机生成的, 需要去掉之后再去重
            temp_entity = copy.deepcopy(temp_entity)
            if 'tbs' in temp_entity:
                del temp_entity['tbs']
            return temp_entity

        current_page = 1
        deleted_entity = set()

        logger.info(f'current in module [{self._name}]')
        while True:
            current_page_entity = self._collect(current_page)

            if len(current_page_entity) == 0:
                # 全部删除干净了
                logger.info(f'all entity in module [{self._name}] are all deleted')
                return

            if len(set([HashableDict(remove_tbs(i)) for i in current_page_entity]).difference(deleted_entity)) == 0:
                # 当前页面全部都是已经删除过的, 跳到下一页, (百度的神奇 BUG, 只有帖子/回复会出现这种情况)
                current_page += 1
                logger.info(f'no more new entity in page [{current_page - 1}], switch to page [{current_page}]')
                continue

            for entity in current_page_entity:
                no_tbs_entity = HashableDict(remove_tbs(entity))

                if no_tbs_entity not in deleted_entity:
                    deleted_entity.add(no_tbs_entity)

                    logger.info(f"now deleting [{entity}], in page [{current_page}]")
                    resp, stop = self._delete(entity)
                    logger.info(f'delete response [{resp.text}]')

                    if stop:
                        logger.info(f"limit exceeded in [{self._name}], exiting")
                        return

    @abc.abstractmethod
    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        raise NotImplementedError("")

    @abc.abstractmethod
    def _delete(self, entity: typing.Any) -> typing.Tuple[requests.Response, bool]:
        raise NotImplementedError("")


class ThreadModule(Module):
    def __init__(self, session: requests.Session):
        super().__init__(session)
        self._name = 'thread'

    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        tid_exp = re.compile(r"/([0-9]+)")
        pid_exp = re.compile(r"pid=([0-9]+)")

        resp = self._session.get("https://tieba.baidu.com/i/i/my_tie", params={'pn': page})

        html = bs4.BeautifulSoup(resp.text, "lxml")
        elements = html.find_all(name="a", attrs={"class": "thread_title"})

        current_page_thread = []
        for element in elements:
            thread = element.get("href")
            thread_dict = dict()
            thread_dict["tid"] = tid_exp.findall(thread)[0]
            thread_dict["pid"] = pid_exp.findall(thread)[0]
            current_page_thread.append(thread_dict)
        return current_page_thread

    def _delete(self, entity: typing.Dict[str, str]) -> typing.Tuple[requests.Response, bool]:
        url = "https://tieba.baidu.com/f/commit/post/delete"

        post_data = copy.deepcopy(entity)
        post_data["tbs"] = self._get_tbs()
        resp = self._session.post(url, data=post_data)

        return resp, resp.json()["err_code"] == 220034


class ReplyModule(Module):
    def __init__(self, session: requests.Session):
        super().__init__(session)
        self._name = 'reply'

    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        tid_exp = re.compile(r"/([0-9]+)")
        pid_exp = re.compile(r"pid=([0-9]+)")  # 主题贴和回复都为 pid
        cid_exp = re.compile(r"cid=([0-9]+)")  # 楼中楼为 cid

        resp = self._session.get("https://tieba.baidu.com/i/i/my_reply", params={'pn': page})

        html = bs4.BeautifulSoup(resp.text, "lxml")
        elements = html.find_all(name="a", attrs={"class": "b_reply"})
        current_page_reply = []

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
                current_page_reply.append(reply_dict)
        return current_page_reply

    def _delete(self, entity: typing.Dict[str, str]) -> typing.Tuple[requests.Response, bool]:
        url = "https://tieba.baidu.com/f/commit/post/delete"

        post_data = copy.deepcopy(entity)
        post_data["tbs"] = self._get_tbs()
        resp = self._session.post(url, data=post_data)
        return resp, resp.json()["err_code"] == 220034


class FollowedBaModule(Module):
    def __init__(self, session: requests.Session):
        super().__init__(session)
        self._name = 'followed_ba'

    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        ba_list = []
        resp = self._session.get("https://tieba.baidu.com/f/like/mylike", params={'pn': page})

        html = bs4.BeautifulSoup(resp.text, "lxml")
        elements = html.find_all(name="span")
        for element in elements:
            ba_dict = dict()
            ba_dict["fid"] = element.get("balvid")
            ba_dict["tbs"] = element.get("tbs")
            ba_dict["fname"] = element.get("balvname")
            ba_list.append(ba_dict)
        return ba_list

    def _delete(self, entity: typing.Dict[str, str]) -> typing.Tuple[requests.Response, bool]:
        url = "https://tieba.baidu.com/f/like/commit/delete"
        resp = self._session.post(url, data=entity)
        return resp, False


class ConcernModule(Module):
    def __init__(self, session: requests.Session):
        super().__init__(session)
        self._name = 'concern'

    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        concern_list = []

        resp = self._session.get("https://tieba.baidu.com/i/i/concern", params={'pn': page})

        html = bs4.BeautifulSoup(resp.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_unfollow"})
        for element in elements:
            concern_dict = dict()
            concern_dict["cmd"] = "unfollow"
            concern_dict["tbs"] = element.get("tbs")
            concern_dict["id"] = element.get("portrait")
            concern_list.append(concern_dict)
        return concern_list

    def _delete(self, entity: typing.Dict[str, str]) -> typing.Tuple[requests.Response, bool]:
        url = "https://tieba.baidu.com/home/post/unfollow"
        resp = self._session.post(url, data=entity)
        return resp, False


class FanModule(Module):
    def __init__(self, session: requests.Session):
        super().__init__(session)
        self._name = 'fan'

    def _collect(self, page: int) -> typing.List[typing.Dict[str, str]]:
        fan_list = []
        tbs_exp = re.compile(r"tbs : '([0-9a-zA-Z]{16})'")  # 居然还有一个短版 tbs.... 绝了

        resp = self._session.get("https://tieba.baidu.com/i/i/fans", params={'pn': page})

        tbs = tbs_exp.findall(resp.text)[0]
        html = bs4.BeautifulSoup(resp.text, "lxml")
        elements = html.find_all(name="input", attrs={"class": "btn_follow"})
        for element in elements:
            fan_dict = dict()
            fan_dict["cmd"] = "add_black_list"
            fan_dict["tbs"] = tbs
            fan_dict["portrait"] = element.get("portrait")
            fan_list.append(fan_dict)
        return fan_list

    def _delete(self, entity: typing.Dict[str, str]) -> typing.Tuple[requests.Response, bool]:
        url = "https://tieba.baidu.com/i/commit"
        resp = self._session.post(url, data=entity)
        return resp, False


def main():
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    with open('cookie.txt', 'r') as f:
        raw_cookie = f.read()

    session = requests.session()
    session = load_cookie(session, raw_cookie)

    if not validate_cookie(session):
        logger.fatal('cookie expired, please update it')
        sys.exit(-1)

    module_constructors: typing.List[typing.Callable[[requests.Session], Module]] = [
        ThreadModule, ReplyModule, FollowedBaModule, ConcernModule, FanModule
    ]

    for module_constructor in module_constructors:
        module = module_constructor(session)

        if module.name in config:
            module_config = config[module.name]
            if module_config['enable']:
                module.run()


if __name__ == "__main__":
    main()
