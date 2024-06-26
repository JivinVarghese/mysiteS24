# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    response = HttpResponse()

    # List of books ordered by primary key
    booklist = Book.objects.all().order_by('pk')
    response.write('<p>List of available books:</p>')
    for book in booklist:
        response.write(f'<p>{book.id}: {book.title}</p>')

    # List of publishers ordered by city name in descending order
    publisherlist = Publisher.objects.all().order_by('-city')
    response.write('<p>List of publishers:</p>')
    for publisher in publisherlist:
        response.write(f'<p>{publisher.name} - {publisher.city}</p>')

    return response

def about(request):
    return HttpResponse("This is an Ebook App.")

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return HttpResponse(f"Title: {book.title.upper()}<br>Price: ${book.price}<br>Publisher: {book.publisher}")