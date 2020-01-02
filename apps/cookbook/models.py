from django.db import models
from apps.login.models import User

class Family(models.Model):
    family_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.ManyToManyField(User,related_name="member_of_family")

class Category(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        for field_name in ['title']:
            val = getattr(self,field_name,False)
            if val:
                setattr(self,field_name,val.capitalize())
        super(Category, self).save(*args, **kwargs)

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    directions = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="recipe",on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="recipe",on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        for field_name in ['title']:
            val = getattr(self,field_name,False)
            if val:
                setattr(self,field_name,val.capitalize())
        super(Recipe, self).save(*args, **kwargs)

class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comment",on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="comment",on_delete=models.CASCADE)
    
class Message(models.Model):
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="message",on_delete=models.CASCADE)
    family = models.ForeignKey(Family, related_name="message",on_delete=models.CASCADE)

# Create your models here.
