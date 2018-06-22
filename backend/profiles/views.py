from django.conf import settings
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .backends import UserAuthentication
from django.shortcuts import redirect,get_object_or_404,Http404
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserCreateForm,LoginForm
from .models import Profile,User

class BaseView(generic.TemplateView):
    template_name = 'profiles/base.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(BaseView, self).get_context_data(*args, **kwargs)
        context['user'] = Profile.objects.filter(pk=self.request.user.pk)
        return context

class AboutView(generic.TemplateView):
    template_name = 'profiles/about.html'

class RegisterView(generic.CreateView):
    template_name = 'profiles/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('profiles:base')
    
    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        pwd = form.cleaned_data.get('password1')
        user = UserAuthentication.authenticate(self.request,username=username, password=pwd)
        user.refresh_from_db()
        login(self.request, user)
        return valid

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'profiles/login.html'
    redirect_authenticated_user = reverse_lazy('profiles:base')
    redirect_field_name = reverse_lazy('profiles:base')
    form = LoginForm

class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = 'profiles:login'
    next_page = 'profiles:base'


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'
    