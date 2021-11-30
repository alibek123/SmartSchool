from django.db import models
from PIL import Image, ImageOps
from io import BytesIO

from django.core.files import File

# Create your models here.
from django.http import HttpRequest


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Meal(models.Model):
    productID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='')
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='meals', on_delete=models.CASCADE)

    # if needs category name add to_field='name', db_column='category',

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            ss = HttpRequest.get_full_path
            return f'http://192.168.1.39' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://192.168.1.39' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://192.168.1.39' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size, Image.ANTIALIAS)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
