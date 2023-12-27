from .models import Item, Order, FeedBack, ItemImage
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import ItemForm


def home(request: HttpRequest):
    return render(request, 'shopapp/home.html')


class ShopListView(ListView):
    template_name = 'shopapp/shop-list.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(archived=False)


class ItemDetailsView(DetailView):
    template_name = 'shopapp/item-details.html'
    context_object_name = 'item'
    queryset = Item.objects.prefetch_related('images')

    def get_queryset(self):
        return Item.objects.prefetch_related('images', 'feedbacks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = FeedBack.objects.filter(item=context['item'])
        return context


class ProductUpdateView(UpdateView):
    model = Item
    template_name_suffix = '_update_form'
    form_class = ItemForm

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ItemImage.objects.create(
                product=self.object,
                image=image
            )
        return response


class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('shopapp:shop-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ItemImage.objects.create(
                product=self.object,
                image=image
            )
        return response


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
