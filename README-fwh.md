## 自定义逻辑功能
1. 先获取数据，然后写入Notion中
2. 多个用户ID的时候, 查询完一个用户ID后就触发保存Notion数据

### Notion-util写入逻辑
1. 获取网络数据源
2. 本地存储一份json数据源
3. 对比数据源中的id数据(唯一值),确认是否有新的数据,再存储Notion中

## 常用运行命令：

- 首次终端运行,需要pip安装
```bash
$ python3 -m pip install weibo-spider
```

- 优先配置config.json文件

- 默认选择config.json文件 输出指定文件夹
```bash
cd /Users/fwh/A_FWH/GitHub/weiboSpider
$ python3 -m weibo_spider --output_dir="/Users/fwh/Downloads/"
```

## 帮助文档
- 设置配置文件
    - https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md
- 获取cookie信息
    - https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md
