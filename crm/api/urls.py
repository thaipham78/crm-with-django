from django.contrib import admin
from django.urls import path, include
from .views import (
    CompanyListApiView,
    CompanyDetailApiView,
    ContactListApiView,
    ContactDetailApiView,
    # UserListApiView,
    LoginView,
)

urlpatterns = [
    path("api/company", CompanyListApiView.as_view()),
    path("api/company/<int:company_id>/", CompanyDetailApiView.as_view()),
    path("api/contact", ContactListApiView.as_view()),
    path("api/contact/<int:contact_id>/", ContactDetailApiView.as_view()),
    path("api/login", LoginView.as_view()),
    # path("api/user", UserListApiView.as_view()),
]
