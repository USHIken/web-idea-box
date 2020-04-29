import glob
import os
import random
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# デフォルトのアイコンのPATHをランダムに取得する
def random_icon_path():
    icons = glob.glob(f'{settings.MEDIA_ROOT}/default_icons/*')
    random_index = random.randrange(0, len(icons))
    icon_path = icons[random_index]
    icon_rel_path = "/".join(icon_path.split('/')[3:])
    return icon_rel_path


class User(AbstractBaseUser, PermissionsMixin):

    # 画像ファイルの保存場所
    def get_image_path(self, filename):
        name = str(uuid.uuid4())
        extension = os.path.splitext(filename)[-1]
        return 'icons/' + name + extension

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'ユーザーネーム',
        max_length=50,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),  # noqa: E501
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    profile = models.TextField(
        '自己紹介文', max_length=140, blank=True, null=True, default="")
    icon = models.ImageField(
        'アイコン', blank=True, null=False,
        upload_to=get_image_path, default=random_icon_path)

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),  # noqa: E501
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
