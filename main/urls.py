from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search_page, name='search'),
    path('help', views.help, name='help'),
    path('result/<int:search_id>', views.results, name='result'),
]
