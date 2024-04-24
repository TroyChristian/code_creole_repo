# Django
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label="",  widget=forms.TextInput(attrs={'class':"username", 'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"password",'placeholder':'Password'}))