旧版
#!/usr/bin/python3
import os
import json
import time
	@@ -22,14 +23,27 @@ def checkError(reqJson):
    return reqJson


class ToodoWechat:
    def __init__(self, appID, appSecret):
        self.appID = appID
        self.appSecret = appSecret
        self.basePath = os.path.dirname(__file__)
        self._session = requests.Session()
        # 确保多个公众号的缓存不会混乱
        self.tokenCache = md5(f"{self.appID}{self.appSecret}".encode()).hexdigest() + '.json'

    def _requests(self, method, url, decode_level=2, retry=10, timeout=15, **kwargs):
        if method in ["get", "post"]:
	@@ -48,7 +62,7 @@ def getNewToken(self):
        文件缓存token格式：{"access_token":"ACCESS_TOKEN","expires_in":7200,"expires_at": int}
        :return: access_token
        """
        baseUrl = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appID}&secret={self.appSecret}"
        res = checkError(self._requests('get', baseUrl))
        res['expires_at'] = int(time.time()) + res['expires_in']
        with open(os.path.join(self.basePath, self.tokenCache), 'w') as f:
	@@ -125,30 +139,61 @@ def uploadMedia(self, mediaType, mediaPath, **kwargs):
            res = checkError(self._requests('post', baseUrl, files={"media": mediaFile}))
        return res


if __name__ == '__main__':
    # 实例化应用
    a = ToodoWechat('appID', 'appSecret')
    # 上传图文中的图片，返回图片src地址，可直接在图文中使用
    picUrl = a.uploadNewsPicture('test.png')
    # 上传图片素材
    media_id1 = a.uploadMedia('image', 'test.png').get('media_id')
    # 上传视频素材
    media_id2 = a.uploadMedia('video', 'test.mp4', title="这个是视频的标题", introduction="测试视频").get('media_id')
    # 图文列表，可以在articles里面放置多个图文数据(最多8个)，其中content字段为正文，支持HTML语法
    data = {
        "articles": [{
            "title": f"图文标题",
            "thumb_media_id": "封面的media_id",
            "author": '图文作者',
            "digest": f"图文简介",
            "show_cover_pic": 1,
            "content": "图文正文(支持HTML语法)",
            "content_source_url": '阅读原文的链接地址',
            "need_open_comment": 1,
            "only_fans_can_comment": 1
        }
        ]
    }
    # 上传图文
    a.uploadNews(data)
