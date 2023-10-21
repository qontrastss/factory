import time

from django.contrib import admin

from orders.models import Order, AttachmentOrder
from orders.tasks import process_order


class AttachmentsInline(admin.TabularInline):
    model = AttachmentOrder


class OrderAdmin(admin.ModelAdmin):

    model = Order

    inlines = (AttachmentsInline,)

    list_display = ('code', 'title', 'user', 'order_status',
                    'created_at')
    fieldsets = (
        (None, {'fields': ('code', 'title', 'user', 'order_status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('code', 'title', 'user', 'order_status')}
         ),
    )
    search_fields = ('code', 'title')
    ordering = ('code',)

    actions = ['process_order',]

    def process_order(self, request, queryset):
        for i in queryset:
            print(i)
            print("-------------------------------------------")
            process_order.delay(order_code=i.code)
            print("********************************************")
            print("ended")


admin.site.register(Order, OrderAdmin)