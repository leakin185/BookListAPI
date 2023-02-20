from django.urls import path 
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/', views.BookView),
    path('books/<int:pk>', views.SingleBookView.as_view()),
    path('book-items',views.BookViewVersion2.as_view({'get':'list'})),
    path('book-items/<int:pk>',views.BookViewVersion2.as_view({'get':'retrieve'})),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    path('book/',views.Book),
    path('welcome',views.welcome),
    path('secret', views.secret),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('manager-view/', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    path('groups/manager/users', views.managers),
]