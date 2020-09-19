from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from core.models import Item, Order, Coupon  # , OrderItem


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    add_to_cart_url = serializers.CharField(
        source='get_add_to_cart_url', read_only=True)
    download_url = serializers.CharField(
        source='get_download_url', read_only=True)

    class Meta:
        model = Item
        fields = ('__all__')

# class OrderItemSerializer(serializers.ModelSerializer):
#     item = ItemSerializer(many=True)
#     class Meta:
#         model = OrderItem
#         fields = ('__all__')


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    total = serializers.CharField(source='get_total', read_only=True)
    total_items = serializers.CharField(
        source='get_total_items', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # ('user','ref_code','items','start_date','ordered_date',
        #         'ordered','coupon','purchased','refund_requested',
        #     'refund_granted',)
        depth = 1
