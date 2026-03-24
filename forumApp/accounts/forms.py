from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser


class AppUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = (
            "Required: 150 characters or fewer, digits and @/./+/-/_ only"
        )


class CustomUserForm(UserCreationForm):
    # noinspection PyUnresolvedReferences
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    # noinspection PyUnresolvedReferences
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'
