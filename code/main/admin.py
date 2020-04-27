from django.contrib import admin
from main.models import Content
from markdownx.admin import MarkdownxModelAdmin


admin.site.register(Content, MarkdownxModelAdmin)
