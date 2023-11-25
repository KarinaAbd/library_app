from django.forms import ModelForm

from library_app.books.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'author', 'year', 'isbn'
        )
