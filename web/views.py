from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from web.cart import Cart
from web.models import Product, Category
from django import views
from django.views.generic import DetailView


class IndexView(views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        cart = Cart(self.request)
        cart_items_count = len(cart)  # Получаем количество товаров в корзине
        for category in categories:
            category.product_dict = self.get_category_products(category)
        context = {
            'categories': categories,
            'cart_items_count': cart_items_count
        }
        return render(request, 'menu.html', context)

    def get_category_products(self, category):
        category_products = category.products()
        total_products = len(category_products)
        half = total_products // 2
        left_products = category_products[:half + (total_products % 2)]
        right_products = category_products[half + (total_products % 2):]
        return {
            'left': left_products,
            'right': right_products,
        }

class CategoryDetailView(views.generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        products = Product.objects.filter(category=category)
        total_products = len(products)
        half = total_products // 2
        left_products = products[:half + (total_products % 2)]
        right_products = products[half + (total_products % 2):]
        cart = Cart(self.request)
        cart_items_count = len(cart)  # Получаем количество товаров в корзине
        context['cart_items_count'] = cart_items_count
        context['left_products'] = left_products
        context['right_products'] = right_products
        subcategories = category.subcategories.all()
        subcategories_data = []
        for subcategory in subcategories:
            subcategory_products = Product.objects.filter(category=subcategory)
            subcategory_total_products = len(subcategory_products)
            subcategory_half = subcategory_total_products // 2
            subcategory_left_products = subcategory_products[:subcategory_half + (subcategory_total_products % 2)]
            subcategory_right_products = subcategory_products[subcategory_half + (subcategory_total_products % 2):]
            subcategories_data.append({
                'subcategory': subcategory,
                'left_products': subcategory_left_products,
                'right_products': subcategory_right_products
            })
        context['subcategories_data'] = subcategories_data
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class ProductDetailView(views.generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_url_kwarg = 'product_slug'
    title = 'product_name'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ct_model = self.model().ct_model
        cart = Cart(self.request)
        cart_items_count = len(cart)  # Получаем количество товаров в корзине
        context['cart_items_count'] = cart_items_count
        context['ct_model'] = ct_model
        context['categories'] = Category.objects.all()
        return context


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get('quantity', 1))
    cart.add(product, quantity)
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')

def update_cart(request, product_id):
    cart = Cart(request)
    cart_product_id = request.POST.get('cart_product_id')
    quantity = int(request.POST.get('quantity'))
    cart.update(cart_product_id, quantity)
    return redirect('cart')

def cart(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    categories = Category.objects.all()
    cart_items_count = len(cart)  # Получаем количество товаров в корзине
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price,
                                         'categories': categories, 'cart_items_count': cart_items_count})