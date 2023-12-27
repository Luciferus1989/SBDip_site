from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import Item, Order, ItemImage, OrderItem
from .admin_mixins import ExportAsCSVMixin
from .forms import ItemForm


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


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = 'item_number', 'name', 'price', 'discount', 'description_short', 'archived'
    ordering = 'item_number',
    search_fields = 'name',
    form_class = ItemForm
    inlines = [
        OrderItemInLine,
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


@admin.action(description='Archived orders')
def mark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='archived')


@admin.action(description='Re-archived orders')
def remark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='archived')


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'customer_name', 'created_at', 'promocode', 'status'
    inlines = [
        OrderItemInLine,
    ]
    actions = [
        mark_archived_order,
        remark_archived_order,
        'export_csv',
    ]
    readonly_fields = ('created_at',)
    fieldsets = [
        (None, {
            'fields': ('customer_name', 'created_at'),
        }),
        ('Description', {
            'fields': ('promocode', 'delivery_address'),
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('customer_name').prefetch_related('items')

    def user_verbose(self, obj: Order) -> str:
        return obj.customer_name.first_name or obj.customer_name.username
