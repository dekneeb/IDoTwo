from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ('name', 'body')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'body' : forms.Textarea(attrs = {'class' : 'form-control'}),
        }

    #      comment = forms.CharField(
    #     label='',
    #     widget=forms.Textarea(attrs={
    #         'rows': '3',
    #         'placeholder': 'Leave a comment...'
    #     })
    # )
    # class Meta:
    #     model = Comment
    #     fields = ['comment']

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.Form):
    message= forms.CharField(label='', max_length=1000)
