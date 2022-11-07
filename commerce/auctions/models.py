from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField() # maybe it is beter to use models.IntegerField
    imageURL = models.URLField()
    category = models.ManyToManyField(Category, blank=True, related_name="category")

    def __str__(self):
        return f"{self.title}"