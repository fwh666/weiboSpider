import json
import os
import logging
import requests
from lxml import etree
import random
from time import sleep

logger = logging.getLogger('spider.notion_util')


class Page:
    def __init__(self, id, user_id, content, article_url, original_pictures, original, video_url, publish_time,
                 publish_place, publish_tool, up_num, retweet_num, comment_num, nickname, weibo_num, following,
                 followers):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.article_url = article_url
        self.original_pictures = original_pictures
        self.original = original
        self.video_url = video_url
        self.publish_time = publish_time
        self.publish_place = publish_place
        self.publish_tool = publish_tool
        self.up_num = up_num
        self.retweet_num = retweet_num
        self.comment_num = comment_num
        self.nickname = nickname
        self.weibo_num = weibo_num
        self.following = following
        self.followers = followers


def data_parse(file_path, exist_ids):
    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    page_list = []

    # Get the user's ID and nickname
    user_id = data['user']['id']
    nickname = data['user']['nickname']
    weibo_num = data['user']['weibo_num']
    following = data['user']['following']
    followers = data['user']['followers']

    # Get the weibo field attributes
    for weibo in data['weibo']:
        id = weibo['id']
        if id in exist_ids:
            continue
        content = weibo['content']
        if u'全文' in content:
            cookie = global_cookie
            content = get_long_content(cookie, id, content)
            if len(content) < 10:
                content = weibo['content']

        article_url = weibo['article_url']
        original_pictures = weibo['original_pictures']
        original = weibo['original']
        video_url = weibo['video_url']
        publish_time = weibo['publish_time']
        publish_place = weibo['publish_place']
        publish_tool = weibo['publish_tool']
        up_num = weibo['up_num']
        retweet_num = weibo['retweet_num']
        comment_num = weibo['comment_num']
        # Create an instance of the Page class
        page = Page(id, user_id, content, article_url, original_pictures, original, video_url, publish_time,
                    publish_place, publish_tool, up_num, retweet_num, comment_num, nickname, weibo_num, following,
                    followers)
        page_list.append(page)
    print(page_list)
    return page_list


def get_long_content(cookie, weibo_id, content):
    try:
        url = f'https://weibo.cn/comment/{weibo_id}'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        headers = {'User_Agent': user_agent, 'Cookie': cookie}
        resp = requests.get(url, headers=headers)
        selector = etree.HTML(resp.content)
        if selector is not None:
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = handle_garbled(info)
            wb_time = info.xpath("//span[@class='ct']/text()")[0]
            weibo_content = wb_content[wb_content.find(':') +
                                       1:wb_content.rfind(wb_time)]
            sleep(random.randint(6, 10))
            if weibo_content is not None:
                return weibo_content
            else:
                return content
    except Exception as e:
        print('获取正文异常', e)
        return content


import sys


def handle_garbled(info):
    """处理乱码"""
    try:
        info = (info.xpath('string(.)').replace(u'\u200b', '').encode(
            sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        return info
    except Exception as e:
        logger.exception(e)
        return u'无'


from notion_client import Client


class notion_client:
    def __init__(self):
        """
        初始化
        """
        global global_query_results
        global global_notion
        global global_database_id
        global_token = "secret_SGSgYlUHk8knQRLcwJr1alzjzVTwXFwrr0UDBawy0Sw"
        global_database_id = "bc6dd8a4495f483989fac402ec1486fa"  # 微博-data
        global_notion = Client(auth=global_token)
        global_query_results = global_notion.databases.query(database_id=global_database_id)
        print('初始化Notion...')

    """
    创建新的页面
    1. 属性名字和字段个数要对应上
    2. 不同的属性用不同的构参方式
    """

    def create_page(self, page):
        new_page = global_notion.pages.create(
            parent={
                'database_id': global_database_id
            },
            properties={
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': 'title'
                            }
                        }
                    ]
                },
                '正文内容': {
                    'rich_text': [
                        {
                            'text': {
                                'content': page.content if len(page.content) <= 2000 else '正文'
                            }
                        }
                    ]
                },
                "点赞数": {
                    "number": page.up_num
                },
                "评论数": {
                    "number": page.comment_num
                },
                "转发数": {
                    "number": page.retweet_num
                },
                '发布人': {
                    'rich_text': [
                        {
                            'text': {
                                'content': page.nickname
                            }
                        }
                    ]
                },
                "发布人ID": {
                    "number": int(page.user_id)
                },
                "关注数": {
                    "number": page.following
                },
                "粉丝数": {
                    "number": page.followers
                },
                "微博数": {
                    "number": page.weibo_num
                },
                "发布时间": {
                    "date": {
                        "start": page.publish_time
                    }
                },
                "正文地址URL": {
                    'url': 'https://m.weibo.cn/detail/' + str(page.id)
                },
                '超话社区': {
                    'select': {
                        'name': page.publish_tool
                    }
                },
                '是否原创': {
                    'select': {
                        'name': str(page.original)
                    }
                },
                '消息ID': {
                    'rich_text': [
                        {
                            'text': {
                                'content': page.id
                            }
                        }
                    ]
                },
                '正文图片': {
                    'rich_text': [
                        {
                            'text': {
                                'content': page.original_pictures
                            }
                        }
                    ]
                },
                '正文视频': {
                    'rich_text': [
                        {
                            'text': {
                                'content': page.video_url
                            }
                        }
                    ]
                },
                "Tags": {
                    "multi_select": [
                        {
                            "name": '初始化'
                        }
                    ]
                },
            },
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": page.content
                                }
                            }
                        ]
                    }
                }
            ]
        )
        return new_page


def write_json_objects_to_file(objects, filename):
    if len(objects) == 0:
        print('没有数据可写入文件。')
        return
    # with open(filename, 'w') as file:
    with open(filename, 'a') as file:
        for obj in objects:
            page_dict = {
                'id': obj.id,
                'user_id': obj.user_id,
                'content': obj.content,
                'article_url': obj.article_url,
                'original_pictures': obj.original_pictures,
                'original': obj.original,
                'video_url': obj.video_url,
                'publish_time': obj.publish_time,
                'publish_place': obj.publish_place,
                'publish_tool': obj.publish_tool,
                'up_num': obj.up_num,
                'retweet_num': obj.retweet_num,
                'comment_num': obj.comment_num,
                'nickname': obj.nickname,
                'weibo_num': obj.weibo_num,
                'following': obj.following,
                'followers': obj.followers
            }
            # Write the JSON object to filefile)
            json.dump(page_dict, file)
            file.write('\n')  # 添加分隔符，例如换行符
    print('JSON文件保存成功。')


def load_json_objects_from_file(filename):
    objects = []
    with open(filename, 'r') as file:
        for line in file:
            obj = json.loads(line)
            objects.append(obj)
    return objects


def get_ids_from_json(file_path):
    ids = set()
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            for line in json_file:
                obj = json.loads(line)
                if 'id' in obj:
                    ids.add(obj['id'])
    return ids


def remove_elements(page_list, condition_id_set):
    if len(condition_id_set) == 0:
        return page_list
    to_remove = []  # 存储需要移除的 list2
    for item in page_list:
        if item.id in condition_id_set:
            to_remove.append(item)  # 将需要移除的元素存储到 list2 中
    for item in to_remove:
        page_list.remove(item)  # 移除 list1 中的 list2
    return page_list


# def notion_main(user_id, source_file_path):
#     logger.info(f'{user_id} 开始Notion自动化处理数据...{source_file_path}')
#     # user_id = 5648162302
#     #  /Users/fwh/Downloads/黄建同学/5648162302.json   数据源
#     # source_file_path = f'/Users/fwh/Downloads/黄建同学/{user_id}.json'  # replace with your file's path
#     page_list = data_parse(source_file_path)
#
#     # 对比文件中的数据
#     # output_file_path = f'/Users/fwh/A_FWH/GitHub/weiboSpider/tests/fwh_test/{user_id}-reuslt.json'  # replace with your desired output file path
#     # output_file_path = f'/Users/fwh/fuwenhao/Github/weiboSpider/tests/fwh_data/{user_id}-reuslt.json'  # replace with your desired output file path
#     output_file_path = f'/home/fwh/github/weiboSpider/tests/fwh_data/{user_id}-reuslt.json'  # replace with your desired output file path
#     if os.path.exists(output_file_path):
#         ids = get_ids_from_json(output_file_path)
#     else:
#         ids = set()
#
#     filter_result_list = remove_elements(page_list, ids)
#     if len(filter_result_list) > 0:
#         write_json_objects_to_file(filter_result_list, output_file_path)
#         # Create a Notion page for each weibo
#         client = notion_client()
#         for page in page_list:
#             client.create_page(page)
#     else:
#         logger.info(f'{user_id} 没有数据可写入文件。')
#         # print('没有数据可写入文件。')


def get_message_ids(result_path):
    set_message_ids = set()
    # 判断文件是否存在
    # result_path = os.path.join(os.path.dirname(__file__), "data", f'twitter-noiton.json')
    if not os.path.exists(result_path):
        print(f'[文件不存在:{result_path}')
        return set_message_ids
    # 读取json文件
    try:
        with open(result_path, 'r') as file:
            for line in file:
                if len(line) > 0:
                    obj = json.loads(line)
                    set_message_ids.add(obj['id'])
    except Exception as e:
        logger.error("NotionClient get_message_ids Error", e)
    print(f'[已记录nodeId数量:{len(set_message_ids)}]')
    return set_message_ids


def get_json_file(folder_path):
    import os
    # 指定文件夹路径
    # folder_path = '/path/to/your/folder'
    # 存储所有JSON文件的路径
    json_files = []
    # 使用os.walk()遍历文件夹中的所有子文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    # 打印所有JSON文件的路径
    # for json_file in json_files:
    #     print(json_file)
    return json_files


'''
1. 获取已经保存notionID数据
2. for循环处理新存储的数据文件
3. 只保存没有的数据到Notion
4. 核心校验数据值为消息ID
'''


def main():
    client = notion_client()
    insert_notion_list = []
    notion_file_path = f'/Users/fwh/fuwenhao/Github/weiboSpider/weibo/weibo-notion.json'
    exist_ids = get_message_ids(notion_file_path)
    data_file_path = '/Users/fwh/fuwenhao/Github/weiboSpider/weibo/'
    # 加载所有json文件
    json_files = get_json_file(data_file_path)
    for json_file in json_files:
        if json_file.endswith('weibo-notion.json'):
            continue
        page_list = data_parse(json_file, exist_ids)
        for page in page_list:
            id = page.id
            if id not in exist_ids:
                if len(page.content) > 2000:
                    print(f'[消息ID:{id}内容过长，跳过]')
                    continue
                new_page = client.create_page(page)
                page_id = new_page['id']
                print(f'保存消息ID为:{id}')
                insert_notion_data = {'id': id, 'page_id': page_id}
                insert_notion_list.append(insert_notion_data)

    with open(notion_file_path, 'a') as f:
        for i in insert_notion_list:
            json.dump(i, f)
            f.write('\n')
        f.close()
        print(f'[notion.json保存:{len(insert_notion_list)}条数据完成]')


"""
1. 加载爬取数据
2. 从数据库中获取已经存在的数据
3. 比较新增的数据，有就保存Notion，无就跳过
"""
from notion_clean_weibo import main as clean_main

global global_cookie
if __name__ == '__main__':
    global_cookie = 'SCF=AmdJA8eVf6WN0I0DpGYvCRJhTxQLYMoMaSoqxI5y_dhdYNYnsv521TbCSGVklmKQfBHpBzBDxo9WAqPUso_FtrA.; SUB=_2A25LAQg7DeRhGeRP7FUQ9ifKyjyIHXVofwXzrDV6PUJbktCOLXH1kW1NUBLdA4EpiFs7REXSLbH3KVC5E3THMYqW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF052.szp5Ep4SBfMjNg4y55JpX5KMhUgL.FozpS0MpSo.ceK52dJLoIpnLxKqL1KqL1hMLxKqLBo-LBKLSqPicIgRt; ALF=1714226539; _T_WM=94535001455; WEIBOCN_FROM=1110106030; MLOGIN=1; XSRF-TOKEN=688eac; mweibo_short_token=e831d00f2f; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26fid%3D1005052217035934%26uicode%3D10000011'
    if len(global_cookie) < 10:
        exit()
    main()
    clean_main()
