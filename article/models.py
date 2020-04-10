from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publish_date = models.DateField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True,blank=True, null=True)
    content = models.TextField()
    category = models.CharField(max_length=20)


class Pic(models.Model):
    img = models.ImageField(upload_to='pic')
