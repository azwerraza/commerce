from django import forms
from .models import Comment
from .models import Subscriber, UserImage

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Share your styling tips or ask questions...',
                'class': 'form-control',
                'rows': 4
            })
        }

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'style': 'width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;',
            }),
        }


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']