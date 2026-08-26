from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
            register,   
            client_register,
            counsellor_register,
            login_view,
            logout_view,
            update_profile,
            settings_view,
            gen_dashboard
    )


urlpatterns = [
    path("register/", register, name="register"),
    path("register/client/", client_register, name="client_register",),
    path("register/counsellor/", counsellor_register,  name="counsellor_register", ),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html" ), name="password_reset", ),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html" ),  name="password_reset_done", ),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html" ), name="password_reset_confirm", ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html" ), name="password_reset_complete", ),
    path("profile/", update_profile, name="update_profile",),
    path("settings/", settings_view, name="settings"),
    path("gen-dashboard/", gen_dashboard, name="gen_dashboard"),
]