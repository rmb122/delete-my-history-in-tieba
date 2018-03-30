# Delete-my-hisroy-in-tieba 

## 使用之前

运行在Python 3.6  
Delete reply by urllib.py 换成自己的 cookie 后可以直接使用  
TieBaDeleter.py 需要下载 selenium 的 webdriver 库  

```sh  
pip install selenium  
```

以及安装 ChromeDriver 后方可使用   

## 安装ChromeDriver

[下载ChromeDriver](1)  
放在 Chrome 的安装位置 (默认在C:\Program Files (x86)\Google\Chrome\Application)  
最后将 Chrome 的安装位置添加到系统环境变量的 PATH 当中即可  

## TieBaDeleter.py

login() 登陆 替换成自己的用户密码即可   
my_tie_collector() 获得自己发的帖子的链接  
my_reply_collector() 获得自己回复的链接  
deleter_tie() 删除帖子 注意需配合my_tie_collector()和my_reply_collector()    
使用而且坑爹的百度每天只能删30条  
deleter_follows() 删除关注  
deleter_fan() 删除粉丝  
deleter_BaIFollow() 删除自己关注的吧  
根据自动的网络情况调整sleep()里面的时间  

## Delete reply by urllib.py

用 urllib 重构的删除回复版本, 删的比 selenium 快而且能在命令行运行  
需要在相同目录下添加自己的 Cookie 文件, JSON 格式  
我用的是 Chrome 的 [EditThisCookie](2) 插件, 可以直接导出 JSON 下的 Cookie  

帖子多的话可以放在 vps 上每天自动运行    
Delete reply by urllib_server.py 即是这个的服务器版, 加入到计划任务中每日运行就可以啦  
PS: 记得根据自己的情况调整在文件中的搜索回复贴子的起始和结束页码  

[1]:https://sites.google.com/a/chromium.org/chromedriver/
[2]:https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg