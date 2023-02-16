from django.urls import path 
from . import views

urlpatterns = [
    # path('books/', views.books)
    path('books/', views.BookView),
    path('books/<int:pk>', views.SingleBookView.as_view()),
]