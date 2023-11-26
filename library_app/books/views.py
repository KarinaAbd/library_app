from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from library_app.books.forms import BookForm
from library_app.books.models import Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = 'books/books.html'
    context_object_name = 'books'
    extra_context = {
        'button_text': 'Подробнее',
    }


class BookCreateView(SuccessMessageMixin,
                     generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = 'layouts/form.html'
    extra_context = {
        'title': 'Добавить книгу',
        'button_text': 'Сохранить',
    }
    success_url = reverse_lazy('book_list')
    success_message = 'Новая книга добавлена!'


class BookUpdateView(SuccessMessageMixin,
                     generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'layouts/form.html'
    extra_context = {
        'title': 'Изменить данные',
        'button_text': 'Сохранить',
    }
    success_url = reverse_lazy('book_list')
    success_message = 'Изменения сохранены!'


class BookDeleteView(SuccessMessageMixin,
                     generic.DeleteView):
    model = Book
    template_name = 'layouts/delete.html'
    context_object_name = 'book'
    extra_context = {
        'title': 'Удалить книгу',
        'button_text': 'Да, точно',
    }
    success_url = reverse_lazy('book_list')
    success_message = 'Книга удалена'

    def get_context_data(self, **kwargs):
        book = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = book.title
        return context


class BookPageView(generic.DetailView):
    model = Book
    template_name = 'books/book_page.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        book = self.get_object()
        context = super().get_context_data(**kwargs)
        context['book_title'] = book.title
        return context
