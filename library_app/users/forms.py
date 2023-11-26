from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, UsernameField
from django.forms import CharField, PasswordInput

from library_app.users.models import User


class UserForm(UserCreationForm):
    first_name = CharField(max_length=150,
                           required=True,
                           label="Имя")
    last_name = CharField(max_length=150,
                          required=True,
                          label="Фамилия")
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'
        )


class UserUpdateForm(UserChangeForm):
    password = None
    password1 = CharField(
        label= "Пароль",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = CharField(
        label= "Подтверждение пароля",
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text= "Введите пароль ещё раз",
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2'
        )
