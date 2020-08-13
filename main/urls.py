from django.urls import path
from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('home/', views.homepage, name='home'),
	path('upload/', views.uploadpage, name='upload'),
	path('images/<int:index>/', views.imagepage, name='image')
]