import os
import uuid

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from users.models import User
from main import utils
from main.utils import EmbedHTML

from markdownx.models import MarkdownxField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(TimeStampedModel):

    # 画像ファイルの保存場所
    def get_image_path(self, filename):
        name = str(uuid.uuid4())
        extension = os.path.splitext(filename)[-1]
        return 'images/' + name + extension

    # 製作者
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contents")
    # タイトル
    title = models.CharField('作品タイトル', max_length=64)
    # 説明
    description = MarkdownxField('説明文', blank=True, null=True)
    # コンテンツのタイプ
    content_type = models.CharField(
        'コンテンツの種類',
        choices=utils.CONTENT_TYPES, default=utils.SCRATCH, max_length=32)
    # 一覧で表示される画像
    thumbnail = models.ImageField('トップ画像', upload_to=get_image_path)
    # プロジェクトの各種サイトURL
    url = models.URLField('作品の掲載元のURL', blank=True, null=True, default="")
    # 埋め込み用HTML: receiverによる自動入力
    embed_html = models.TextField(blank=True, null=False)

    def __str__(self):
        return f'{self.content_type}: {self.title}'

    @property
    def is_embed_type(self):
        """コンテンツ埋め込みタイプであるかどうか"""
        return self.content_type in utils.EMBED_TYPES

    def is_created_by(self, user):
        """コンテンツ投稿者であるかどうか"""
        return self.creator == user

    # 訪問履歴取得関数群
    def get_visits_other_than_creator(self):
        """コンテンツ投稿者以外の訪問履歴を取得"""
        return self.visits.filter(~Q(visitor=self.creator))

    def get_visits_only_logged_in_user(self):
        """ログインユーザーのみの訪問履歴を取得"""
        return self.visits.filter(~Q(visitor=None))


class ContentVisit(TimeStampedModel):
    """作品への訪問"""
    # 訪問された作品
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="visits")
    # 訪問したユーザー(ログインしていなければAnonymousUser)
    visitor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="visits",
        blank=True, null=True, default=None)
    # 接続元IPアドレス
    remote_addr = models.GenericIPAddressField('接続元IPアドレス')
    # 接続元UserAgent
    user_agent = models.TextField('接続元UserAgent')
    # リクエストHTTPメソッド
    request_method = models.CharField('HTTPメソッド', max_length=10)

    def __str__(self):
        title = self.content.title
        visitor = self.visitor
        if visitor:
            visitor_name = visitor.username
        else:
            visitor_name = "AnonymousUser"
        date = self.created_at.strftime(r"%Y/%m/%d %H:%M:%S")
        return f'[{date}] "{title}" - {visitor_name}'


# class Favorite(TimeStampedModel):
#     content = models.OneToOneField(
#         Content, related_name="likes", on_delete=models.CASCADE)
#     users = models.ManyToManyField(User, related_name='likes')

#     def __str__(self):
#         return f'{self.content.title}'


@receiver(pre_save, sender=Content)
def validate_url_and_auto_fill_embed_html_pre_save(
        sender, instance: Content, *args, **kwargs):
    """URLのvalidation後、コンテンツ保存前にURLに合わせて埋め込み用のHTMLを生成して入力する"""
    if instance.url:
        # URLのクリーニング
        content_type = instance.content_type
        url = utils.clean_content_url(instance.url, content_type)
        instance.url = url
        # URLのバリデーション
        content_url_validator = utils.ContentURLValidator()
        content_url_validator(url, content_type)
        # safetyなURLから埋め込み用のHTMLを取得
        if content_type in utils.EMBED_TYPES:
            get_embed_html = EmbedHTML(content_type, url)
            instance.embed_html = get_embed_html()


@receiver(post_delete, sender=Content)
def auto_remove_image_file_post_delete(sender, instance, *args, **kwargs):
    """コンテンツ削除時に画像削除"""
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


@receiver(pre_save, sender=Content)
def auto_remove_image_on_change(sender, instance, **kwargs):
    """画像変更時に元画像削除"""
    if not instance.pk:
        return False

    try:
        old_file = Content.objects.get(pk=instance.pk).thumbnail
    except Content.DoesNotExist:
        return False

    if not bool(old_file):
        return False

    new_file = instance.thumbnail
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
