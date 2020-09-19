from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')

def cart_view(request):
    return render(request, 'pages/cart.html')