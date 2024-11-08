from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_book_list, name='book-list'),
    path('books/<int:pk>/', views.get_book, name='book-detail'),
    path('books/create/', views.create_book, name='book-create'),

    path('members/', views.get_member_list, name='member-list'),
    path('members/<int:pk>/', views.get_member, name='member-detail'),
    path('members/create/', views.create_member, name='member-create'),

    path('transactions/', views.get_transaction_list, name='transaction-list'),
    path('transactions/issue/', views.issue_book, name='issue-book'),
    path('transactions/return/', views.return_book, name='return-book'),
]