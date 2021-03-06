from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from it_articles.models import Article
from .models import User

class UserRegisterForm(UserCreationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print('REGISTER FORM')
		self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
		self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
		self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
		self.fields['password2'].widget.attrs.update({'placeholder': 'Password confirmation'})

class UserLoginForm(AuthenticationForm, forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

	def __init__(self, request = None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print('LOGIN FORM')
		self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
		self.fields['username'].widget.attrs.update({'placeholder': 'Username'})

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'age', 'gender']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#for field in self.fields:
			#self.fields[field].widget.attrs['autocomplete'] = 'off'
		self.fields['first_name'].widget.attrs['placeholder'] = 'Your first name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Your last name'
		self.fields['age'].widget.attrs['placeholder'] = 'Your age'
		self.fields['username'].widget.attrs['placeholder'] = 'Your username'
		self.fields['email'].widget.attrs['placeholder'] = 'Your email'
		#self.fields['image'].widget.attrs['enctype'] = 'multipart/form-data'



