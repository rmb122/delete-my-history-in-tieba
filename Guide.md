# 傻瓜教程

1. 首先下载[安装包][1], 解压到桌面  
![](https://s2.loli.net/2022/06/11/rDXR9SOigWLYotd.png)

2. 用 Chrome 打开 https://tieba.baidu.com/index.html 并确保已经登录贴吧, 如果刚登录的话多刷新几次

3. 在页面空白处右键, 点击检查, 打开开发者工具  
![](https://s2.loli.net/2022/06/11/Blew1ks2hd84FIu.png)

4. 选中网络选项卡  
![](https://s2.loli.net/2022/06/11/zK38beVXlgjvnDH.png)

5. 确保保留日志是**没有**勾选的状态, 然后刷新页面, 将选项卡拉到最上面, 点击 `index.html`. 在右侧子页面向下滑动, 找到请求标头的 `Cookie`  
![](https://s2.loli.net/2024/03/16/x84zdilB5hnWPXv.png)

6. 把 Cookie 右侧的值全部拖动选中, 右键点击复制
![](https://s2.loli.net/2024/03/16/8KEjq4OeWHdsITA.png)

7. 把刚刚复制的 Cookie 粘贴到到刚刚下载的空白文件 cookie.txt 里面 (注意 Cookie 值可以等效你的账号密码，因此不要把复制结果泄漏到互联网上)  
![](https://s2.loli.net/2022/06/11/WaGfiVcnIU7ZgRX.png)

8. 双击`DeleteMyHistory.exe` 即开始运行  
![](https://s2.loli.net/2022/08/11/PRi5WMqVkw9FvmY.png)

如果出现问题, 例如闪退, 首先请参考 README 中的 [FAQ][2], 如果仍然存在错误, 可以按照如下操作提出 issue  
1. 在文件夹空白处 `Shift+右键`, 点击此处打开 Powershell 窗口  
![](https://s2.loli.net/2022/06/11/I5e4QfZqSpVG6al.png)
2. 输入 `.\DeleteMyHistory.exe`, 将输出结果复制到 issue 处提交  
![](https://s2.loli.net/2022/06/11/Yz46ucXUxLFV8Wk.png)

[1]: https://github.com/rmb122/delete-my-history-in-tieba/releases/download/v1.1.1/delete-my-history-in-tieba-v1.1.1.zip
[2]: https://github.com/rmb122/delete-my-history-in-tieba#FAQ
