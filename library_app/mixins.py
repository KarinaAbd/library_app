from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import RedirectURLMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ProjectRedirectURLMixin(RedirectURLMixin):
    next_page = None
    success_message = None
    info_message = None

    def get_default_redirect_url(self):
        """Return the default redirect URL with message."""
        if self.next_page:
            if self.success_message:
                messages.success(self.request, self.success_message)
            elif self.info_message:
                messages.info(self.request, self.info_message)
        return super().get_default_redirect_url()


class ProjectLoginRequiredMixin(LoginRequiredMixin):
    """
    Authentication check.
    Restricts access without authentication.
    Show message about necessarity to log in and redirect on login page.
    """
    login_url = reverse_lazy('login')
    denied_message = "Авторизуйтесь"

    def handle_no_permission(self):
        messages.error(self.request, self.denied_message)
        return redirect(self.login_url)


class HasPermissionUserChangeMixin(UserPassesTestMixin):
    """Only user can change information about him or delete his profile."""
    denied_url = None
    permission_denied_message = None

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.denied_url)
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.get_object() == self.request.user
