from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import Item, Order, ItemImage
from .admin_mixins import ExportAsCSVMixin
from .forms import ItemForm


class OrderInLine(admin.StackedInline):
    model = Item.orders.through


class ItemInLine(admin.StackedInline):
    model = ItemImage


@admin.action(description='Archived products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Re-archived products')
def remark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.action(description='Set discount 10 percent')
def set_discount_10(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=10)


@admin.action(description='Set discount 5 percent')
def set_discount_5(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=5)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = 'item_number', 'name', 'price', 'discount', 'description_short', 'archived'
    ordering = 'item_number',
    search_fields = 'name',
    form_class = ItemForm
    inlines = [
        OrderInLine,
        ItemInLine,
    ]
    fieldsets = [
        (None, {
            'fields': ('item_number', 'name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount',),
            'description': 'The Price is specified in $',
        }),
        ('Images', {
            'fields': ('preview',),
        }),
    ]
    actions = [
        mark_archived,
        remark_archived,
        set_discount_5,
        set_discount_10,
        'export_csv',
    ]




class ItemInLine(admin.StackedInline):
    model = Order.items.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'user_verbose', 'created_at', 'promocode'
    inlines = [
        ItemInLine,
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('customer_name').prefetch_related('items')

    def user_verbose(self, obj: Order) -> str:
        return obj.customer_name.first_name or obj.customer_name.username
