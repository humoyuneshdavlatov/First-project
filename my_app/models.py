from django.db import models
# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('publish', 'Publish')
    )

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("blog:post_detal",
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])

    objects = models.Manager()
    published = PublishedManager()

posts = Post.objects.all()
p_posts = Post.published.all()

