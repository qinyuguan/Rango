from django.contrib.auth.models import User
from django.db import models
from uuid import uuid1, uuid4
from shortuuidfield import ShortUUIDField

# Create your models here.
from django.template.defaultfilters import slugify


class Category(models.Model):
    NAME_MAX_LENGTH = 4096
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class BookDetail(models.Model):
    MAX_LENGTH = 256
    title = models.CharField(max_length=MAX_LENGTH, unique=True)
    author = models.CharField(max_length=MAX_LENGTH, default="author")
    img = models.URLField()
    publisher = models.CharField(max_length=MAX_LENGTH)
    price = models.CharField(max_length=MAX_LENGTH)
    publish_date = models.CharField(max_length=MAX_LENGTH)
    language = models.CharField(max_length=MAX_LENGTH)
    book_type = models.CharField(max_length=MAX_LENGTH)
    ISBN = models.CharField(max_length=MAX_LENGTH)
    slug = models.SlugField(blank=True, unique=True)
    desc = models.CharField(max_length=8192, default="")
    category = models.CharField(max_length=8192, default="")
    categories = models.ManyToManyField(Category)

    # TODO- category, reviews, desc
    # category = ""
    # reviews = []
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BookDetail, self).save(*args, **kwargs)

    def get_categories(self):
        return self.category.split(";")

    class Meta:
        ordering = ('title',)


class Like(models.Model):
    book = models.OneToOneField(BookDetail, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

class Cart(models.Model):
    user = models.ManyToManyField(User)
    book = models.ManyToManyField(BookDetail)
    num = models.IntegerField(default=1)

    def increment(self):
        self.num = self.num + 1

class Order(models.Model):
    user = models.ManyToManyField(User)
    book = models.ManyToManyField(BookDetail)
    price = models.CharField(max_length=255)
    quantity = models.IntegerField(default=255)
    total_price = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    date = models.DateTimeField()
    isComment = models.IntegerField(default=0)
    order_no = ShortUUIDField(primary_key=False, default=uuid1, editable=False)


class Comment(models.Model):
    content = models.TextField(default="")
    date = models.DateTimeField()
    book = models.ManyToManyField(BookDetail)


