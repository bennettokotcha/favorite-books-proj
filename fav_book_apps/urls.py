from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register_login),
    path('books', views.books),
    path('login', views.login),
    path('logout', views.logout),
    path('add-book', views.add_book),
    path('books/<int:number>', views.book_details),
    path('add-book/edit/<int:number>', views.edit_book),
    path('add-likes/<int:number>', views.add_likes),
    path('destroy/<int:number>', views.delete_book),
    path('remove-like/<int:number>', views.remove_book),
]