from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review, ShippingAddress


class LoginForm(AuthenticationForm):
    """this class for login form """

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'id': 'userName',
        'name': 'userName',
        'placeholder': 'Username',
        'type': 'text'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'pwd',
        'name': 'password',
        'placeholder': 'Password'
    }))


class RegisterForm(UserCreationForm):
    """this class for register form """

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'id': 'form3Example3',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write..'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email..'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name..'
            })

        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'region', 'city', 'zip_code', 'mobile', 'email']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address..'
            }),
            'region': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Region'
            }),
            'city': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'city..'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123..'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1233..'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email..'
            })

        }
