from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Article, Comment

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl border"

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("category", "topic", "content", "image")

        widgets = {
            'category': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            "topic": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "content": CKEditorWidget(attrs={'class': INPUT_CLASSES}),
            "image": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 mb-4 border border-2 border-transparent border-gray-200 rounded-lg focus:ring focus:ring-blue-500 focus:outline-none"
                }
            )
        }
