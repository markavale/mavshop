from django.shortcuts import HttpResponse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# , OrderItemSerializer
from . serializers import OrderSerializer, ItemSerializer, CouponSerializer
from core.models import Item, Order, Coupon  # , OrderItem
from .permissions import AllowPost, ReadOnly, IsMemberOrIpAddressOnly

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsMemberOrIpAddressOnly, ])
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == "GET":
        queryset = Order.objects.filter(user=request.user, ordered=False)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    # elif request.method == "DELETE":
    #     obj.delete()
    #     data = {}
    #     data['Delete'] = "Success"
    #     return Response(data)


@permission_classes([AllowAny, ])
@api_view(['GET', ])
def get_extra_order(request):
    if request.method == "GET":
        get_items = []
        lightroom_items = Item.objects.filter(
             is_free=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if orders.exists():
            order_qs = orders[0]
            for item in lightroom_items:
                if item in order_qs.items.all():
                    pass
                    print(item)
                else:
                    get_items.append(item)
                    print(get_items)
            serializer = ItemSerializer(get_items, many=True)
            return Response(serializer.data)


@permission_classes([AllowAny, ])
@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == "GET":
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsMemberOrIpAddressOnly,])
@api_view(['GET', 'POST'])
def lightroom_list(request):
    if request.method == "GET":
        queryset = Item.objects.filter(item_type="Lightroom")
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsMemberOrIpAddressOnly,])
@api_view(['GET', 'POST'])
def photoshop_list(request):
    if request.method == "GET":
        queryset = Item.objects.filter(item_type="Photoshop")
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)


def download_view(request, slug):
    item = Item.objects.get(slug=slug)
    filename = item.download_file.name.split('/')[-1]
    response = HttpResponse(item.download_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    item.downloads += 1
    item.save()

    return response


@permission_classes([AllowAny, ])
@api_view(['GET', ])
def add_to_cart(request, slug):
    item = Item.objects.get(slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    data = {}
    if order_qs.exists():
        order = order_qs[0]
        item_in_cart = False
        for obj in order.items.all():
            if obj.slug == item.slug:
                item_in_cart = True
            else:
                item_in_cart = False
        if item_in_cart:
            data['message'] = "{} was already in cart.".format(item.title)
            return Response(data)
        else:
            order.items.add(item)
            data['message'] = "{} was added to your cart.".format(item.title)
            return Response(data)
    else:
        ordered_date = timezone.now()
        order, created = Order.objects.get_or_create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(item)
        order.save()
        data['message'] = "{} was added to your cart.".format(item.title)
        print("{} was added to your cart".format(item.title))
    return Response(data)


class AddCouponView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, code):
        coupon = get_object_or_404(Coupon, code=code)
        if coupon is None:
            return Response({"message": "Invalid data received"}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        order.coupon = coupon
        order.save()
        return Response(status=status.HTTP_200_OK)


@permission_classes([AllowAny, ])
@api_view(['GET', ])
def remove_to_cart(request, slug):
    item = Item.objects.get(slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    data = {}
    if order_qs.exists():
        order = order_qs[0]
        order.items.remove(item)
        data['message'] = "{} was removed from your cart.".format(
            item.title)
        return Response(data)
    else:
        data['message'] = "You do not have an active order."
        print("{} was not in your cart".format(item.title))
    return Response(data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE', ])
def order_detail(request, slug):
    try:
        item = Item.objects.get(slug=slug)
        data = {}
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ItemSerializer(item, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['update'] = "update successful"
            return Response(data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['update'] = "update successful"
            return Response(data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        item.delete()
        data['delete'] = "delete successful"
        return Response(data)
