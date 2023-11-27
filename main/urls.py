from django.urls import path
from . import views

app_name = 'og'

urlpatterns = [
	path('', views.main, name = 'main'),
]