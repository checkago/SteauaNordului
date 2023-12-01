from django.db import models
from django.urls import reverse


class Item(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Наименование млд.')
    name_ru = models.CharField(max_length=100, verbose_name='Наименование рус.', blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')
    composition = models.CharField(max_length=250, verbose_name='Состав млд.', blank=True, null=True)
    composition_ru = models.CharField(max_length=250, verbose_name='Состав рус.', blank=True, null=True)
    volume_choice = models.ForeignKey('Volume', on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='Ед. изм')
    volume_1 = models.CharField(max_length=100, verbose_name='Объем/Вес', blank=True)
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
        return reverse('product_detail', kwargs={'category_slug': self.category.slug, 'item_slug': self.slug})


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

    def items(self):
        return Item.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


class Volume(models.Model):
    name = models.CharField(max_length=4, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Ед. изм.'
        verbose_name_plural = 'Единицы имз.'

    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE, verbose_name='Корзина')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'

    def __str__(self):
        return f"Продукт: {self.item.name} для корзины"

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.item.price_1
        super().save(*args, **kwargs)


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem', related_name='carts')
    total_products = models.IntegerField(default=0, verbose_name='Общее количество товаров в корзине')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Общая стоимость')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Итоговая стоимость')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины покупателей'

    def __str__(self):
        return f"Корзина №{self.id}"

    def add_to_cart(self, item_id, quantity):
        item = Item.objects.get(id=item_id)
        cart_product, created = CartItem.objects.get_or_create(cart=self, item=item)
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        self.update_totals()

    def remove_from_cart(self, item_id):
        item = Item.objects.get(id=item_id)
        cart_product = CartItem.objects.get(cart=self, item=item)
        cart_product.delete()
        self.update_totals()

    def update_totals(self):
        cart_products = self.items.all()
        total_quantity = cart_products.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        total_price = cart_products.aggregate(total_price=models.Sum('final_price'))['total_price']
        self.total_products = total_quantity if total_quantity else 0
        self.final_price = total_price if total_price else 0.00
        self.total = self.final_price
        self.save()


