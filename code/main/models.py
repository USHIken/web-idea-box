import os
import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User
from main import utils
from main.utils import EmbedHTML


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


@receiver(pre_save, sender=Content)
def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.embed_html = EmbedHTML(instance.content_type, instance.url).get()
