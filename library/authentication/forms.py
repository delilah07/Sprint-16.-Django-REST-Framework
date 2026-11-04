
from django import forms

from .models import CustomUser


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=20,
        label='First name',
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'first_name',
            'autocomplete': 'given-name',
            'placeholder': 'First name',
        }),
    )

    last_name = forms.CharField(
        max_length=20,
        label='Last name',
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'last_name',
            'autocomplete': 'family-name',
            'placeholder': 'Last name',
        }),
    )

    middle_name = forms.CharField(
        max_length=20,
        label='Middle name',
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'middle_name',
            'placeholder': 'Middle name',
        }),
    )

    email = forms.EmailField(
        max_length=100,
        label='Email address',
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'autocomplete': 'email',
            'placeholder': 'you@example.com',
        }),
    )

    password = forms.CharField(
        min_length=8,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'autocomplete': 'new-password',
            'placeholder': 'Create a password',
        }),
    )

    password_confirm = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'id': 'password_confirm',
            'autocomplete': 'new-password',
            'placeholder': 'Repeat password',
        }),
    )

    role = forms.ChoiceField(
        choices=[
            ('0', 'Guest'),
            ('1', 'Librarian'),
        ],
        label='Register as',
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip()

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'A user with this email already exists.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error(
                'password_confirm',
                'Passwords do not match.'
            )

        return cleaned_data

    def save(self):
        return CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            middle_name=self.cleaned_data['middle_name'],
            role=int(self.cleaned_data['role']),
        )


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label='Email address',
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'autocomplete': 'email',
            'placeholder': 'you@example.com',
        }),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'autocomplete': 'current-password',
            'placeholder': 'Enter your password',
        }),
    )
