from django.shortcuts import render
from . models import Item, Categories, Order#, OrderItem


def lightroom_view(request):
    template_name = 'core/lightroom/lightroom-preset.html'
    presets = Item.objects.filter(item_type="Lightroom").order_by('-created_at')
    context = {
        'presets':presets,
    }
    return render(request, template_name, context)

def photoshop_view(request):
    template_name = 'core/photoshop/photoshop.html'
    templates = Item.objects.filter(item_type="Photoshop").order_by('-created_at')
    context = {
        'templates':templates,
    }
    return render(request, template_name, context)


def cart_quick_view(request):
    carts = Order.objects.filter(ordered=False)
    template_name = 'header.html'
    print(carts)
    context = {
        "carts":carts,
    }
    return render(request, template_name, context)

    