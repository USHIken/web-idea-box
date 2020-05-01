from django import forms

from main.models import Content
from main.utils import clean_content_url, ContentURLValidator


class ContentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
        self.fields["thumbnail"].widget = forms.widgets.FileInput()
        self.fields["thumbnail"].widget.attrs["style"] = "display: none;"

    def clean_url(self):
        # URLのクリーニング
        content_type = self.cleaned_data.get("content_type")
        url = self.cleaned_data.get("url")
        url = clean_content_url(url, content_type)
        # URLのバリデーション
        content_url_validator = ContentURLValidator()
        content_url_validator(url, content_type)
        return url


class ContentCreateForm(ContentForm):

    class Meta:
        model = Content
        fields = ("content_type", "title", "description", "thumbnail", "url")


class ContentUpdateForm(ContentForm):

    class Meta:
        model = Content
        fields = ("title", "description", "thumbnail", "url")
