from django import forms


class UserRegistrationForm(forms.Form):

    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32,
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.EmailInput(),
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput(),
    )


class UserUpdateForm(forms.Form):

    email = forms.CharField(
        required=False,
        label='Email',
        max_length=32,
        widget=forms.EmailInput(),
    )
    password = forms.CharField(
        required=False,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput(),
    )
