from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('feedback/', views.getFeedback, name='feedback1'),
    path('findbooks/', views.findbooks, name='findbooks'),
    ]
