from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from library_app.books.forms import BookForm
from library_app.books.models import Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookCreateView(SuccessMessageMixin,
                     generic.CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    success_message = 'Новая книга добавлена!'


class BookUpdateView(SuccessMessageMixin,
                     generic.UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    success_message = 'Изменения сохранены!'


class BookDeleteView(SuccessMessageMixin,
                     generic.DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    success_message = 'Книга удалена'


class BookPageView(generic.DetailView):
    model = Book
