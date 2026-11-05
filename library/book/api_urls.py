from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_api, name='book_list_api'),
    path('<int:book_id>/', views.book_detail_api, name='book_detail_api'),
]