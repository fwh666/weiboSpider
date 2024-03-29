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
        print('初始化notion客户端...')

    """
    获取所有页面
    """

    def get_all_pages_and_duplicate(self):
        results = []
        start_cursor = None
        while True:
            response = global_notion.databases.query(
                database_id=global_database_id,
                start_cursor=start_cursor,
                page_size=100,  # Maximum page size
            )
            results.extend(response['results'])
            # temp 处理重复数据-根据唯一值的属性
            self.delete_duplicate_page(results, "消息ID")

            start_cursor = response.get('next_cursor')
            if not start_cursor:
                break
        return results

    """
    删除页面内容
    """

    def delete_page_content(self, page_id):
        try:
            del_block = global_notion.blocks.delete(block_id=page_id)
            print(f'删除成功:{page_id}')
        except Exception as e:
            print(f'删除失败:{page_id}')
            print(e)

    """
    删除重复的页面-保留最新的页面
    """

    def delete_duplicate_page(self, page_list, property_name):
        property_name_set = set()
        for page in page_list:
            if page["object"] == "page":
                for key, value in page["properties"].items():
                    if key == property_name:
                        # 获取富文本类型的值
                        text_value = value['rich_text'][0]['text']['content']
                        # text_value = value['url']
                        if text_value in property_name_set:
                            print(page["id"])
                            self.delete_page_content(page["id"])
                        else:
                            property_name_set.add(text_value)


"""
1. 清理冗余重复数据
"""


def main():
    client = notion_client()
    client.get_all_pages_and_duplicate()


if __name__ == '__main__':
    main()
    # client = notion_client()
    # client.get_all_pages_and_duplicate()
    print('清理完毕')
