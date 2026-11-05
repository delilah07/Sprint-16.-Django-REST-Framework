from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list_api, name='author_list_api'),
    path('<int:author_id>/', views.author_detail_api, name='author_detail_api'),
]