from django.contrib import admin
from web.models import Product, Category, Volume
from import_export.admin import ImportExportModelAdmin


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category')
    list_filter = ('category',)

    actions = ['duplicate_products']

    def duplicate_products(self, request, queryset):
        for product in queryset:
            # Создаем новый объект с переносом данных полей и пустым значением slug
            new_product = Product(
                category=product.category,
                name=product.name,
                name_ru=product.name_ru,
                slug='',  # Пустое значение slug
                composition=product.composition,
                composition_ru=product.composition_ru,
                volume_choice=product.volume_choice,
                volume_1=product.volume_1,
                price_1=product.price_1,
                volume_2=product.volume_2,
                price_2=product.price_2,
                image=product.image
            )
            new_product.save()

    duplicate_products.short_description = 'Дублировать выбранные элементы'

    def save_model(self, request, obj, form, change):
        # Проверяем, является ли slug пустым
        if not obj.slug:
            obj.slug = ''  # Устанавливаем пустое значение slug
        obj.save()


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(Volume)
class VolumeAdmin(ImportExportModelAdmin):
    list_display = ('name',)




