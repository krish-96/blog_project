from django import forms
from .models import ContactUs, Comment, Post, Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class CreatePostForm(forms.ModelForm):
    content = forms.Textarea()
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_pic', 'slug',  'status' , 'privacy']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 15}),

        }

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, label='Comment Message')
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"

class UpdateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name',  'phone_no', 'email', 'address',  'photo' , 'about']