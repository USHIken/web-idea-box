import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    def get_scratch_embed_html(self):
        embed_html = f'<iframe src="{self.url}/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_unityroom_embed_html(self):
        # プロジェクトURLのHTML取得
        r = requests.get(self.url)
        html = BeautifulSoup(r.text)
        # aタグからWebGLのURLを取得
        a_tag = html.select_one("div.spec-games-center a[target='_blank']")
        webgl_url = a_tag.get("href")
        # 埋め込み用のHTMLを生成
        embed_html = f'<iframe src="{webgl_url}" width="560" height="358" scrolling="no" frameborder="0" allowfullscreen></iframe>'  # noqa: E501
        return embed_html

    def get_sketchfab_embed_html(self):
        # seleniumドライバのセットアップ
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1080,1080')
        driver = webdriver.Chrome(chrome_options=options)
        # プロジェクトURLにアクセス
        driver.get(self.url)
        # EmbedHTMLを取得するためのボタンをクリック
        selector = "button[title='Embed']"
        embed_button = driver.find_elements_by_css_selector(selector)[0]
        embed_button.click()
        # EmbedHTMLを持つ要素が表示されるまで待つ
        class_name = "CodeMirror-code"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        # EmbedHTMLを取得
        embed_elm = driver.find_elements_by_class_name(class_name)[0]
        html_plain = embed_elm.get_attribute("innerHTML")
        html_bs4 = BeautifulSoup(html_plain).text
        embed_html = re.sub(" \xa0", "", html_bs4)
        return embed_html

    def get_web_embed_html(self):
        embed_html = f"<a src='self.url'>{self.url}</a>"
        return embed_html
