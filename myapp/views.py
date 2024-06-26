from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .forms import FeedbackForm

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
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})
