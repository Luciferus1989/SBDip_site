from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Item, Order, FeedBack, ItemImage, OrderItem
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import ItemForm, OrderCreateForm


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

    def get_queryset(self):
        return Order.objects.filter(customer_name=self.request.user)


class OrderDetailsView(DetailView, UserPassesTestMixin):
    template_name = 'shopapp/order-details.html'
    model = Order
    context_object_name = 'order'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user or order.is_public

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = self.object.orderitem_set.all()
        total_quantity = sum(item.quantity for item in order_items)
        total_amount = sum(item.item.price * item.quantity for item in order_items)

        context['order_items'] = order_items
        context['total_quantity'] = total_quantity
        context['total_amount'] = total_amount

        return context


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order, created = Order.objects.get_or_create(customer_name=request.user, status='active')
    order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

    if not created:
        order_item.quantity += 1
        order_item.save()
    else:
        order_item.quantity = 1
        order_item.save()

    return redirect('shopapp:item_details', pk=item_id)


@login_required
class OrderCreateView(CreateView):
    template_name = 'shopapp/order_create.html'
    form_class = OrderCreateForm

    def form_valid(self, form):
        form.instance.customer_name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shopapp:order_details', kwargs={'pk': self.object.pk})
