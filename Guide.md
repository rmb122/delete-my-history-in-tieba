# 傻瓜教程

首先下载安装 [python][1]  
(3.6.5 是版本号, 不一样没关系)  
![][2]  

注意安装时选择 `Add Python 3.6 to PATH`  (一定要勾选, 否则接下来无法运行)  
![][3]  

最后安装 [EditThisCookie][4]、下载 git 上的代码  
![][5]  

如果是 `Windows 10` 按照图示打开 `PowerShell`, 注意需要 `管理员` 权限  

![][6]  

如果是 Win7 的话, 如图搜索 `cmd` 右键以 `管理员` 权限打开  

![][7]  
  
在窗口中分别输入以下指令后回车 (等待一条完成之后再输下一条)  
```sh
pip install bs4
pip install requests
pip install lxml
```

![][8]  

安装完成之后登录进贴吧, 在[百度首页][9]上如图所示导出自己的 cookie  
![][10]  

将压缩包内文件解压到一个文件夹  
打开 `cookie.json`, 将原来的内容全部删除后 `ctrl` +  `v`, 将自己的 cookie 复制上去保存  
这个时候双击 `DeleteMyHistory.py`, 应该就可以运行了~  

默认情况下只删除主题帖和回复帖, 如果需要删除关注等, 请参考 `README.md` 里面的内容, 将对应的键值  
从 `false` 替换为 `true`.  

PS: 觉得好用的话点个 `Star` 吧 \_(:з」∠)\_  
PSS: 还有疑问或者遇到 `bug` 的话可以在 `issues` 里提出, 有空的话我会尽量解决的  

[1]: https://www.python.org/
[2]: https://i.loli.net/2019/04/27/5cc33976370ef.png
[3]: https://i.loli.net/2019/04/27/5cc3397638db7.png
[4]: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
[5]: https://i.loli.net/2019/04/27/5cc339761586c.png
[6]: https://i.loli.net/2019/04/27/5cc3397635602.png
[7]: https://i.loli.net/2019/04/27/5cc339761a427.png
[8]: https://i.loli.net/2019/04/27/5cc33975c0774.png
[9]: https://www.baidu.com
[10]: https://i.loli.net/2019/04/27/5cc3397613b89.png