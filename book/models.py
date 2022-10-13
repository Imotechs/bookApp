from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    photo = models.ImageField(null = True,blank = True)

# def save(self):
#     img = Image.open(self.image.path)
#     if img.height > 300 or img.width >300:
#         imageparam = (300, 300)
#         img.thumbnail(imageparam)
#         return img.save(self.photo.path)
        


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
