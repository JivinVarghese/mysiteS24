from django.shortcuts import render
from .models import Book

def home(request):
    return render(request, 'home.html')
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})

def about(request):
    return render(request, 'myapp/about0.html')

def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'myapp/detail0.html', {"book": book})