UUID는 매우 길고 복잡하기 때문에 수동으로 입력하기는 어렵습니다. 
이를 해결하기 위해 사용자가 보다 쉽게 접근할 수 있는 방법을 제공하는 것이 중요합니다. 
다음은 몇 가지 접근 방식입니다.

1. 사용자에게 단순한 주문 번호 제공
각 주문에 대해 사용자 친화적인 고유한 숫자형 주문 번호를 제공하고, 이 번호를 통해 영수증을 조회할 수 있게 합니다.

class Order(models.Model):
    PAYMENT_TYPES = [
        ('card', '카드'),
        ('cash', '현금'),
    ]
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_qty = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_datetime = models.DateTimeField(auto_now_add=True)
    user_friendly_order_id = models.AutoField()  # 사용자 친화적인 주문 번호 추가

    def __str__(self):
        return str(self.user_friendly_order_id)

class Receipt(models.Model):
    receipt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.receipt_id)
    
2. 주문 번호를 통해 영수증 조회
주문 번호를 통해 영수증을 조회하도록 합니다.

from django.shortcuts import render, get_object_or_404
from .models import Receipt, Order

def receipt_detail(request, order_id):
    order = get_object_or_404(Order, user_friendly_order_id=order_id)
    receipt = get_object_or_404(Receipt, order=order)
    user = receipt.user
    product = order.product
    
    context = {
        'receipt_id': receipt.receipt_id,
        'order_id': order.user_friendly_order_id,
        'user_id': user.user_id,
        'user_type': user.get_user_type_display(),
        'product_name': product.product_name,
        'order_qty': order.order_qty,
        'payment_type': order.get_payment_type_display(),
        'order_amount': order.order_amount,
        'order_datetime': order.order_datetime,
        'receipt_datetime': receipt.receipt_datetime,
    }

    return render(request, 'receipt_detail.html', context)
3. URL 설정
URL 설정을 통해 사용자가 주문 번호로 영수증을 조회할 수 있게 합니다.

from django.urls import path
from .views import receipt_detail

urlpatterns = [
    path('receipt/<int:order_id>/', receipt_detail, name='receipt_detail'),
]
4. 사용자 인터페이스에서 주문 번호 제공
사용자에게 주문 번호를 제공하는 인터페이스를 구현합니다. 예를 들어, 주문 완료 후 주문 번호를 사용자에게 표시하고, 이메일이나 문자 메시지로 발송할 수 있습니다.

<!-- 예제: 주문 완료 페이지 -->
<!DOCTYPE html>
<html>
<head>
    <title>Order Confirmation</title>
</head>
<body>
    <h1>Order Confirmation</h1>
    <p>Your order has been placed successfully!</p>
    <p><strong>Your Order Number:</strong> {{ order.user_friendly_order_id }}</p>
    <p>Please save this order number for future reference.</p>
</body>
</html>
이러한 접근 방식을 사용하면 사용자는 복잡한 UUID 대신 간단한 숫자형 주문 번호로 영수증을 조회할 수 있게 됩니다. 
이는 사용자의 편의성을 크게 향상시킬 것입니다.