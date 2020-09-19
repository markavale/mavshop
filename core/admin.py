from django.contrib import admin
from .models import Item, Categories, Order, Coupon #OrderItem


def make_refund_accepted(ModelAdmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('user','title','price', 'discount_price', 'is_free', 'item_type', 'downloads','views',
            'category','created_at',)
    prepopulated_fields = {'slug': ('title',)} # new

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','slug',)
    prepopulated_fields = {'slug': ('category_name',)} # new

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'purchased',
                    'refund_requested',
                    'refund_granted',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'coupon'
    ]
    list_filter = ['ordered',
                   'purchased',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Categories, CategoryAdmin)