from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy


class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name='authentication/login.html'

    def get_success_url(self):
        return reverse_lazy('user_index')

    def form_invalid(self, form):
        messages.error(self.request,'Неправильный логин или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(LogoutView):
    next_page = reverse_lazy('login')
