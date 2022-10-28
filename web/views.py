from django.shortcuts import render
from web.models import Item, Category
from django import views
from django.views.generic import DetailView


class IndexView(views.View):
    model = Category

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        items = Item.objects.filter(category=category)
        context = {
            'categories': categories,
            'items': items
        }
        return render(request, 'menu.html', context)


class CategoryDetailView(views.generic.DetailView):
    model = Category
    categories = Category.objects.all()
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        items = Item.objects.filter(category=category)
        context['category_items'] = items
        return context


class ItemDetailView(views.generic.DetailView):
    model = Item
    template_name = 'product_detail.html'
    slug_url_kwarg = 'item_slug'
    title = 'item_name'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ct_model = self.model().ct_model
        context['ct_model'] = ct_model
        context['categories'] = Category.objects.all()
        return context
