# 傻瓜教程

首先下载安装 [python][1]  
![][2]  

注意安装时选择 `Add Python 3.6 to PATH`  
![][3]  

然后下载 [ChromeDriver][4], 注意如果是老版本 Chrome 的话需要下载对应的老版本 ChromeDriver  
![][5]
![][6]  
下载完成之后放在 chrome 安装目录下 (默认在`C:\Program Files (x86)\Google\Chrome\Application`)  
![][7]  

最后安装 [EditThisCookie][8]、下载 git 上的代码  
![][9]  

完成之后配置环境变量, 首先按 `WIN` + `pause/break` 键打开系统属性页面, 选择高级系统设置, 按照下图的顺序添加  
![][10]  
![][11]  
![][12]  
![][13]  
![最终效果][14]  

之后进入下载下来解压后的代码文件夹, 按照图示打开 `PowerShell`, 注意需要管理员权限  
![][15]  
  
输入以下指令 `pip install -r requirements.txt`  
![][16]  

安装完成之后登录进贴吧, 在[百度首页][17]上如图所示导出自己的 cookie  
![][18]  

打开 `cookie.json`, 将原来的内容全部删除后 `ctrl` +  `v`, 将自己的 cookie 复制上去保存  
最后打开 `TieBaDeleter.py`, 替换成自己的用户名和密码  
![][19]  

这个时候双击两个 `.py` 文件, 应该就可以运行了~

[1]: https://www.python.org/
[2]: http://i.imgur.com/o3wdzlk.png
[3]: http://i.imgur.com/P206SmS.png
[4]: https://sites.google.com/a/chromium.org/chromedriver/downloads
[5]: https://imgur.com/oxh32GN.png
[6]: https://imgur.com/NK8Zyt3.png
[7]: https://imgur.com/zFcZ5Nv.png
[8]: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
[9]: https://imgur.com/4qq0Cxo.png
[10]: https://imgur.com/7bD4h6F.png
[11]: https://imgur.com/JYutg5e.png
[12]: https://imgur.com/RPPFv0w.png
[13]: https://imgur.com/lEl33CI.png
[14]: https://imgur.com/v8v06k6.png
[15]: https://imgur.com/gucdJKA.png
[16]: https://imgur.com/bojLBlf.png
[17]: https://www.baidu.com
[18]: https://imgur.com/6vS5ihv.png
[19]: https://imgur.com/4vAXzOC.png