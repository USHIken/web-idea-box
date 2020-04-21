import re
import requests
from bs4 import BeautifulSoup


# コンテンツのタイプ一覧
SCRATCH = "scratch"
UNITY = "unity"
WEB = "web"
ARTWORK3D = "artwork3d"
ARTWORK2D = "artwork2d"
OTHER = "other"

CONTENT_TYPES = (
    (SCRATCH, "Scratch"),
    (UNITY, "Unity"),
    (WEB, "Web"),
    (ARTWORK3D, "3D Artwork"),
    (ARTWORK2D, "2D Artwork"),
    (OTHER, "Other"),
)


class EmbedHTML(object):
    def __init__(self, content_type, project_url):
        self.type = content_type
        self.url = project_url
        self.ERRORS = {
            "invalid_url": "URLが間違っています。"
        }
        self.clean_url()

    def get(self):
        if not self.is_valid_url():
            return self.ERRORS["invalid_url"]
        if self.type == SCRATCH:
            return self.get_scratch_embed_html()
        elif self.type == UNITY:
            return self.get_unityroom_embed_html()
        elif self.type == ARTWORK3D:
            return self.get_sketchfab_embed_html()
        elif self.type == WEB:
            return self.get_web_embed_html()
        else:
            return ""

    def is_valid_url(self):
        if self.type == SCRATCH:
            url_regex = r"https://scratch\.mit\.edu/projects/\d{9}"
        elif self.type == UNITY:
            url_regex = r"https://unityroom\.com/games/.+"
        elif self.type == ARTWORK3D:
            url_regex = r"https://sketchfab\.com/3d-models/.+-[0-9a-f]{32}"
        elif self.type == WEB:
            url_regex = r"https?://[\w!?/\+\-_~=;\.,*&@#$%\(\)\'\[\]]+"
        # 正規表現にマッチすればTrue
        if re.fullmatch(url_regex, self.url):
            return True
        else:
            return False

    def clean_url(self):
        self.remove_query_string()
        self.remove_hash_string()
        self.remove_last_slash()

    def remove_query_string(self):
        splitted_url = self.url.split("?")
        if len(splitted_url) > 1:
            self.url = splitted_url[0]
        return self.url

    def remove_hash_string(self):
        splitted_url = self.url.split("#")
        if len(splitted_url) > 1:
            self.url = splitted_url[0]
        return self.url

    def remove_last_slash(self):
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        return self.url

    def get_bs4_html(self):
        # プロジェクトURLのHTML取得
        r = requests.get(self.url)
        html = BeautifulSoup(r.text)
        return html

    def get_scratch_embed_html(self):
        embed_html = f'<iframe src="{self.url}/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_unityroom_embed_html(self):
        # プロジェクトURLのHTML取得
        html = self.get_bs4_html()
        # aタグからWebGLのURLを取得
        a_tag = html.select_one("div.spec-games-center a[target='_blank']")
        webgl_url = a_tag.get("href")
        # 埋め込み用のHTMLを生成
        embed_html = f'<iframe src="{webgl_url}" width="560" height="358" scrolling="no" frameborder="0" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_sketchfab_embed_html(self):
        # プロジェクトURLのHTML取得
        html = self.get_bs4_html()
        # プロジェクト投稿ユーザーのSketchfabURL取得
        user_link = html.select_one("a.user-name__link").get("href")
        # プロジェクトURLの32文字のID取得
        project_id = re.search(r"[a-f0-9]{32}", self.url).group(0)

        # 埋め込み用iframeの生成
        iframe_src = f'https://sketchfab.com/models/{project_id}/embed?preload=1&amp;ui_controls=1&amp;ui_infos=1&amp;ui_inspector=1&amp;ui_stop=1&amp;ui_watermark=1&amp;ui_watermark_link=1'  # noqa: E501
        iframe = f'<iframe title="A 3D model" width="640" height="480" src="{iframe_src}" frameborder="0" allow="autoplay; fullscreen; vr" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>'  # noqa: E501

        # 埋め込み用プロジェクト概要HTMLの生成
        title_a = f'<a href="{self.url}?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">Sakana</a>'  # noqa: E501
        user_link_a = f'by <a href="{user_link}?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">Meimei</a>'  # noqa: E501
        content_desc_p = f'<p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;">{title_a}{user_link_a}</p>'  # noqa: E501

        # 埋め込み用SketchfabリンクHTMLの生成
        sketchfab_a = 'on <a href="https://sketchfab.com?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a>'  # noqa: E501

        # 埋め込み用HTMLの生成
        embed_html = f'<div class="sketchfab-embed-wrapper">{iframe}{content_desc_p}{sketchfab_a}</div>'  # noqa: E501
        return embed_html

    def get_web_embed_html(self):
        embed_html = f"<a src='self.url'>{self.url}</a>"
        return embed_html
