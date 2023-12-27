from django.contrib.auth.models import User
from django.db import models


def product_preview_directory_path(instance: "Item", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Item(models.Model):
    class Meta:
        ordering = ['name', 'price']

    item_number = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Item price')
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)


    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        else:
            return self.description[:50] + '...'

    def __str__(self) -> str:
        return self.name


def item_image_directory_path(instance: 'ItemImage', filename: str) -> str:
    return 'media/products/product_{pk}/images/{filename}'.format(pk=instance.item.pk, filename=filename,)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=item_image_directory_path)
    description = models.CharField(max_length=100, null=False, blank=True)


class Order(models.Model):
    customer_name = models.ForeignKey(User, on_delete=models.PROTECT)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(Item, related_name='orders')
    # receipt = models.FileField(null=True, upload_to='orders/receipts')


class FeedBack(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='feedbacks')
    customer_name = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_text = models.TextField(max_length=300)
