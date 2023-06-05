from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null =True)
    # bio = models.TextField(null=True)

    # avatar = models.ImageField(null = True, default="avatar.svg")

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Contact_Us(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class CompanyName(models.Model):
    symbol = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'myapp_company'


#models for My-expense--------

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.category

    class Meta:
        ordering= ["-date"]

class Category(models.Model):
    name = models.CharField(max_length=266)

    def __str__(self):
        return self.name
    

# models for market news section

class News(models.Model):
    date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title