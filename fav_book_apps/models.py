from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'Provided FIRST NAME must be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Provided LAST NAME must be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = 'Passwords do not match!'
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        return errors

    def book_validator(self, postData):
        errors= {}
        if len(postData['title']) < 1:
            errors['title'] = 'Must provide a TITLE.'
        if len(postData['desc']) < 5:
            errors['desc'] = 'Provided DESCRIPTION must be at least 5 characters.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=275)
    password = models.CharField(max_length=75)
    confirm_pw = models.CharField(max_length=75)
    objects = UserManager()
    #books_uploaded = list of books uploaded by User
    #liked_books = list od books liked by a user

class Book(models.Model):
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_books') #favorites
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# Create your models here.
