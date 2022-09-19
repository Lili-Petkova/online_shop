from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'recipient', 'email',
                    'address', 'city', 'postal_code', 'created', 'status']
    list_filter = ['created', 'status']
    inlines = [OrderItemInline]
    actions = ["change_status_to_completed"]

    def change_status_to_completed(self, request, queryset):
        queryset.update(status='completed')

    change_status_to_completed.short_description = "Status: completed"


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    list_filter = ['book']


admin.site.register(Order, OrderAdmin)
