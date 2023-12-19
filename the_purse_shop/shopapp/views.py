from .models import Item, Order, FeedBack
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView


def home(request: HttpRequest):
    return render(request, 'shopapp/home.html')


class ShopListView(ListView):
    template_name = 'shopapp/shop-list.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(archived=False)


class ItemDetailsView(DetailView):
    template_name = 'shopapp/item-details.html'
    # queryset = (
    #     Item.objects.prefetch_related('images'),
    #     FeedBack.objects.prefetch_related('item'),
    # )
    context_object_name = 'item'

    def get_queryset(self):
        return Item.objects.prefetch_related('images', 'feedbacks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = FeedBack.objects.filter(item=context['item'])
        return context



class ItemCreate(CreateView):
    model = Item
    fields = 'item_number', 'name', 'description', 'price', 'preview'
    success_url = reverse_lazy('shopapp:shop-list')


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('shopapp:shop-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    template_name = 'shopapp/order-list.html'
    context_object_name = 'orders'
    queryset = Order.objects.all


class OrderDetailsView(DetailView):
    template_name = 'shopapp/order-details.html'
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )
    context_object_name = 'orders'
