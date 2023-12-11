from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
	path('', views.main, name = 'main'),
    path('/item_make', views.item_make, name = 'item_make'),
    path('/item_list', views.item_list, name = 'item_list'),
    path('/item_entry_list', views.item_entry_list, name = 'item_entry_list'),
    path('/item_mine_list', views.item_mine_list, name = 'item_mine_list'),
    path('/item_entry', views.item_entry, name = 'item_entry'),
    path('/item_detail/<int:item_id>', views.item_detail, name = 'item_detail')
]