from django.contrib.sessions.models import Session
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Наименование млд.')
    name_ru = models.CharField(max_length=100, verbose_name='Наименование рус.', blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')
    composition = models.CharField(max_length=250, verbose_name='Состав млд.', blank=True, null=True)
    composition_ru = models.CharField(max_length=250, verbose_name='Состав рус.', blank=True, null=True)
    volume_choice = models.ForeignKey('Volume', on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='Ед. изм')
    volume_1 = models.CharField(max_length=100, verbose_name='Объем/Вес', blank=True, null=True)
    price_1 = models.FloatField(verbose_name='Цена')
    volume_2 = models.CharField(max_length=100, verbose_name='Объем/Вес', blank=True, null=True)
    price_2 = models.FloatField(verbose_name='Цена', blank=True, null=True)
    image = models.ImageField(upload_to='media/images', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name

    @property
    def ct_model(self):
        return self._meta.model_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                        related_name='subcategories', verbose_name='Родительская категория')
    icon = models.ImageField(upload_to='media/category_icons', blank=True, null=True, verbose_name='Иконка')
    foto = models.ImageField(upload_to='media/category_fotos', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории меню'

    def __str__(self):
        return self.name

    def products(self):
        return Product.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


class Volume(models.Model):
    name = models.CharField(max_length=4, blank=True, null=True, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Ед. изм.'
        verbose_name_plural = 'Единицы имз.'

    def __str__(self):
        return self.name








