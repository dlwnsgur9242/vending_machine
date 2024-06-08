브랜드	상품명	구매가	수량	금액


def view_cart(request):
    cart_session_id = request.session.get('cart_session_id')
    cart_items, total_product_payment, delivery_fee, total_payment = get_cart_items(cart_session_id)

    selected_items = []
    select_all = False

    if request.method == 'POST':
        action = request.POST.get('action')
        select_all = 'select_all' in request.POST
        selected_items = request.POST.getlist('cart_num')
        
        if select_all:
            selected_items = [str(item.id) for item in cart_items]
        
        handle_cart_post_action(action, request, selected_items)
        return redirect('vending_app:view_cart')

    context = {
        'cart_items': cart_items,
        'total_product_payment': total_product_payment,
        'delivery_fee': delivery_fee,
        'total_payment': total_payment,
        'selected_items': selected_items,
        'select_all': select_all,
    }
    return render(request, 'main/view_cart.html', context)

def handle_cart_post_action(action, request, selected_items):
    if action == 'delete_selected':
        Cart.objects.filter(id__in=selected_items).delete()
    elif action == 'delete_all':
        Cart.objects.all().delete()
    elif action == 'select_buy':
        # 선택 상품 구매 처리 로직 (구현 필요)
        pass
    elif action == 'all_buy':
        # 전체 상품 구매 처리 로직 (구현 필요)
        pass




######
# 장바구니 보기
def view_cart(request):
    cart_session_id = request.session.get('cart_session_id')
    cart_items, total_product_payment, delivery_fee, total_payment = get_cart_items(cart_session_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_items = request.POST.getlist('cart_num')

        if action == 'select_buy':
            handle_cart_post_action(action, request, selected_items)
            return redirect('vending_app:orderPayment', selected_items=selected_items)

    context = {
        'cart_items': cart_items,
        'total_product_payment': total_product_payment,
        'delivery_fee': delivery_fee,
        'total_payment': total_payment,
    }
    return render(request, 'main/view_cart.html', context)


# 주문 결제
def orderPayment(request):
    selected_items = request.GET.getlist('selected_items')  # 선택된 상품 리스트 가져오기
    cart_items = Cart.objects.filter(id__in=selected_items)

    total_product_payment = sum(item.total_price() for item in cart_items)
    delivery_fee = 3000  # 배송비
    total_payment = total_product_payment + delivery_fee

    if request.method == 'POST':
        # 여기에 결제 처리 로직을 추가해야 합니다.
        # 사용자가 결제를 완료하면, 주문 정보를 생성하고 장바구니를 비워야 합니다.
        # 이후에 주문 완료 페이지로 리다이렉트하면 됩니다.
        return redirect('vending_app:order_completed')  # 주문 완료 후의 페이지로 리다이렉트

    context = {
        'cart_items': cart_items,
        'total_product_payment': total_product_payment,
        'delivery_fee': delivery_fee,
        'total_payment': total_payment,
    }
    return render(request, 'main/orderPayment.html', context)



 #주문 결제 페이지DB

# order 테이블

주문 번호,
주문한 상품,
주문 수량,
결제 종류(카드, 현금),
결제 금액,
주문 날짜 및 시간,



# OrderItem 테이블

order table
주문 번호,
주문한 상품,
주문 수량,
결제 종류(카드, 현금),
결제 금액,
주문 날짜 및 시간,



class Order(models.Model):
    PAYMENT_CHOICES = [
        ('card', '카드'),
        ('cash', '현금'),
    ]

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_qty = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 결제 금액 계산: 주문 수량 * 상품 가격
        self.payment_amount = self.order_qty * self.product.product_price
        super().save(*args, **kwargs)



## 결제
# 선택(현금 결제/카드 결제)
# 현금 선택시 (제한조건 - 천원, 오천원, 만원 가능, 오만원 불가)
# 1000, 5000, 10000 넣는 수량을 각각 입력 시킨다.(총 입금 금액 계산 로직 필요.)
# 현금 선택시 / 거스름돈 / (제한조건 - 거스룸돈은 100원, 500원, 1000원 가능)
# 1000원>500원>100원 순서로 거스름 돈을 출력한다.
#( ex)거스름돈 5700원 = 1000원 5장, 500원 1개, 100원 2개 )


#필요한 것
#결제 선택
#현금 결제/카드 결제를





#table 
#결제 방식 선택(현금/카드)
# 1000 수량
# 5000 수량
# 10000 수량
# 총 입금한 금액





##결제방식(현금/카드) 선택
##결제방식에 맞는 화면 출력
##현금일 시 금액 입력
##


# Receipt 테이블
## 총 입금 금액 = total_deposit
## 총 거스름 돈 =


#결제하기를 누르면 결제 완료 

## 결제한 상품 목록을 저장해 놓아야한다.
## 테이블을 하나 만들어서 보관(비휘발성) or order table 출력(휘발성)


# 주문 완료 페이지
# {{ order.receipt.payment_type }} 연결 필요.
# views.py의 def orderComplete(request): 수정
# orderComplete 부분 수정 필요


#구현의 어려움
#상세페이지 
#수량 증가 및 바로구매로직