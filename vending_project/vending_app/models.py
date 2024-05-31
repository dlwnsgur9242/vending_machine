from django.db import models
import uuid

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
    cart_session_id = models.CharField(max_length=32)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart')
        ]

    # 각 항목의 총 가격을 표시하고 전체 장바구니의 총 금액 계산
    def total_price(self):
        return self.product.product_price * self.cart_qty
