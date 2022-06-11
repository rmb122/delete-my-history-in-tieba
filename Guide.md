# 傻瓜教程

1. 首先下载[安装包][1], 解压到桌面
![](https://s2.loli.net/2022/06/11/rDXR9SOigWLYotd.png)
2. 用 Chrome 打开 https://tieba.baidu.com/index.html, 在页面空白处右键, 点击检查, 打开开发者工具
![2022-06-11_20-10.png](https://s2.loli.net/2022/06/11/Blew1ks2hd84FIu.png)
3. 选中网络选项卡
![2022-06-11_20-10_1.png](https://s2.loli.net/2022/06/11/zK38beVXlgjvnDH.png)
4. 确保保留日志是**没有**勾选的状态, 然后刷新页面, 将选项卡拉到最上面, 点击 `index.html`. 
在请求标头的 `Cookie` 的值上右键, 点击复制值
![2022-06-11_20-15.png](https://s2.loli.net/2022/06/11/XGmK7BLeY6jfcZF.png)
5. 把结果复制到刚刚下载的 cookie.txt 里面 (注意不要把复制结果泄漏到互联网上)
![2022-06-11_20-16.png](https://s2.loli.net/2022/06/11/WaGfiVcnIU7ZgRX.png)
6. 在文件夹空白处 `Shift+右键`, 点击此处打开 Powershell 窗口
![2022-06-11_20-16_1.png](https://s2.loli.net/2022/06/11/I5e4QfZqSpVG6al.png)
7. 输入 `.\DeleteMyHistory.exe` 即开始运行
![2022-06-11_20-17.png](https://s2.loli.net/2022/06/11/Yz46ucXUxLFV8Wk.png)

[1]: https://github.com/rmb122/Delete-my-hisroy-in-tieba/suites/6890631552/artifacts/267076890