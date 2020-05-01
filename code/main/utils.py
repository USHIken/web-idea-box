import re
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.template.loader import render_to_string
from django.utils.html import escape, smart_urlquote


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

# 埋め込みタイプのコンテンツタイプ
EMBED_TYPES = [SCRATCH, UNITY, WEB, ARTWORK3D]

# requestsのアクセスが許可されたオリジン
ALLOWED_ORIGIN = {
    SCRATCH: "https://scratch.mit.edu",
    UNITY: "https://unityroom.com",
    ARTWORK3D: "https://sketchfab.com",
}


def clean_content_url(url, content_type):
    """
    埋め込みタイプのコンテンツのURLをcleanする
        - remove_query_string:  `?`以降のクエリストリングを削除
        - remove_hash_string:   `#`以降のハッシュストリングを削除
        - remove_last_slash:    URLの最後の`/`を削除
    """

    def remove_query_string(url):
        splitted_url = url.split("?")
        if len(splitted_url) > 1:
            url = splitted_url[0]
        return url

    def remove_hash_string(url):
        splitted_url = url.split("#")
        if len(splitted_url) > 1:
            url = splitted_url[0]
        return url

    def remove_last_slash(url):
        if url[-1] == "/":
            url = url[:-1]
        return url

    if not url:
        return url
    # URLエンコーディング
    url = smart_urlquote(url)
    # 埋め込みタイプなら、不要な文字列を削除(WEBの場合は不要)
    if content_type in EMBED_TYPES and content_type != WEB:
        url = remove_query_string(url)
        url = remove_hash_string(url)
        url = remove_last_slash(url)

    return url


def get_origin_from(url):
    """
    URLからオリジンを取得する
    例:
    >>> url = "https://scratch.mit.edu/projects/38717893/;param?q=q#fragment"
    >>> get_origin_from(url)
    https://scratch.mit.edu
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    return f'{scheme}://{netloc}'


class ContentURLValidator(URLValidator):
    schemes = ['http', 'https']

    def __call__(self, value, content_type):
        if value is None:
            value = ""
        # content_typeごとにvalidationを行う
        self.validate_embed_type_url(value, content_type)

    def validate_embed_type_url(self, url, content_type):
        if content_type == SCRATCH:
            url_regex = r"https://scratch\.mit\.edu/projects/\d{9}/?"
            message = "ScratchのプロジェクトURLを入力してください。"
            example = "例: https://scratch.mit.edu/projects/111222333"
        elif content_type == UNITY:
            url_regex = r"https://unityroom\.com/games/.+"
            message = "UnityroomのプロジェクトURLを入力してください。"
            example = "例: https://unityroom.com/game/game_name"
        elif content_type == ARTWORK3D:
            url_regex = r"https://sketchfab\.com/3d-models/.+-[0-9a-f]{32}"
            message = "SketchfabのプロジェクトURLを入力してください。"
            example = "例: https://sketchfab.com/3d-models/project_name"
        else:
            url_regex = r".*"
            message = "httpあるいはhttpsからはじまる有効なURLを入力してください。"
            example = ""

        self.message = message + example

        # URLValidator(親クラス)のvalidationを行う
        super().__call__(url)

        # 正規表現にマッチしなければ
        if not re.fullmatch(url_regex, url):
            raise ValidationError(self.message, code=self.code)


class EmbedHTML(object):

    def __init__(self, content_type, project_url):
        self.type = content_type
        # HTMLのhref用
        self.encoded_url = smart_urlquote(project_url)
        # HTMLのinnerText用
        self.safe_url = escape(unquote(project_url))

    def __call__(self):
        if self.type not in EMBED_TYPES:
            # 埋め込みタイプでなければ、埋め込みHTMLは空にする
            return ""
        if self.type == SCRATCH:
            return self.get_scratch_embed_html()
        elif self.type == UNITY:
            return self.get_unityroom_embed_html()
        elif self.type == ARTWORK3D:
            return self.get_sketchfab_embed_html()
        elif self.type == WEB:
            return self.get_web_embed_html()

    @property
    def origin(self):
        return get_origin_from(self.encoded_url)

    def get_bs4_html(self):
        """
        指定したURLにアクセスしHTMLを取得
        """
        # SSRF対策: ALLOWED_ORIGIN以外にサーバーをアクセスさせないようチェック
        import requests
        if not self.origin == ALLOWED_ORIGIN[self.type]:
            raise ValidationError("投稿が許可されているサイトのURLを入力してください。")
        # プロジェクトURLのHTML取得
        r = requests.get(self.encoded_url)
        html = BeautifulSoup(r.text)
        return html

    def get_scratch_embed_html(self):
        embed_html = f'<iframe src="{self.encoded_url}/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_unityroom_embed_html(self):
        # プロジェクトURLのHTML取得
        html = self.get_bs4_html()
        # aタグからWebGLのURLを取得
        a_tag = html.select_one("div.spec-games-center a[target='_blank']")
        safe_webgl_url = smart_urlquote(a_tag.get("href"))
        # 埋め込み用のHTMLを生成
        embed_html = f'<iframe src="{safe_webgl_url}" width="560" height="358" scrolling="no" frameborder="0" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_sketchfab_embed_html(self):
        # プロジェクトURLのHTML取得
        html = self.get_bs4_html()
        # プロジェクト投稿ユーザーのSketchfabURL取得
        safe_user_link = smart_urlquote(
            html.select_one("a.user-name__link").get("href"))
        # プロジェクトURLの32文字のID取得
        project_id = re.search(r"[a-f0-9]{32}", self.encoded_url).group(0)

        iframe_html = 'main/sketchfab_iframe.html'
        context = {
            "project_id": project_id,
            "encoded_url": self.encoded_url,
            "user_link": safe_user_link}
        embed_html = render_to_string(iframe_html, context)
        return embed_html

    def get_web_embed_html(self):
        embed_html = f"<a href='{self.encoded_url}'>{self.safe_url}</a>"
        return embed_html


def get_client_ip(request):
    """requestからIPアドレスを取得"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
