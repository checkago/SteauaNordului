from django.http import JsonResponse
from django.shortcuts import render, redirect
from decimal import Decimal

from web.models import Item, Category, Cart, CartItem
from django import views
from django.views.generic import DetailView


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            category.item_dict = self.get_category_items(category)
        context = {
            'categories': categories,
        }
        return render(request, 'menu.html', context)

    def get_category_items(self, category):
        category_items = category.items()
        total_items = len(category_items)
        half = total_items // 2
        left_items = category_items[:half + (total_items % 2)]
        right_items = category_items[half + (total_items % 2):]
        return {
            'left': left_items,
            'right': right_items,
        }

class CategoryDetailView(views.generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_context_data(self, category_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object_or_404(Category, slug=category_slug)
        items = Item.objects.filter(category=category)
        total_items = len(items)
        half = total_items // 2
        left_items = items[:half + (total_items % 2)]
        right_items = items[half + (total_items % 2):]
        context['left_items'] = left_items
        context['right_items'] = right_items

        subcategories = category.subcategories.all()
        subcategories_data = []
        for subcategory in subcategories:
            subcategory_items = Item.objects.filter(category=subcategory)
            subcategory_total_items = len(subcategory_items)
            subcategory_half = subcategory_total_items // 2
            subcategory_left_items = subcategory_items[:subcategory_half + (subcategory_total_items % 2)]
            subcategory_right_items = subcategory_items[subcategory_half + (subcategory_total_items % 2):]
            subcategories_data.append({
                'subcategory': subcategory,
                'left_items': subcategory_left_items,
                'right_items': subcategory_right_items
            })

        context['subcategories_data'] = subcategories_data

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

class AddToCartView(views.View):
    def post(self, request, category_slug, item_slug):
        quantity = int(request.POST.get('quantity', 1))
        category = Category.objects.get(slug=category_slug)
        item = Item.objects.get(category=category, slug=item_slug)
        cart, created = Cart.objects.get_or_create()
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += int(quantity)  # Преобразуем значение в int перед выполнением операции
            cart_item.save()
        cart.total += Decimal(str(item.price_1)) * int(quantity)  # Преобразуем значение в Decimal перед выполнением операции
        cart.save()
        response_data = {
            'message': 'Товар успешно добавлен в корзину.'
        }
        return redirect('cart')

class CartView(views.View):
    def get(self, request):
        cart = Cart.objects.first()
        cart_items = cart.items.all()
        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
        return render(request, 'cart.html', context)


