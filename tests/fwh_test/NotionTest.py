import json
import os
from notion_client import Client

class Page:
    def __init__(self, id, user_id, content, article_url, original_pictures, original, video_url,publish_time, publish_place, publish_tool, up_num, retweet_num, comment_num, nickname, weibo_num, following, followers):
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


def data_parse(file_path):
    # Load the JSON file
    with open(file_path,'r') as f:
        data = json.load(f)

    page_list=[]
    
    # Get the user's ID and nickname
    user_id = data['user']['id']
    nickname = data['user']['nickname']
    weibo_num = data['user']['weibo_num']
    following = data['user']['following']
    followers = data['user']['followers']

    # Get the weibo field attributes
    for weibo in data['weibo']:
        id = weibo['id']
        content = weibo['content']
        article_url = weibo['article_url']
        original_pictures = weibo['original_pictures']
        original = weibo['original']
        video_url = weibo['video_url']
        publish_time=weibo['publish_time']
        publish_place = weibo['publish_place']
        publish_tool = weibo['publish_tool']
        up_num = weibo['up_num']
        retweet_num = weibo['retweet_num']
        comment_num = weibo['comment_num']
        # Create an instance of the Page class
        page = Page(id, user_id, content, article_url, original_pictures, original, video_url,publish_time, publish_place, publish_tool, up_num, retweet_num, comment_num, nickname, weibo_num, following, followers)
        page_list.append(page)
    print(page_list)
    return page_list
    


    
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
        global_database_id = "bc6dd8a4495f483989fac402ec1486fa"
        global_notion = Client(auth=global_token)
        global_query_results = global_notion.databases.query(database_id=global_database_id)
        print('开始Notion自动化获取数据...')
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
                                'content': page.content
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
                    'url': 'https://m.weibo.cn/detail/'+str(page.id)
                },
                '超话社区': {
                    'select':{
                        'name': page.publish_tool
                    }
                },
                '是否原创': {
                    'select':{
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
                }
            }
        )
        print(new_page)
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
    to_remove = []  # 存储需要移除的 list2
    for item in page_list:
        if item.id in condition_id_set:
            to_remove.append(item)  # 将需要移除的元素存储到 list2 中
    for item in to_remove:
        page_list.remove(item)  # 移除 list1 中的 list2
    return page_list

def notion_main():
    user_id = 5648162302
    #  /Users/fwh/Downloads/黄建同学/5648162302.json   数据源
    file_path = f'/Users/fwh/Downloads/黄建同学/{user_id}.json'  # replace with your file's path
    page_list=data_parse(file_path)

    # 对比文件中的数据
    # output_file_path = f'/Users/fwh/A_FWH/GitHub/weiboSpider/tests/fwh_test/{user_id}-reuslt.json'  # replace with your desired output file path
    output_file_path = f'/Users/fwh/fuwenhao/Github/weiboSpider/tests/fwh_test/{user_id}-reuslt.json'  # replace with your desired output file path
    ids=get_ids_from_json(output_file_path)

    filter_result_list=remove_elements(page_list, ids)
    if len(filter_result_list) > 0:
        write_json_objects_to_file(filter_result_list, output_file_path)
        # Create a Notion page for each weibo
        client=notion_client()
        for page in page_list:
            client.create_page(page)
    else:
        print('没有数据可写入文件。')
    


"""
1. 加载爬取数据
2. 从数据库中获取已经存在的数据
3. 比较新增的数据，有就保存Notion，无就跳过
"""
if __name__ == '__main__':
    notion_main()
