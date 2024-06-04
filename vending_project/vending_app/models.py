from django.db import models
import uuid
from django.utils.crypto import get_random_string

def generate_unique_session_id():
    return get_random_string(32)

class User(models.Model):
    USER_TYPES = [
        ('admin', '관리자'),
        ('customer', '손님'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    user_id = models.CharField(max_length=10, unique=True)
    user_pwd = models.CharField(max_length=10, blank=True, null=True)

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=20)
    product_stock = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_flag = models.CharField(max_length=10)
    product_image = models.ImageField(upload_to='vending_app/static/img/', null=True, blank=True)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_qty = models.PositiveIntegerField(default=1)
    cart_session_id = models.CharField(max_length=32, default=generate_unique_session_id)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart')
        ]

    # 각 항목의 총 가격을 표시하고 전체 장바구니의 총 금액 계산
    def total_price(self):
        return self.product.product_price * self.cart_qty
    
class Order(models.Model):
    PAYMENT_TYPES = [
        ('card', '카드'),
        ('cash', '현금'),
    ]
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_qty = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

class Receipt(models.Model):
    receipt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.receipt_id)