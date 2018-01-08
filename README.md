# Delete-my-hisroy-in-tieba 
<h3>
运行在Python 3.6<br>
需要下载selenium的webdriver库 pip install selenium<br>
以及安装ChromeDriver后方可使用<br>
新加了个用Urllib删除回复的，速度比webdriver快← ←，可以稍微改改删其他的用<br><br>

安装ChromeDriver<br>
</h3>
<a href="https://sites.google.com/a/chromium.org/chromedriver/"/>下载ChromeDriver</a><br>
放在chrome的安装位置(默认在C:\Program Files (x86)\Google\Chrome\Application)<br>
最后将chrome的安装位置添加到系统环境变量的PATH当中即可<br><br>
<h3>
函数解释<br>
</h3>
login() 登陆 替换成自己的用户密码即可<br><br>
my_tie_collector() 获得自己发的帖子的链接<br><br>
my_reply_collector() 获得自己回复的链接<br><br>
deleter_tie() 删除帖子 注意需配合my_tie_collector()和my_reply_collector()使用<br>而且坑爹的百度每天只能删30条<br><br>
deleter_follows() 删除关注<br><br>
deleter_fan() 删除粉丝<br><br>
deleter_BaIFollow() 删除自己关注的吧<br><br>
根据自动的网络情况调整time.sleep()
