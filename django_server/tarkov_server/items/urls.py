from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", views.Main.as_view(), name='main'),
    path("registration/", views.RegisterView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.MyLogoutView.as_view(), name='logout'),
    path("check/", views.CheckView.as_view(), name='check_view'),
    path("item/", csrf_exempt(views.get_item_data), name='items'),
    path("item/lng/", views.change_language, name='language'),
    path("download/", views.download, name='download'),
    path("download_instruction/", views.download_instruction, name='download_ins'),
    path("profile/", views.get_profile, name='profile'),
    path("change/", views.ChangePasswordView.as_view(), name='change'),
    path("message/", views.ChangePasswordView.as_view(), name='message'),
    path("drop/", views.DropPasswordView.as_view(), name='drop'),
    path("ip/", csrf_exempt(views.ChechIpView.as_view()), name='check_ip'),
    path("test/", csrf_exempt(views.TestConnectView.as_view()), name='test_connect'),
]

