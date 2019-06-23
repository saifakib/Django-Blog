from django import forms
from .models import Article, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CreateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]

class RegistationForm(UserCreationForm):
    username = forms.CharField(max_length=100,required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Enter Your First Name')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(max_length=254, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment'
        ]