import os
import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User
from main import utils
from main.utils import EmbedHTML


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(models.Model):

    # 画像ファイルの保存場所
    def get_image_path(self, filename):
        name = str(uuid.uuid4())
        extension = os.path.splitext(filename)[-1]
        return 'images/' + name + extension

    # 製作者
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contents")
    # タイトル
    title = models.CharField(max_length=64)
    # 説明
    description = models.TextField(blank=True, null=False)
    # コンテンツのタイプ
    content_type = models.CharField(
        choices=utils.CONTENT_TYPES, default=utils.SCRATCH, max_length=32)
    # 一覧で表示される画像
    thumbnail = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    # プロジェクトの各種サイトURL
    url = models.URLField(blank=True, null=False, default="")
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


@receiver(pre_save, sender=Content)
def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.embed_html = EmbedHTML(instance.content_type, instance.url).get()
