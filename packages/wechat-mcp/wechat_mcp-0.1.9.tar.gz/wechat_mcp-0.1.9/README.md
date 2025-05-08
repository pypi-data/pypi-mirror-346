# 方法1
```bash
git clone https://github.com/DarkNoah/wechat-mcp
uv sync
```
需要先登陆微信

# start sse
```bash
uvx wechat-mcp --wxid "your_wechat_id" --port 8000 --transport sse
```

# start stdio
```bash
uvx wechat-mcp --wxid "your_wechat_id" 
```


# tool list
- get_wechat_message
- get_last_wechat_message
- sql_wechat_message
- send_wechat_message
  
# client config
## sse
http://127.0.0.1:8000/sse


# 感谢以下开源项目的支持
- [wxauto](https://github.com/cluic/wxauto) 微信自动化
- [pywxdump](https://github.com/xaoyaoo/PyWxDump) wxdump