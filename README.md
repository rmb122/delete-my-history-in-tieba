# Delete-my-hisroy-in-tieba 

## 使用之前

```sh  
pip install -r requirements.txt
```

运行环境为 `Python 3.6`  
`DeleteMyHistory.py` 删除你的回复、主题帖、关注、粉丝、关注的吧  
`TieBaDeleter.py` 用 webdriver 模拟操作删除, 速度慢, 已经废弃, 请用 `DeleteMyHistory.py`  
如果你是个小白的话, 请参阅[傻瓜教程][3]  

PS: 不要在意项目名中的 `hisroy`, 手滑不小心打错了 (逃

## DeleteMyHistory.py

用 `requests` 重构的版本, 删的比 webdriver 快很多  
使用前需要在 `cookie.json` 中添加自己的 Cookie, JSON 格式  
我用的是 Chrome 的 [EditThisCookie][2] 插件, 可以直接导出 JSON 下的 Cookie  
可以在 `config.json` 中更改设置, 下面详细介绍  

## config.json

相当于设置, 不同项对应不同的行为, 其中  
`thread` 对应主题帖  
`reply` 对应回复  
`followedBa` 对应关注的吧  
`concern` 对应关注  
`fans` 对应粉丝  
  
例如将  
```json
"thread": {
        "enable": true,
        "start": 1,
        "end": 5
    },
```
改为  
```json
"thread": {
        "enable": false,
        "start": 2,
        "end": 6
    },
```
后, 将不会删除主题帖, 且删除范围将从在 [http://tieba.baidu.com/i/i/my_tie](http://tieba.baidu.com/i/i/my_tie) 的 `1-5` 页变为 `2-6` 页  
其他同理, 默认全部开启, 在删除完后可以自行调整关闭, 加快速度.  

帖子多的话可以放在 vps 上每天自动运行, 加入到计划任务中就可以啦  
PS: 记得根据自己的情况调整在文件中的搜索回复贴子的起始和结束页码 (百度有各种奇葩的 bug)  
PS2: 觉得好用的话点个 `Star` 吧 \_(:з」∠)\_  
PS3: 还有疑问, 或者遇到 `bug` 的话可以在 `issues` 里提出, 有空的话我会尽量解决的  

[1]: https://sites.google.com/a/chromium.org/chromedriver/downloads
[2]: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
[3]: https://github.com/rmb122/Delete-my-hisroy-in-tieba/blob/master/Guide.md
