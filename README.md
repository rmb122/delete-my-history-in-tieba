# Delete-my-hisroy-in-tieba
<h3>
需要下载selenium的webdriver库<br>
以及安装ChromeDriver后方可使用<br><br>


函数解释<br></h3>
login() 登陆 替换成自己的用户密码即可<br><br>
my_tie_collector() 获得自己发的帖子的链接<br><br>
my_reply_collector() 获得自己回复的链接<br><br>
deleter_tie() 删除帖子 注意需配合my_tie_collector()和my_reply_collector()使用<br>而且坑爹的百度每天只能删30条<br><br>
deleter_follows() 删除关注<br><br>
deleter_fan() 删除粉丝<br><br>
deleter_BaIFollows() 删除自己关注的吧<br><br>
