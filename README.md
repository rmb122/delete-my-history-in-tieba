# Delete-my-hisroy-in-tieba 

## 使用之前
运行在Python 3.6  
Delete reply by urllib.py可以直接使用  
TieBaDeleter.py需要下载selenium的webdriver库  
```sh  
pip install selenium  
```
以及安装ChromeDriver后方可使用   

## 安装ChromeDriver
[下载ChromeDriver](1)  
放在Chrome的安装位置(默认在C:\Program Files (x86)\Google\Chrome\Application)  
最后将Chrome的安装位置添加到系统环境变量的PATH当中即可  

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
用urllib重构的删除回复版本, 删的比selenium更快些  
需要在相同目录下添加自己的Cookie文件, JSON格式  
我用的是Chrome的[EditThisCookie](2)插件, 可以直接导出JSON的Cookie  
帖子多的话可以改成pyw每次开机自动运行  
Delete reply by urllib_server.py即是这个的Linux服务器版, 加入到计划任务中每日运行就可以啦  

[1]:https://sites.google.com/a/chromium.org/chromedriver/
[2]:https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg