from django.db import models
import re

class UserManager(models.Manager):
    def reg_validator(self,postData):
        reg_errors = {}
        if len(postData['firstname']) < 2:
            reg_errors["firstname"] = "First Name must be at least 2 characters"
        if len(postData['lastname']) < 2:
            reg_errors["lastname"] = "Last Name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            reg_errors["email"] = "Invalid Email Address"
        if len(postData['password']) < 8:
            reg_errors["password"] = "Password must be at least 8 characters"
        if postData['password'] != postData['passwordconf']:
            reg_errors["passwordconfirm"] = "Passwords do not match"
        all_users = User.objects.all()
        for u in all_users:
            if u.email == postData['email']:
                reg_errors["duplicate_email"] = "User account already exists with this email"
        return reg_errors
    
    def login_validator(self,postData):
        log_errors = {}
        if len(postData['email']) < 1:
            log_errors["email_length"] = "Email Required"
        if len(postData['password']) < 1:
            log_errors["password"] = "Password Required"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            log_errors["email"] = "Invalid Email Address"
        user = User.objects.get(email=postData['email'])
        return log_errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
# Create your models here.
