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
    product_price = models.IntegerField()
    product_flag = models.CharField(max_length=10)
    product_image = models.ImageField(upload_to='vending_app/static/img/', null=True, blank=True)

class Detail(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    detail_qty = models.PositiveIntegerField(default=1)

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
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_datetime = models.DateTimeField(auto_now_add=True)

    # 각 항목의 총 가격을 표시하고 전체 주문결제의 총 금액 계산
    def order_total_price(self):
        return self.product.product_price * self.order_qty
    
    def __str__(self):
        return str(self.order_id)

class Receipt(models.Model):
    PAYMENT_TYPES = [
        ('card', '카드'),
        ('cash', '현금'),
    ]
    receipt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Order와의 관계 설정
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='receipts')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    #총 결제할 금액
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_datetime = models.DateTimeField(auto_now_add=True)
    
    # 추가 필드: 1000원, 5000원, 10000원 수량
    one_thousand = models.PositiveIntegerField(default=0)
    five_thousand = models.PositiveIntegerField(default=0)
    ten_thousand = models.PositiveIntegerField(default=0)

    # #추가 필드: 총 입금 금액
    # total_deposit
    
    # 총 입금 금액을 계산하는 메소드
    def total_deposit(self):
        return self.one_thousand * 1000 + self.five_thousand * 5000 + self.ten_thousand * 10000

    def __str__(self):
        return str(self.receipt_id)
    
    class Meta:
        get_latest_by = 'receipt_datetime'