from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField
from django_prices.models import MoneyField
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = VersatileImageField(
        upload_to="hana-category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    objects = models.Manager()

    class Meta:
        app_label = "hanabackend"
        ordering = ("name",)

    def __str__(self):
        return self.name





class Product(models.Model):
    name = models.CharField(max_length=128)
    IMEI = models.CharField( max_length=128, blank=True )
    name_description_1 = models.CharField(max_length=128,null=True,blank=True)
    name_description_2 = models.CharField(max_length=128,null=True,blank=True)
    price = MoneyField(amount_field="price_amount", currency_field="currency")
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )
    ordering = models.CharField( max_length=16, default="Null" )
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = "hanabackend"
        ordering = ("name",)

    def __iter__(self):
        pass

    def __repr__(self):
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        return super().save(force_insert, force_update, using, update_fields)

    def get_first_image(self):
        images = list(self.images.all())
        return images[0] if images else None




class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="hana-products", ppoi_field="ppoi", blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        app_label = "hanabackend"



class Emarket(models.Model):
    product = models.ForeignKey(
        Product, related_name="Emarkets", on_delete=models.CASCADE
    )
    emarket_url = models.CharField(max_length=128, blank=True)

    class Meta:
        app_label = "hanabackend"


class CollectionProduct(models.Model):
    collection = models.ForeignKey(
        "Collection", related_name="collectionproduct", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="collectionproduct", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("collection", "product"),)

    def get_ordering_queryset(self):
        return self.product.collectionproduct.all()



class Collection(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128)
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="collections",
        through=CollectionProduct,
        through_fields=["collection", "product"],
    )
    background_image = VersatileImageField(
        upload_to="collection-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)


    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:collection", kwargs={"pk": self.id, "slug": self.slug})
