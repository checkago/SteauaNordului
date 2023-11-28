from django.shortcuts import render
from web.models import Item, Category
from django import views
from django.views.generic import DetailView


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            category_items = category.items()
            total_items = len(category_items)
            half = total_items // 2
            left_items = category_items[:half + (total_items % 2)]
            right_items = category_items[half + (total_items % 2):]
            category.item_dict = {
                'left': left_items,
                'right': right_items,
            }
        context = {
            'categories': categories,
        }
        return render(request, 'menu.html', context)

class CategoryDetailView(views.generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        items = Item.objects.filter(category=category)
        total_items = len(items)
        half = total_items // 2
        left_items = items[:half + (total_items % 2)]
        right_items = items[half + (total_items % 2):]
        context['left_items'] = left_items
        context['right_items'] = right_items

        categories = Category.objects.all()
        context['categories'] = categories

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
