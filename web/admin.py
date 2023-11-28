from django.contrib import admin
from web.models import Item, Category, Volume
from import_export.admin import ImportExportModelAdmin


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category')
    list_filter = ('category',)

    actions = ['duplicate_items']

    def duplicate_items(self, request, queryset):
        for item in queryset:
            # Создаем новый объект с переносом данных полей и пустым значением slug
            new_item = Item(
                category=item.category,
                name=item.name,
                name_ru=item.name_ru,
                slug='',  # Пустое значение slug
                composition=item.composition,
                composition_ru=item.composition_ru,
                volume_choice=item.volume_choice,
                volume_1=item.volume_1,
                price_1=item.price_1,
                volume_2=item.volume_2,
                price_2=item.price_2,
                image=item.image
            )
            new_item.save()

    duplicate_items.short_description = 'Дублировать выбранные элементы'

    def save_model(self, request, obj, form, change):
        # Проверяем, является ли slug пустым
        if not obj.slug:
            obj.slug = ''  # Устанавливаем пустое значение slug
        obj.save()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('name',)



