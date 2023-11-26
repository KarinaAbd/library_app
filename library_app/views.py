from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from library_app.mixins import ProjectRedirectURLMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLogInView(ProjectRedirectURLMixin, LoginView):
    template_name = 'layouts/form.html'
    extra_context = {
        'title': 'Авторизоваться',
        'button_text': 'Войти'
    }
    next_page = reverse_lazy('index')
    success_message = 'Вы авторизованы'


class UserLogOutView(ProjectRedirectURLMixin, LogoutView):
    next_page = reverse_lazy('index')
    info_message = 'Вы разлогинились'
