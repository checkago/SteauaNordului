from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path
from web.views import IndexView, CategoryDetailView, ItemDetailView, CartView, AddToCartView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('cart/', CartView.as_view(), name='cart'),
    path('<str:category_slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('<str:category_slug>/<str:item_slug>/', ItemDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<str:category_slug>/<str:item_slug>/', AddToCartView.as_view(), name='add_to_cart'),

]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
