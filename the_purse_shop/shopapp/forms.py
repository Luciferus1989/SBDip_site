from django import forms
from django.core import validators
from .models import Item, Order, OrderItem
from django.contrib.auth.models import Group


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = 'item_number', 'name', 'price', 'discount', 'archived', 'preview'

    images = MultipleFileField()


class OrderCreateForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=OrderItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'promocode', 'items']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['items'].queryset = OrderItem.objects.filter(order__customer_name=user)
