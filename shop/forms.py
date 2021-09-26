from django.db.models import fields
from shop.models import Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



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




