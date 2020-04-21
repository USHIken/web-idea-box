from django import forms

from main.models import Content


class ContentCreateForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ("title", "description", "content_type", "thumbnail", "url")
