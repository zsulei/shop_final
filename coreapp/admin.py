from django.contrib import admin
from .models import Product, Client, Categories, Material, Size, Type, Manufacturer, AdminLog
from django.contrib.auth.models import Permission


admin.site.register(Permission)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_staff', )
    search_fields = ('last_name__startswith', )
    fields = ('username', 'last_name', 'first_name', 'avatar', 'activation_code', 'is_staff', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material', )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', )


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('product_type', )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('country', )


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('purchase_date', 'total_price', 'client', 'products_list', )
    list_filter = ('purchase_date', )

    def products_list(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html, urlencode
        url = (reverse('admin:coreapp_product_changelist')
               + '?' + urlencode({'adminlog__id': str(obj.id)}))
        return format_html('<a href="{}">Products</a>', url)
