from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (home,
                    ShopListView,
                    ItemCreate,
                    ItemDetailsView,
                    add_to_cart,
                    OrderDetailsView,
                    OrderListView)

app_name = 'shopapp'

urlpatterns = [
    path('', home, name='home'),
    path('shop/', ShopListView.as_view(), name='shop_list'),
    path('shop/create', ItemCreate.as_view(), name='item_create'),
    path('shop/<int:pk>/', ItemDetailsView.as_view(), name='item_details'),
    path('shop/<int:item_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
