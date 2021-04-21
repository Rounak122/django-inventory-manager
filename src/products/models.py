from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator

# Create your models here.


def get_product_image_filepath(self, filename):
    return f'products/{self.owner.pk}/{self.id}.png'


def get_prduct_default_image_filepath():
    return 'qr_thumbnail_24dp.svg'


class Product(models.Model):

    name = models.CharField(verbose_name="product name", max_length=100)
    code = models.CharField(verbose_name="product code",
                            max_length=100, null=True, blank=True)
    price = models.CharField(verbose_name="product price",
                             max_length=10, null=True, blank=True)
    currency = models.CharField(
        verbose_name="currency", max_length=10, null=True, blank=True)
    image = models.ImageField(verbose_name="image path", upload_to=get_product_image_filepath,
                              null=True, blank=True, default=get_prduct_default_image_filepath)
    quantity = models.IntegerField(verbose_name="product quantity", validators=[
                                   MinValueValidator(limit_value=0, message='Invalid quantity')])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name="owner", on_delete=models.CASCADE)
    date_added = models.DateTimeField(
        verbose_name="Date-Time added", auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name="Date-Time updated", auto_now=True)
    qr_code = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Product)
def _post_save_receiver(sender, instance, **kwargs):
    instance.image.delete(False)


# qr_code will store-> {"product_name"="myproductname","product_code", "owner"="Rounak", "price" = "Rs. 800"}
# QR CHANGES WITH CHANGE IN ANY OF THE ABOVE
