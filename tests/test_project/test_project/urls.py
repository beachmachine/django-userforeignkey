from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^polls/', include("test_project.polls.urls", namespace="polls")),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name="logout"),
]
