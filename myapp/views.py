from django.shortcuts import render, get_object_or_404,redirect
from myapp.forms import OrderForm
from myapp.models import Book
from django.http import HttpResponse
from .forms import FeedbackForm
from .forms import SearchForm

def home(request):
    return render(request, 'home.html')

# def about(request):
#     return render(request, 'about.html')


def about(request):
    return render(request, 'myapp/about.html')


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/details.html', {'book': book})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else: choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(price__lte=max_price, category=category)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'booklist': booklist})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')  # Replace with your success URL
    else:
        form = OrderForm()
    return render(request, 'myapp/create_order.html', {'form': form})