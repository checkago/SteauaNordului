from django.contrib import admin
from web.models import Item, Category, Volume


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category')
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('name',)



