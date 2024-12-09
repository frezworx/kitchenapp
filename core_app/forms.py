from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core_app.models import DishType


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class DishTypeForm(forms.ModelForm):
    success_message = None

    class Meta:
        model = DishType
        fields = ["name"]
        labels = {
            "name": "Add type dish:",  # Здесь укажите новую надпись
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if DishType.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This type dish already exists.")
        return name
