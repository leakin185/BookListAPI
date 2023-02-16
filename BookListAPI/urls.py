from django.urls import path 
from . import views

urlpatterns = [
    path('books/', views.BookView.as_view()),
    path('books/<int:pk>', views.SingleBookView.as_view()),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    path('book/',views.Book),
    path('welcome',views.welcome),
]