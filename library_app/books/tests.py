import json

from django.contrib.messages.storage.cookie import CookieStorage
from django.test import Client, TestCase

from django.urls import reverse_lazy

from library_app.books.models import Book


def get_fixture_content(file_path):
    with open(f'library_app/fixtures/{file_path}', 'r') as input:
        return json.load(input)


class BookTestCase(TestCase):
    """Test case for CRUD of books."""
    fixtures = ["books.json"]

    test_data = get_fixture_content('test_data.json')
    book_data = test_data['test_book'].copy()

    def setUp(self) -> None:
        self.client = Client()
        self.book_count = Book.objects.count()

    def test_create_book(self) -> None:
        response = self.client.get(reverse_lazy('book_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse_lazy('book_create'),
                                    data=self.book_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('book_list'))

        book = Book.objects.last()
        self.assertEqual(book.title, self.book_data['title'])
        self.assertEqual(book.author, self.book_data['author'])
        self.assertEqual(book.year, self.book_data['year'])
        self.assertEqual(book.isbn, self.book_data['isbn'])
        self.assertEqual(book.url, self.book_data['url'])
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Новая книга добавлена!',
                      messages_container)

    def test_list_book(self) -> None:
        self.client.post(reverse_lazy('book_create'),
                         data=self.book_data)
        response = self.client.get(reverse_lazy('book_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.book_data['title'])
        self.assertContains(response, self.book_data['author'])

    def test_page_book(self) -> None:
        self.client.post(reverse_lazy('book_create'),
                         data=self.book_data)
        book = Book.objects.last()

        response = self.client.get(reverse_lazy('book_page',
                                   kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.book_data['title'])
        self.assertContains(response, self.book_data['author'])
        self.assertContains(response, self.book_data['year'])
        self.assertContains(response, self.book_data['isbn'])

    def test_update_book(self) -> None:
        self.client.post(reverse_lazy('book_create'),
                         data=self.book_data)
        book = Book.objects.last()

        response = self.client.get(reverse_lazy('book_update',
                                   kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse_lazy('book_update', kwargs={'pk': book.id}),
            {
                'title':
                'Clean Code: A Handbook of Agile Software Craftsmanship',
                'author': self.book_data['author'],
                'year': self.book_data['year'],
                'isbn': self.book_data['isbn'],
                'url': self.book_data['url']
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('book_list'))
        book.refresh_from_db()
        self.assertEqual(
            book.title,
            'Clean Code: A Handbook of Agile Software Craftsmanship'
        )
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Изменения сохранены!',
                      messages_container)

    def test_delete_book(self) -> None:
        self.client.post(reverse_lazy('book_create'),
                         data=self.book_data)
        book = Book.objects.last()

        response = self.client.get(reverse_lazy('book_delete',
                                   kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse_lazy('book_delete', kwargs={'pk': book.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('book_list'))
        self.assertNotContains(response, self.book_data['title'],
                               status_code=302)
        self.assertEqual(Book.objects.count(), self.book_count)
        messages_container = [
            str(message) for message in CookieStorage(response)._decode(
                response.cookies['messages'].value
            )
        ]
        self.assertIn('Книга удалена',
                      messages_container)
