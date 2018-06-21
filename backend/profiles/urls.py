from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.BaseView.as_view(),name='base'),
    path('register/', views.RegisterView.as_view(),name='register'),
    path('login/', views.UserLoginView.as_view(),name='login'),
    path('logout/', views.UserLogoutView.as_view(),{'next_page': '/'},name='logout'),
    path('u/<int:user_id>/',views.UserProfileView.as_view(), name='profile'),
    path('about', views.AboutView.as_view(),name='about'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)