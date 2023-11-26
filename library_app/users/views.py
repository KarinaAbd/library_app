from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from library_app.mixins import ProjectLoginRequiredMixin, HasPermissionUserChangeMixin
from library_app.users.forms import UserForm, UserUpdateForm
from library_app.users.models import User


class UserListView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin,
                     generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'layouts/form.html'
    extra_context = {
        'title': 'Регистрация',
        'button_text': 'Подтвердить',
    }
    success_url = reverse_lazy('login')
    success_message = 'Вы зарегестрированы!'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class UserUpdateView(ProjectLoginRequiredMixin,
                     HasPermissionUserChangeMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'layouts/form.html'
    extra_context = {
        'title': 'Изменить данные',
        'button_text': 'Сохранить',
    }
    success_url = reverse_lazy('user_list')
    success_message = 'Изменения сохранены!'
    denied_url = reverse_lazy('user_list')
    permission_denied_message = 'Нельзя изменять данные других пользователей'

class UserDeleteView(ProjectLoginRequiredMixin,
                     HasPermissionUserChangeMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    model = User
    template_name = 'layouts/delete.html'
    context_object_name = 'user'
    extra_context = {
        'title': 'Удалить',
        'button_text': 'Да, точно',
    }
    success_url = reverse_lazy('user_list')
    success_message = 'Пользователь удален'
    denied_url = reverse_lazy('user_list')
    permission_denied_message = 'Нельзя удалять других пользователей'

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = user.get_full_name()
        return context


class UserPageView(generic.DetailView):
    model = User
    template_name = 'users/user_page.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['name'] = user.username
        return context
