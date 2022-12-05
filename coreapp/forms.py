from django import forms
from django.contrib.auth import authenticate
from .models import Client
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

    # class Meta:
    #     model = Client
    #     fields = ('avatar', )

# class ClientRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'id': 'password1'}), )
#     password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'id': 'password2'}), )
#
#     class Meta:
#         model = Client
#         fields = ('first_name', 'last_name', 'email', )
#
#     def clean_password(self):
#         cd = self.cleaned_data
#         return cd['password']
#
#
# class ClientLoginForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput, )
#
#     class Meta:
#         model = Client
#         fields = ('username', 'password', )
#         widgets = {
#             'email': forms.EmailInput,
#             'password': forms.PasswordInput
#            }

    # def clean(self):
    #     if self.is_valid():
    #         email = self.cleaned_data.get('email')
    #         password = self.cleaned_data.get('password')
    #         if not authenticate(email=email, password=password):
    #             raise forms.ValidationError('WRONG LOGIN/PASSWORD')

