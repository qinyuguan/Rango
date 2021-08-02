from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify


class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class BookDetail(models.Model):
    MAX_LENGTH = 256
    title = models.CharField(max_length=MAX_LENGTH)
    author = models.CharField(max_length=MAX_LENGTH,default="author")
    img = models.URLField()
    publisher = models.CharField(max_length=MAX_LENGTH)
    price = models.CharField(max_length=MAX_LENGTH)
    publish_date = models.CharField(max_length=MAX_LENGTH)
    language = models.CharField(max_length=MAX_LENGTH)
    book_type = models.CharField(max_length=MAX_LENGTH)
    ISBN = models.CharField(max_length=MAX_LENGTH)

    # TODO- category, reviews, desc
    # category = ""
    # reviews = []

    # def __init__(self, title, img, publisher, price, publish_date, language, book_type, ISBN):
    #     self.title = title
    #     self.img = img
    #     self.price = price
    #     self.publisher = publisher
    #     self.publish_date = publish_date
    #     self.language = language
    #     self.book_type = book_type
    #     self.ISBN = ISBN

    def __str__(self):
        return self.title
    #     return json.dump({
    #         'title': title,
    #         'img': img,
    #         'publisher': publisher,
    #         'publish_date': publish_date,
    #         'language': language,
    #         'book_type': book_type,
    #         'ISBN': ISBN,
    #         'price': price
    #     })
