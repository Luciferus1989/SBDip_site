from django.urls import path, include
from .views import home, ShopListView

app_name = 'shopapp'

urlpatterns = [
    path('', home, name='home'),
    path('shop/', ShopListView.as_view(), name='shop_list'),
]
