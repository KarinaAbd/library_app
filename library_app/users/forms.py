from time import sleep

from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField, PasswordInput
from django.core.mail import send_mail

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

    def send_email(self):
        """Sends an email when the user creation form has been submitted."""
        sleep(20)  # Simulate expensive operation that freezes Django
        send_mail(
            "Привет!",
            "Рады видеть вас в нашей Маленькой библиотеке питониста! Заходите почаще!",
            "support@example.com",
            [self.cleaned_data["email"]],
            fail_silently=False,
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
