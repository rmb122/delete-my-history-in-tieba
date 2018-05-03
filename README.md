# Delete-my-hisroy-in-tieba 

## 使用之前

```sh  
pip install -r requirements.txt
```
注意还需要安装 ChromeDriver 才可以使用 TieBaDeleter.py  

运行在Python 3.6  
TieBaDeleter.py 可以删除关注、粉丝、帖子、回复  
Delete-reply.py 只能删除回复但是速度快  

## 安装ChromeDriver

[下载ChromeDriver][1]  
放在 Chrome 的安装位置 (默认在C:\Program Files (x86)\Google\Chrome\Application)  
最后将 Chrome 的安装位置添加到系统环境变量的 PATH 当中即可  

## TieBaDeleter.py

login() 登陆 替换成自己的用户密码即可  
my_tie_collector() 获得自己发的帖子的链接  
my_reply_collector() 获得自己回复的链接  
deleter_tie() 删除帖子 注意需配合 my_tie_collector() 和 my_reply_collector()  
deleter_follows() 删除关注  
deleter_fan() 删除粉丝  
deleter_BaIFollow() 删除自己关注的吧  
根据自动的网络情况调整 sleep() 里面的时间  

## Delete-reply.py

用 requests 重构的删除回复版本, 删的比 selenium 快很多  
需要在 cookie.json 中添加自己的 Cookie, JSON 格式  
我用的是 Chrome 的 [EditThisCookie][2] 插件, 可以直接导出 JSON 下的 Cookie  

帖子多的话可以放在 vps 上每天自动运行, 加入到计划任务中就可以啦  
PS: 记得根据自己的情况调整在文件中的搜索回复贴子的起始和结束页码 (百度有各种奇葩的 bug)  

[1]: https://sites.google.com/a/chromium.org/chromedriver/downloads
[2]: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
