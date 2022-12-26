from django.urls import path
from .views import *

urlpatterns = [
    path('list-menu/', list_menu, name="list_menu"),
    path('add-customer/', add_customer, name="add_customer"),
    path('add-book/', add_book, name="add_book"),
    path('loan-book/', loan_book, name="loan_book"),
    path('display-customers/', display_customers, name="display_customers"),
    path('display-books/', display_books, name="display_books"),
    path('display-loans/', display_loans, name="display_loans"),
    path('display-late-loans/', display_late_loans, name="display_late_loans"),
    path('active-loans/', active_loans, name="active_loans"),
    path('return-book/<int:id>/', return_book, name="return_book"),
    path('remove-book/<int:id>/', remove_book, name="remove_book"),
    path('remove-customer/<int:id>/', remove_customer, name="remove_customer"),
]