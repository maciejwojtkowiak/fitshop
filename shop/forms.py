from django.db.models import fields
from shop.models import Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm



class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="password1",
        widget=forms.PasswordInput(attrs={'class': 'formy'}),
    )
    password2 = forms.CharField(
        label="password2",
        widget=forms.PasswordInput(attrs={'class': 'formy'}),
    )
    class Meta:
        model = User 
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'formy'}),
            'email': forms.TextInput(attrs={'class': 'formy'}),
            
        }

class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'class': 'formy'})
        )
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'formy'}),
    )
    class Meta:
        model = User
        fields = ['username', 'password']
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_image']

class CommentCreationForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'post a comment', 'class':'comment-field'}),
            
        }




