from django.urls import path
from .views import *

urlpatterns = [
	path('',index,name = 'index'),
	path('books/', BookListView.as_view(), name='books'),
	path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
	path('name/',get_name, name = 'name'),
]