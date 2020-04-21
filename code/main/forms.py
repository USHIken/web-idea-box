from django import forms

from main.models import Content


class ContentCreateForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ("content_type", "title", "description", "thumbnail", "url")


class ContentUpdateForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ("title", "description", "thumbnail", "url")
