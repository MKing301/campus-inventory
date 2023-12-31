from django.urls import path, reverse_lazy
from . import views
from .views import PasswordsChangeView
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("core/inventory", views.inventory, name="inventory"),
    path("core/add_item", views.add_item, name="add_item"),
    path("core/edit_item/<int:id>", views.edit_item, name="edit_item"),
    path("core/load_areas", views.load_areas, name="load_areas"),
    path("core/notes/<int:id>", views.notes, name="notes"),
    path(
        "core/export_to_excel", views.export_to_excel, name="export_to_excel"
    ),
    path("accounts/logout/", views.logout_request, name="logout_request"),
    path("accounts/login/", views.login_request, name="login_request"),
    path("register/", views.register, name="register"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path(
        "<int:id>/password/",
        PasswordsChangeView.as_view(
            template_name='accounts/password_change.html'
        )
    ),
    path(
        "accounts/password_changed/",
        views.password_changed,
        name="password_changed"),
    path(
        "accounts/password-reset/",
        PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            success_url=reverse_lazy('core:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        "accounts/password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('core:password_reset_complete')
        ),
        name='password_reset_confirm'),
    path(
        "accounts/password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'),
    path("contact/", views.contact, name='contact'),
]

htmx_urlpatterns = [
    path(
        'register/check_username/', views.check_username, name='check_username'
        ),
    path(
        'register/check_email/', views.check_email, name='check_email'
        ),
]

urlpatterns += htmx_urlpatterns