from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Review
from .forms import FeedbackForm
from .forms import SearchForm, OrderForm, ReviewForm

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
            feedback = form.cleaned_data.get('feedback', [])
            choices = []
            if 'B' in feedback:
                choices.append(' to borrow books') 
            if 'P' in feedback:
                choices.append(' to purchase books')
            if not feedback: 
                choices.append(' None.')
            
            choice = ' &'.join(choices)
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {
                'name': name,
                'category': category,
                'booklist': booklist
            })
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})

#lab8
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            order.books.set(books)  # Associate the selected books with the order
            order.save()  # Save again to persist the relationship

            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})
    

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                review.save()
                
                # Increment num_reviews for the specified book
                book = review.book
                book.num_reviews += 1
                book.save()

                return redirect('/myapp/')  # Redirect to the main page after successful submission
            else:
                return HttpResponse('You must enter a rating between 1 and 5!')
        else:
            return HttpResponse('Form submission error. Please check your input.')
    else:
        form = ReviewForm()

    return render(request, 'myapp/review.html', {'form': form})

