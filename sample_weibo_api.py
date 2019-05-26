import weibo_api
import requests
from weibo_api.client import WeiboClient
import re
import json


MILLION = 1000000
DACAO = '1882760720'

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf8'
        return r.text
    except:
        return ""

def getUID(name):
    try:
        url = "https://s.weibo.com/user?q=%s&Refer=SUer_box" % name
        html = getHTMLText(url)

        plt = re.findall('class="s-btn-c" uid=([1-9][0-9]{9})', html)
        if len(plt) >= 1:
            return plt[0]
        return ""
    except:
        return ""



def update_popular_followees(uid, thres, save_json=False):
    client = WeiboClient()
    p = client.people(uid)

    followees = {}
    for follow in p.follows.all():
        try:
            if follow.followers_count > 1 * MILLION: # 粉丝数量
                followees[follow.id] = follow.name
                print(follow.name, follow.id)
        except:
            pass

    if save_json:
        try:
            with open('weibo/followees.json', 'w') as file:
                json.dump(followees, file)
        except:
            print('saving followees to json failed! ')

    return followees

if __name__ == '__main__':

    update_popular_followees(DACAO, 1, save_json=True)
    exit()


    with open('weibo/followees.json', 'r') as f:
        followees = json.load(f)

    client = WeiboClient()


    p = client.people('1882760720')  # my UID
    # print(type(p.name))
    # print(u"用户名：{}".format(p.name))
    # print(u"用户简介：{}".format(p.description))
    # print(u"他关注的用户数：{}".format(p.follow_count))
    # print(u"关注他的用户数：{}".format(p.followers_count))
    # print(u"他最近发布的微博：")
    # print("==================================================")
    # page(1) 表示获取第一页的内容，
    # 可以用all()方法获取所有内容(对于非必要情况，不要获取全部，因为对于有大量内容的用户，需要进行大量网络请求)
    # for status in p.statuses.page(1):
    #     print(u"微博动态：{}".format(status.id))
    #     print(u"发布时间：{}".format(status.created_at))
    #     print(u"微博内容概要：{}".format(status.text))
    #     print(u"转发数：{}".format(status.reposts_count))
    #     print(u"点赞数：{}".format(status.attitudes_count))
    #     print(u"评论数：{}".format(status.comments_count))
    #     print(u"发布于：{}".format(status.source))
    #     print("==================================================")

    # print('他的粉丝：')
    # print('#' * 50)
    # for follower in p.followers.page(1):
    #     print(follower.name)

    print('他关注的用户：')
    print('#' * 50)
    for follow in p.follows.all():
        try:
            if follow.followers_count > 1 * MILLION: # 粉丝数量
                print(follow.name, follow.id)
                for status in follow.statuses.page(1):
                    print(u"微博动态：{}".format(status.id))
                    print(u"发布时间：{}".format(status.created_at))
                    print(u"微博内容概要：{}".format(status.text))
                    print(u"转发数：{}".format(status.reposts_count))
                    print(u"点赞数：{}".format(status.attitudes_count))
                    print(u"评论数：{}".format(status.comments_count))
                    print(u"发布于：{}".format(status.source))
                    print("==================================================")
                    break
        except:
            pass

    # print('他的文章：')
    # print('#' * 50)
    # for article in p.articles.page(1):
    #     print(article.text)