# Django
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import Thread, ThreadMessage


#this app
User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField(
		label=_('Username'),
		widget=forms.TextInput(
			attrs={
				'class': "username",
				'placeholder': _('Username')  # Marking the placeholder text for translation
			}
		)
	)
	password = forms.CharField(
		label=_('Password'),
		widget=forms.PasswordInput(
			attrs={
				'class': "password",
				'placeholder': _('Password')  # Marking the placeholder text for translation
			}
		)
	)

class RegistrationForm(forms.ModelForm):
	email = forms.EmailField(max_length=200, label=_("Email Address"))
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"col1"}), label=_("Username"))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"col1"}), label=_("Password"))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"col1"}), label=_("Confirm Password"))
	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'confirm_password']

	def clean_password(self):
		# Check that the two password entries match
		password = self.cleaned_data.get("password")
		confirm_password = self.data.get("confirm_password")
		
		if (password and confirm_password) and (password == confirm_password):
			return password 
		else:
			raise forms.ValidationError(_("Passwords don't match"))
	def clean_email(self):
		email = self.cleaned_data.get('email')
		
		# Use Django's built-in validator to check for a valid email
		try:
			validate_email(email)
		except ValidationError:
			raise ValidationError(_("Invalid email format."))
		
		# Additional custom validation: check if the email is already in use
		if User.objects.filter(email=email).exists():
			raise ValidationError(_("Email already registered."))

		# Any other custom email validation logic can go here

		return email

class CommentForm(forms.Form):
	body = forms.CharField(label=False)

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['body'].widget = forms.TextInput(attrs=({'class':'reply_text','enter_comment':_('add a comment')}))

class EditCommentForm(forms.ModelForm):
	
	class Meta:
		model = ThreadMessage
		fields =['body']

