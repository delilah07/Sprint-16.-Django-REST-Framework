from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'title',
            'placeholder': 'Search by title...',
        }),
    )

    author = forms.CharField(
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={
            'id': 'author',
            'placeholder': 'Search by author...',
        }),
    )
