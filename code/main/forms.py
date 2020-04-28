from django import forms

from main.models import Content


class ContentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
        self.fields["thumbnail"].widget = forms.widgets.FileInput()
        self.fields["thumbnail"].widget.attrs["style"] = "display: none;"


class ContentCreateForm(ContentForm):

    class Meta:
        model = Content
        fields = ("content_type", "title", "description", "thumbnail", "url")


class ContentUpdateForm(ContentForm):

    class Meta:
        model = Content
        fields = ("title", "description", "thumbnail", "url")
