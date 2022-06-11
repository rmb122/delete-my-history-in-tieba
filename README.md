# Delete-my-hisroy-in-tieba 

## 使用之前

```sh  
pip install -r requirements.txt
```

运行环境为 `Python >= 3`  
`DeleteMyHistory.py` 删除你的回复、主题帖、关注、粉丝、关注的吧  
如果你是个小白的话, 请参阅[傻瓜教程][1]  

PS: 不要在意项目名中的 `hisroy`, 手滑不小心打错了 (逃

## DeleteMyHistory.py

使用前需要在 `cookie.txt` 中添加自己的 Cookie  
直接复制 Chrome 开发者工具下网络页面中对 `tieba.baidu.com` 请求的 Cookie 进去即可  
可以在 `config.toml` 中更改设置, 下面详细介绍  

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
```json
[thread]
enable = false
```
后, 将不会删除主题帖  
默认开启对主题贴和回复的删除  

帖子多的话可以放在 vps 上每天自动运行, 加入到计划任务中就可以啦  

觉得好用的话点个 `Star` 吧 \_(:з」∠)\_, 如果还有疑问, 或者遇到 `bug` 的话可以在 `issues` 里提出, 有空的话我会尽量解决的  

[1]: https://github.com/rmb122/Delete-my-hisroy-in-tieba/blob/master/Guide.md
