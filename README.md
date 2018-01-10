# Delete-my-hisroy-in-tieba 
<h3>
运行在Python 3.6<br>
需要下载selenium的webdriver库<br>
pip install selenium<br>
以及安装ChromeDriver后方可使用<br><br>

安装ChromeDriver<br>
</h3>
<a href="https://sites.google.com/a/chromium.org/chromedriver/"/>下载ChromeDriver</a><br>
放在chrome的安装位置(默认在C:\Program Files (x86)\Google\Chrome\Application)<br>
最后将chrome的安装位置添加到系统环境变量的PATH当中即可<br><br>

<h3>
Delete reply by urllib.py<br>
</h3>
用urllib重构的版本，删的更快些<br>
需要在相同目录下添加自己的cookie文件,JSON格式<br>
我用的是chrome的<a href="https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg">EditThisCookie</a>插件,可以直接导出JSON的Cookie<br>
帖子多的话可以改成pyw每次开机自动运行<br>
Delete reply by urllib_server.py即是这个的Linux服务器版，加入到计划任务中每日运行就可以啦<br><br>
<h3>
TieBaDeleter.py<br>
</h3>
login() 登陆 替换成自己的用户密码即可<br>
my_tie_collector() 获得自己发的帖子的链接<br>
my_reply_collector() 获得自己回复的链接<br>
deleter_tie() 删除帖子 注意需配合my_tie_collector()和my_reply_collector()使用<br>而且坑爹的百度每天只能删30条<br>
deleter_follows() 删除关注<br>
deleter_fan() 删除粉丝<br>
deleter_BaIFollow() 删除自己关注的吧<br>
根据自动的网络情况调整time.sleep()<br>

