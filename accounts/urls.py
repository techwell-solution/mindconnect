from django.urls import path
from .views import (
    register,   
    client_register,
    counsellor_register,
    login_view,
    logout_view
)


urlpatterns = [
    path("register/", register, name="register"),
    path("register/client/", client_register, name="client_register",),
    path("register/counsellor/", counsellor_register,  name="counsellor_register", ),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout")
]