from django.urls import reverse
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify # new
from taggit.managers import TaggableManager

User = settings.AUTH_USER_MODEL

ITEM_TYPE = [
    ('Photoshop', 'Photoshop'),
    ('Lightroom', 'Lightroom'),
]

# Create your models here.
class Item(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    title               = models.CharField(max_length=255, blank=False, null=False)
    slug                = models.SlugField(unique=True, max_length=255, null=False)
    description         = models.TextField(max_length=1000, blank=True, null=True)
    old_img             = models.ImageField(upload_to='shop', blank=True, null=True)
    new_img             = models.ImageField(upload_to='shop')
    price               = models.IntegerField(default=0, blank=True, null=True)
    discount_price      = models.IntegerField(blank=True, null=True)
    is_free             = models.BooleanField(blank=False, null=False)
    item_type           = models.CharField(max_length=255, choices=ITEM_TYPE)
    is_ordered          = models.BooleanField(default=False)
    download_file       = models.FileField(upload_to='files')
    downloads           = models.PositiveIntegerField(default=0)
    views               = models.PositiveIntegerField(default=0)
    category            = models.ForeignKey('Categories',on_delete=models.CASCADE,related_name='item_categories')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    tags                = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("item-update", kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse("item-delete", kwargs={"slug":self.slug})

    def get_file_name(self):
        return self.download_file.name.split('/')[-1]

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart', kwargs={
            'slug':self.slug
        })

    def get_download_url(self):
        return reverse('core:download-file', kwargs={
            'slug':self.slug
        })

    def get_total_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Categories(models.Model):
    category_name = models.CharField(max_length=255, blank=False, null=False)
    slug            = models.SlugField(unique=True, max_length=255)
    featured_image = models.ImageField(upload_to='featured_image',default='featured_image/default.jpg')
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    def get_featured_image(self):
        image = self.featured_image
        if image and hasattr(image, 'url'):
            return image.url
        else:
            return '/media/featured_image/default.jpg'

    def get_total_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_amount_saved(self):
        if self.discount_price:
            return self.price - self.discount_price
        return None

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

# class OrderItem(models.Model):
#     user        = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_ordered  = models.BooleanField(default=False)
#     item        = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')

#     def __str__(self):
#         return f"{ self.user.username }'s order: {self.item.title}"

#     def get_total_price(self):
#         if self.item.discount_price:
#             return self.item.discount_price
#         return self.item.price

#     def get_amount_saved(self):
#         if self.item.discount_price:
#             return self.item.price - self.item.discount_price
#         return None

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.item.discount_price * self.quantity
    #     else:
    #         return self.item.price * self.quantity

class Order(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code                = models.CharField(max_length=20, blank=True, null=True)
    items                   = models.ManyToManyField(Item)
    start_date              = models.DateTimeField(auto_now_add=True)
    ordered_date            = models.DateTimeField()
    ordered                 = models.BooleanField(default=False)
    # shipping_address        = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL,
    #     blank=True, null=True)
    # billing_address         = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL,
    #     blank=True, null=True)
    # payment                 = models.ForeignKey('Payment', on_delete=models.SET_NULL,
    #     blank=True, null=True)   
    coupon                  = models.ForeignKey('Coupon', on_delete=models.SET_NULL,
        blank=True, null=True) 
    # being_delivered         = models.BooleanField(default=False)
    purchased               = models.BooleanField(default=False)
    refund_requested        = models.BooleanField(default=False)
    refund_granted          = models.BooleanField(default=False)

    '''
    1. Added Item to cart
    2. adding a billing address
    (Failed to checkout)
    3. Payment form
    (Preprocessing, processing, packaging, etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        if self.coupon:    
            total -= self.coupon.amount
        return total
    
    def get_total_items(self):
        return self.items.count()


class Coupon(models.Model):
    code            = models.CharField(max_length=255)
    amount          = models.FloatField()

    def __str__(self):
        return self.code