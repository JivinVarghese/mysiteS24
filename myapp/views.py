from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg
from .models import Book, Review, Member
from .forms import FeedbackForm
from .forms import SearchForm, OrderForm, ReviewForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
import math
import random

def home(request):
    return render(request, 'home.html')
def index(request):
    last_login = request.session.get('last_login')

    if last_login:
        last_login_time = datetime.fromisoformat(last_login)
        message = f'Your last login was on {last_login_time.strftime("%Y-%m-%d %H:%M:%S")}'
    else:
        message = 'Your last login was more than one hour ago'
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist, 'message':message})

def about(request):
    mynum = request.COOKIES.get('lucky_num')

    if not mynum:
        mynum = random.randint(1, 100)
        response = render(request, 'myapp/about0.html', {'mynum': mynum})
        expires_at = timezone.now() + timedelta(minutes=5)
        response.set_cookie('lucky_num', mynum, expires=expires_at)
        return response

    return render(request, 'myapp/about0.html', {'mynum': mynum})
    # return render(request, 'myapp/about0.html')

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
            sq_root_rating = math.sqrt(rating)
            # print(type(sq_root_rating) == int)
            # if 1 <= rating <= 5:
            if type(sq_root_rating) == int:
                review = form.save(commit=False)
                review.save()
                
                # Increment num_reviews for the specified book
                book = review.book
                book.num_reviews += 1
                book.save()

                return redirect('/myapp/')  # Redirect to the main page after successful submission
            else:
                # return HttpResponse('You must enter a rating between 1 and 5!')
                return HttpResponse('You must enter a rating must be a perfect square.')
        else:
            return HttpResponse('Form submission error. Please check your input.')
    else:
        form = ReviewForm()

    return render(request, 'myapp/review.html', {'form': form})


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(timezone.now())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.') 
    else:
        return render(request, 'myapp/login.html', {'form':LoginForm})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def chk_reviews(request, book_id):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        return HttpResponse('You are not a registered member!')

    book = Book.objects.get(pk=book_id)
    avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']

    if avg_rating is None:
        message = 'There are no reviews submitted for this book.'
    else:
        message = f'The average rating for the book is {avg_rating:.2f}.'

    return render(request, 'myapp/chk_reviews.html', {'message': message})