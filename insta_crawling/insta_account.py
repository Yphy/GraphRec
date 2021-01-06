import time
import json
import datetime
import pymysql
import traceback
from os.path import join as pjoin
import requests
from utils.account_crawling import account_crawling
from utils.misc import get_logger

def get_account_with_selenium():
    file_names = ["brand.txt", "ex_brand.txt"]
    for file_name in file_names:
        accounts = []
        with open(pjoin("resources", file_name), 'r', encoding='UTF-8')  as fin:
            accounts = [str(account).strip() for account in fin.readlines()]
        accounts = list(set(accounts))
        accounts.sort()
        account_crawling(accounts)

def parse_post(p):
    caption_nodes = p.get("edge_media_to_caption", {}).get("edges", [])
    comment = caption_nodes[0]["node"]["text"] if caption_nodes else ""
    tags = [c[1:] for c in comment.split() if c.startswith("#")] if comment else []
    ut = int(p["taken_at_timestamp"])
    created_time = datetime.datetime.utcfromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")
    return (
        p["shortcode"], #shortcode
        created_time, #date_post
        p["thumbnail_src"], # image
        comment, #text
        str(tags), #tags
        p["edge_media_preview_like"]["count"], #like_num
        p["edge_media_to_comment"]["count"], #comment_num
    )

class InstaAccount:

    def __init__(self):
        self.logger = get_logger()
        self.base_url = "https://instagram.com/"

    def load(self, file_name):
        accounts = []
        with open(pjoin("resources", file_name), 'r', encoding='UTF-8')  as fin:
            accounts = [str(account).strip() for account in fin.readlines()]
        accounts = list(set(accounts))
        accounts.sort()
        self.logger.info("Accounts len {} from {}".format(len(accounts), file_name))
        return accounts

    def _parse_user_meta(self, info):
        graphql = info.get("graphql", {})
        user = graphql.get("user", {})
        return dict(
            id = user.get("id"),
            name = user.get("username"),
            followed_by = user.get("edge_followed_by", {})["count"],
            follow = user.get("edge_follow", {})["count"],
            is_private = user.get("is_private", True),
            edges = user.get("edge_owner_to_timeline_media", {}),
        )

    def _parse_post(self, info):
        start_time = time.time()
        page_info = info.get("page_info", {})
        has_next_page = page_info.get("has_next_page")
        end_cursor = page_info.get("end_cursor")
        edges = info.get("edges", [])
        posts = []
        for edge in edges:
            try:
                posts.append(parse_post(edge["node"]))
            except:
                self.logger.info(traceback.format_exc())

        last_time = time.time()
        if last_time - start_time < 2.0:
            time.sleep(2.0 - (last_time - start_time))
        return has_next_page, end_cursor, posts

    def crawl_account(self, account):
        account_url = self.base_url + account
        r = requests.get(account_url, params={"__a": 1})
        time.sleep(1)
        meta_info = r.json()
        meta_info = self._parse_user_meta(meta_info)
        if meta_info.get("is_private"):
            # log private
            return []
        edges = meta_info.get("edges")
        has_next_page, end_cursor, total_posts = self._parse_post(edges)
        while has_next_page:
            params = {
                "query_hash": "472f257a40c653c64c666ce877d59d2b",
                "variables": json.dumps({
                    "id": meta_info["id"],
                    "first": 50,
                    "after": end_cursor,
                }),
            }
            r = requests.get(self.base_url + "graphql/query/", params=params)
            time.sleep(1)
            info = r.json().get("data", {}).get("user", {}).get("edge_owner_to_timeline_media", {})
            if not info:
                break
            has_next_page, end_cursor, posts = self._parse_post(info)
            total_posts.extend(posts)

        return {"id": meta_info["id"], "name": meta_info["name"]}, total_posts

    def remove_multiple_row(self, posts):
        new_posts, shortcodes = list(), set()
        for post in posts:
            if post[0] not in shortcodes:
                new_posts.append(post)
                shortcodes.add(post[0])
        return new_posts

    def save(self, account, posts):
        posts = self.remove_multiple_row(posts)
        self.logger.info("account {} get {} posts".format(account["name"], len(posts)))
        conn = pymysql.connect(host='localhost',
                           user='remote',
                           password='!@#qweasdzxc',
                           db='prj_wearly', charset='utf8mb4')
        cursor = conn.cursor()
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        query = """INSERT INTO
            prj_wearly.post_by_account(post_id, user_num, account_name,
                date_post, date_crawl, image, text, hashtags, like_num, comment_num)
            VALUES (%s, {}, '{}', %s, '{}', %s, %s, %s, %s, %s)
            """.format(account.get("id"), account.get("name"), now)
        cursor.executemany(query, posts)
        conn.commit()
        cursor.close()
        conn.close()
        self.logger.info("account {} is inserted to db".format(account["name"]))

    def save_image():

        conn = pymysql.connect(host='localhost',
                           user='root',
                           password='!Wearly123'
                           db='instagram_crawling', charset='utf8')
        cursor = conn.cursor()
        query = """INSERT INTO
            prj_wearly.image_total(id, image_name, dataset_name, id_from_dataset,
                category, x_1, y_1, x_2, y_2, is_fashion_image, is_train_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(query, data)
        conn.commit()
        cursor.close()
        conn.close()

    def run(self):
        file_names = ["brand.txt", "ex_brand.txt"]
        for file_name in file_names:
            accounts = self.load(file_name)
            for account in accounts:
                try:
                    account_info, posts = self.crawl_account(account)
                    self.save(account_info, posts)
                except KeyboardInterrupt:
                    raise Exception("stop")
                except:
                    self.logger.info(traceback.format_exc())


if __name__ == "__main__":
    while True:
        get_account_with_selenium()
        time.sleep(10.0)
        ins = InstaAccount()
        ins.run()
        time.sleep(10.0)
