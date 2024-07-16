from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('feedback/', views.getFeedback, name='feedback'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('place_order/', views.place_order, name='place_order'),#lab 8
    path('review/',views.review, name='review'),
    path('login/', views.user_login, name='login'),
    path('chk_reviews/<int:book_id>/', views.chk_reviews, name='chk_reviews'),
    path('logout/',views.user_logout, name='logout')
]
