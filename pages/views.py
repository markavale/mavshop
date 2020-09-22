from django.shortcuts import render
from django.conf import settings
from users.models import User
import random
import string
# User = settings.AUTH_USER_MODEL

def create_random_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    if request.method == "GET":
        ip = visitor_ip_address(request)
        print(ip)
        test_user = User.objects.all()
        for test in test_user:
            print(test.id)
            print(test.username)
            print(test.password)
        users = User.objects.filter(ip_address=ip)
        username = create_random_username()
        if not users.exists():
            #user = users[0]
            user = User.objects.create(
                ip_address = ip,username=username,
                email="none", first_name="none", last_name="none"
            )
        else:
            print("User Exists Already")
    return render(request, 'pages/index.html')

def cart_view(request):
    return render(request, 'pages/cart.html')

