from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    last_login = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    authors = models.ManyToManyField(User, related_name='blogs', blank=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=2048)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, default=None)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    body = models.CharField(max_length=2048)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return str(self.user)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "blog")

    def __str__(self):
        return str(self.user)
