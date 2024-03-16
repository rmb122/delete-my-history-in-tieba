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

此文件相当于设置, 不同项对应不同的行为, 其中 `user_agent`, `cookie_file` 正常情况下不需要修改, 而剩下的每一项对应一个模块的配置  
`thread` 对应主题帖  
`reply` 对应回复  
`followed_ba` 对应关注的吧  
`concern` 对应关注  
`fans` 对应粉丝

以 `thread` 为例子  
```toml
[thread]
enable = true
start_page = 1
```

`enable` 字段代表是否启动这个模块, `true` = 启动, `false` = 不启动, 默认开启对主题贴和回复的删除  
而 `start_page` 代表开始删除帖子的页数, 可以解决部分贴吧的 bug, 可以参考 [#31][2] 和下面的 FAQ

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

## FAQ

Q: 出现 `OSError: [Errno 0] Error` 等连接错误.  
A: 请确保代理/翻墙软件的全局模式处于关闭状态.

Q: 运行之后帖子没有删除, 仍然存在.  
A: 贴吧删除功能存在 bug, 存在帖子删除后在 `我的帖子` 中仍然存在的可能. 但实际上这些帖子已经删除, 点开查看可以确认已经删掉了.

Q: 只删除了最新的一个回复.  
A: 仍然为贴吧的 bug, 原因为部分页面为空, 导致程序误以为已经将回复清空 ([#31][2]). 可以通过修改对应模块的 `start_page` 字段来解决, 例如将 `start_page` 修改为 2, 将直接跳过空白的第 1 页, 直接从第 2 页开始收集回复并删除.

Q: 帖子没有删除干净, 或者出现 `limit exceeded`.  
A: 百度贴吧每天最多只允许删除 30 条帖子 (实际上存在各种 bug, 导致实际删除数量大于 30), 可以等明天继续运行.

Q: 出现 `UnicodeDecodeError: 'gbk'...` 解码错误  
A: 参考 [#37][3], 去掉 cookie.txt 中的乱码内容即可.

## 最后

觉得好用的话可以点个 `Star` 鼓励作者, 如果还有疑问, 或者遇到 `bug` 的话可以在 `issues` 里提出

[1]: https://github.com/rmb122/Delete-my-hisroy-in-tieba/blob/master/Guide.md
[2]: https://github.com/rmb122/delete-my-history-in-tieba/issues/31
[3]: https://github.com/rmb122/delete-my-history-in-tieba/issues/37
