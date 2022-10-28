from django.db import models
from django.urls import reverse


class Item(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Наименование млд.')
    name_ru = models.CharField(max_length=100, verbose_name='Наименование рус.', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')
    composition = models.CharField(max_length=100, verbose_name='Состав млд.', blank=True)
    composition_ru = models.CharField(max_length=100, verbose_name='Состав рус.', blank=True)
    volume_1 = models.CharField(max_length=100, verbose_name='Объем/Вес')
    price_1 = models.FloatField(verbose_name='Цена')
    volume_2 = models.CharField(max_length=100, verbose_name='Объем/Вес', blank=True, null=True)
    price_2 = models.FloatField(verbose_name='Цена', blank=True, null=True)
    image = models.ImageField(upload_to='media/images', verbose_name='Фото')

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name

    @property
    def ct_model(self):
        return self._meta.model_name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'item_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории меню'

    def __str__(self):
        return self.name

    def items(self):
        return Item.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


