import json

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.storage.cookie import CookieStorage

from library_app.users.models import User



def get_fixture_content(file_path):
    with open(f'library_app/fixtures/{file_path}', 'r') as input:
        return json.load(input)


class UserTestCase(TestCase):
    """Test case for CRUD of user."""
    fixtures = ['users.json']

    test_data = get_fixture_content('test_data.json')
    user_data = test_data['test_user'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.user_count = User.objects.count()

    def test_create_user(self) -> None:
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(reverse('user_create'),
                                    data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        user = User.objects.last()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.username, self.user_data['username'])
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Вы зарегестрированы!',
                      messages_container)

    def test_list_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users.html')
        self.assertContains(response, 'Ник')
        self.assertContains(response, 'Дата регистрации')
        self.assertContains(response, self.user_data['username'])

    def test_update_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        user = User.objects.last()
        self.client.force_login(user)

        response = self.client.get(reverse('user_update',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/form.html')

        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'first_name': self.user_data['first_name'],
                'last_name': 'Newman',
                'username': self.user_data['username'],
                'email': self.user_data['email'],
                'password1': self.user_data['password1'],
                'password2': self.user_data['password2']
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, 'Newman')
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password1']))
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Изменения сохранены!',
                      messages_container)

    def test_delete_user(self) -> None:
        self.client.post(reverse('user_create'),
                         data=self.user_data)
        user = User.objects.last()
        self.client.force_login(user)

        response = self.client.get(reverse('user_delete',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='layouts/delete.html')

        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        self.assertEqual(User.objects.count(), self.user_count)
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Пользователь удален',
                      messages_container)


class UserWrongTestCase(TestCase):
    """Test case for CRUD of user with wrong conditions."""
    fixtures = ['users.json']

    test_data = get_fixture_content('test_data.json')
    user_data = test_data['test_user'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.user_count = User.objects.count()
        self.login_user = User.objects.first()
        self.client.force_login(self.login_user)

    def test_update_other_user(self) -> None:
        user = User.objects.last()
        response = self.client.get(reverse('user_update',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))

    def test_delete_other_user(self) -> None:
        user = User.objects.last()
        response = self.client.get(reverse('user_delete',
                                           kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
