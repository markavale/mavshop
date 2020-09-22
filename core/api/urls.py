from django.urls import path
from . views import (order_list, item_list, lightroom_list, photoshop_list,
                    add_to_cart, remove_to_cart,download_view,
                    get_extra_order, AddCouponView
)

urlpatterns = [
    path('add-to-cart/<slug>', add_to_cart,name="add-to-cart"),
    path('add-coupon/<str:code>', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>', remove_to_cart,name="remove-from-cart"),
    path('download/<slug>', download_view,name="download-file"),
    path('cart-list', order_list,name="cart-list"),
    path('extra-items', get_extra_order,name="extra-items"),
    path('item-list', item_list,name="item-list"),
    path('lightroom-list', lightroom_list,name="lightroom-list"),
    path('photoshop-list', photoshop_list,name="photoshop-list"),
    
]
