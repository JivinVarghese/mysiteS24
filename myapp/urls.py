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
    path('review/',views.review, name='review')

]
