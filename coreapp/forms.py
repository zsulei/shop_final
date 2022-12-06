from django import forms
from django.contrib.auth import authenticate
from .models import Client, Product
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.images import get_image_dimensions


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ('username', 'first_name', 'last_name', 'avatar')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class AvatarUpdateForm(forms.Form):
    avatar = forms.ImageField()


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
