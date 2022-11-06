from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Seller(models.Model):
    name = models.CharField(max_length=64)

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField() #maybe it is beter to use models.IntegerField
    imageURL = models.URLField()
    category = models.ManyToManyField(Category, blank=True, related_name="category")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

