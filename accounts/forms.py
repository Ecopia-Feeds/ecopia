from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Full Name",
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Email",
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Phone",
        })
    )
    role_choice = forms.ChoiceField(
        choices=CustomUser.Role.choices,   # Comes from your model Enum
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border p-2",
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Password",
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Confirm Password",
        })
    )

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "phone", "role_choice", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Assign role
        user.role_choice = self.cleaned_data["role_choice"]

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Email or Phone",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-lg border p-2",
            "placeholder": "Password",
        })
    )