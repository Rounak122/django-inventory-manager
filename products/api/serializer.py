from rest_framework import serializers
from products.models import Product
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB


class ProductSerializer(serializers.ModelSerializer):

    # username 		= serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Product
        fields = ['pk', 'name', 'code', 'currency', 'price', 'image',
                  'quantity',  'date_added', 'date_updated', 'qr_code']

    # def get_username_from_author(self, blog_post):
    # 	username = blog_post.author.username
    # 	return username

    def validate_image_url(self, product):
        image = product.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

        def validate(self, product):
            try:
                quantity = product['quantity']
                if quantity < 0:
                    raise serializers.ValidationError(
                        {"response": "Enter Valid Quantity"})

                price = product['price']
                if quantity < 0:
                    raise serializers.ValidationError(
                        {"response": "Enter Valid Price"})

                image = product['image']
                url = os.path.join(settings.TEMP, str(image))
                storage = FileSystemStorage(location=url)

                with storage.open('', 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()

                if os.path.getsize(img_url) > IMAGE_SIZE_MAX_BYTES:
                    os.remove(url)
                    raise serializers.ValidationError(
                        {"response": "That image is too large. Images must be less than 3 MB. Try a different image."})

                os.remove(url)
            except KeyError:
                pass
            return product
