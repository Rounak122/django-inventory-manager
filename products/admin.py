from django.contrib import admin
from products.models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'code', 'name',
                    'currency', 'price', 'quantity')
    # search_fields = ('owner', 'code', 'name')
    readonly_fields = ('date_added', 'date_updated')


admin.site.register(Product, ProductAdmin)
# admin.site.register(Product)
