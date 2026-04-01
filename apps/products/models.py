from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.managers import ActiveProductManager
from mptt.models import MPTTModel, TreeForeignKey
from django_ckeditor_5.fields import CKEditor5Field

from django.core.cache import cache

from apps.common.models import Media


# Create your models here.

class Category(MPTTModel):
    name = models.CharField(_("name"), max_length=255)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")  # Bo'limlar
        verbose_name_plural = _("Categories")

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    name = models.CharField(_("name"), max_length=255)
    price = models.DecimalField(_("price"),max_digits=10, decimal_places=2, min_value=0)
    short_description = models.TextField(_("short description"))
    description = models.TextField(_("description"))
    quantity = models.IntegerField(_("quantity"))
    instructions = CKEditor5Field(config_name='extends')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    in_stock = models.BooleanField(_("in stock"), default=True)
    brand = models.CharField(_("brand"), max_length=255)
    discount = models.IntegerField(_("discount"), help_text=_("in percentage"))
    thumbnail = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cache.delete("all_products")
        self.category.save()
        super().save(*args, **kwargs)


class ProductColour(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colours")
    colour = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.id}|Colour: {self.colour.id}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.id}|Image: {self.image.id}"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")
    value = models.CharField(_("value"), max_length=255)

    def __str__(self):
        return f"Product: {self.product.id}|Size: {self.value}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    review = models.TextField(_("review"))
    rank = models.IntegerField(_("rank"), validators=[])
    email = models.EmailField(_("email"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.id}|User: {self.user.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_product_review')
        ]


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="wishlists")

    def __str__(self):
        return f"Product: {self.product.id}|User: {self.user.id}"