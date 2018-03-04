from django import forms
from .models import Article
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password']
		widgets = {
			"password": forms.PasswordInput()
		}

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = ['title', 'content', 'image', 'publish_date']
        exclude = ['author']

        widgets = {
        	"publish_date": forms.DateInput(attrs={"type":"date"})
        }
    