from django import forms
from .models import post,Comments

class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('author','title','text')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),

        }
class commentForm(forms.ModelForm):
    class Meta:
        model= Comments
        fields= ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),

        }