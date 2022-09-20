from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
# from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class New(models.Model):

    STATUS = {
        ('published', 'published'),
        ('draft', 'draft'),
    }

    title = models.CharField(max_length=100)
    body = models.TextField()
    body1 = models.TextField(blank=True, null=True)
    body2 = models.TextField(blank=True, null=True)
    new_img = models.ImageField(upload_to='new_img', blank=True)
    new_img1 = models.ImageField(upload_to='new_img', blank=True)
    new_img2 = models.ImageField(upload_to='new_img', blank=True)
    new_img3 = models.ImageField(upload_to='new_img', blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    views = models.IntegerField(default=0)
    new_author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('new:detail', args=[self.slug])


class Review(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.comment



