from django.contrib import admin
from main.models import Content, ContentVisit
from markdownx.admin import MarkdownxModelAdmin


admin.site.register(Content, MarkdownxModelAdmin)
admin.site.register(ContentVisit)
