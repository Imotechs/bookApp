from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.forms import BooleanField

# Create your models here.

     

#books table
class Books(models.Model):
    cover_image = models.ImageField(upload_to = 'media/')
    title = models.CharField(max_length = 50)
    ISBN = models.CharField(max_length = 50)
    revision_number = models.CharField(max_length = 50)
    published_date = models.DateField()
    publisher = models.CharField(max_length = 70)
    author = models.CharField(max_length = 150)
    genre = models.CharField(max_length = 50)
    date_added = models.DateTimeField(auto_now =True)
    def __str__(self):
        return self.title

#calculate the total books in the store
    @property
    def total_books(self):
        return self.objects.all().count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    photo = models.ImageField(default = "default.png",upload_to = 'media/',blank = True )
    books = models.ManyToManyField(Books)
    def __str__(self):
        return self.user.username

#book cheking table
class CheckedBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Books, on_delete = models.CASCADE)
    date_checked = models.DateTimeField(auto_now =True)
    date_due = models.DateTimeField()
    has_returned= models.BooleanField(default=False)
    def __str__(self):
        return self.book.ISBN

