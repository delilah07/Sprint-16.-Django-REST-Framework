from django import forms

from .models import Author


class AuthorForm(forms.ModelForm):

    name = forms.CharField(
        max_length=20,
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'name',
            'placeholder': 'Enter first name',
        }),
    )

    surname = forms.CharField(
        max_length=20,
        required=True,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'surname',
            'placeholder': 'Enter surname',
        }),
    )

    patronymic = forms.CharField(
        max_length=20,
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'patronymic',
            'placeholder': 'Enter patronymic',
        }),
    )

    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']

        labels = {
            'name': 'First name',
            'surname': 'Surname',
            'patronymic': 'Patronymic',
        }