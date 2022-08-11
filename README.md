# delete-my-history-in-tieba

## 使用之前

### Windows 操作系统

如果使用 Windows 系统, 可以直接参考[教程][1]  

### 其他操作系统

```sh
git clone https://github.com/rmb122/delete-my-history-in-tieba.git
cd delete-my-history-in-tieba
pip install -r requirements.txt
```

运行环境为 `Python >= 3`  
使用前需要在 `cookie.txt` 中添加自己的 Cookie, 直接复制 Chrome 开发者工具下网络页面中对 `tieba.baidu.com` 请求的 Cookie 进去即可, 如果还不了解是什么意思的话, 请参考[教程][1]  
之后运行 `DeleteMyHistory.py` 就可以删除回复、主题帖、关注、粉丝、关注的吧  
更多选项可以在 `config.toml` 中更改设置, 下面详细介绍  

## config.toml

相当于设置, 不同项对应不同的行为, 其中  
`thread` 对应主题帖  
`reply` 对应回复  
`followed_ba` 对应关注的吧  
`concern` 对应关注  
`fans` 对应粉丝
  
例如将  
```toml
[thread]
enable = true
```
改为  
```toml
[thread]
enable = false
```
后, 将不会删除主题帖  
默认开启对主题贴和回复的删除  

## FAQ

1. Q: 出现 `OSError: [Errno 0] Error` 等连接错误  
A: 请确保代理/翻墙软件的全局模式处于关闭状态

2. Q: 运行之后帖子没有删除, 仍然存在  
A: 贴吧删除功能存在 bug, 存在帖子删除后在 `我的帖子` 中仍然存在的可能. 但实际上这些帖子已经删除, 点开查看可以确认已经删掉了

3. Q: 帖子没有删除干净, 或者出现 `limit exceeded`  
A: 百度贴吧每天最多只允许删除 30 条帖子 (实际上存在各种 bug, 导致实际删除数量大于 30), 可以等明天继续运行

## 最后

觉得好用的话可以点个 `Star` 鼓励作者, 如果还有疑问, 或者遇到 `bug` 的话可以在 `issues` 里提出

[1]: https://github.com/rmb122/Delete-my-hisroy-in-tieba/blob/master/Guide.md
