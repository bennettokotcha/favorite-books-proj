from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'login.html')

def register_login(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, 'Email already exist, please register with a different email address!')
            return redirect('/')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)

            user1 = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
                confirm_pw=request.POST['confirm_pw']
                )
            request.session['username'] = user1.first_name
            request.session['userid'] = user1.id
            return redirect('/books')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['username'] = logged_user.first_name
            request.session['userid'] = logged_user.id
            return redirect('/books')
        else:
            messages.error(request, 'Invalid email or password')
        return redirect('/')
    messages.error(request, 'Invalid email or password')   
    return redirect('/')

def books(request):
    if 'username' not in request.session:
        return redirect ('/')
    context = {
        'all_books': Book.objects.all(),
    }
    return render (request, 'login_books.html', context)

def add_book(request):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/books')
    #else:
    num = request.session['userid']
    this_user = User.objects.get(id=num)
    new_book = Book.objects.create(
        title=request.POST['title'], 
        desc=request.POST['desc'],
        uploaded_by= this_user,
        )
    this_user.liked_books.add(new_book)
    return redirect('/books')

def book_details(request, number):
    context = {
        'all_books' : Book.objects.all(),
        'this_book': Book.objects.get(id=number),
        'uploader': Book.objects.get(id=number).uploaded_by,
        'logged_user': User.objects.get(id=request.session['userid'])
    }
    return render (request, 'book_details.html', context)

def edit_book(request, number):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/books/{number}')
    #else:
    this_book = Book.objects.get(id=number)
    this_book.title = request.POST['title']
    this_book.desc = request.POST['desc']
    this_book.save()
    return redirect('/books')

def add_likes(request, number):
    this_user = User.objects.get(id=request.session['userid'])
    book = Book.objects.get(id=number)
    this_user.liked_books.add(book)
    return redirect(f'/books/{number}')

def remove_book(request, number):
    this_user = User.objects.get(id=request.session['userid'])
    this_book = Book.objects.get(id=number)
    this_user.liked_books.remove(this_book)
    return redirect(f'/books/{number}')

def delete_book(request, number):
    book = Book.objects.get(id=number)
    book.delete()
    return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')


        
# Create your views here.


