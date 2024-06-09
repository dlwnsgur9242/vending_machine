from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, User, Order, Receipt, Detail
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import ProductRegisterForm, AddToCartForm
from .forms import AddToCartForm
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST

def index(request):
    return render(request, 'main/index.html')


#상품 리스트
def ProductList(request):
    products = Product.objects.all()
    return render(request, 'main/ProductList.html', {'products': products})

# 상품 등록
def productmanage(request):
    if request.method == 'POST':
        #POST 요청이면, 사용자가 제출한 데이터로 폼을 초기화
        #POST 요청이 아닌 경우, 즉 초기 상태에서는 빈 폼을 생성
        form = ProductRegisterForm(request.POST, request.FILES)
        if form.is_valid(): #폼이 유효한지 여부를 확인
            product = form.save(commit=False)
            product.save() #상품을 데이터베이스에 저장
    else:
        form = ProductRegisterForm()

    return render(request, 'main/productmanage.html', {'form': form})

# 상품 상세페이지
def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_qty = form.cleaned_data['cart_qty']
            # Detail 테이블에 해당 상품 정보 추가
            detail = Detail.objects.create(
                product=product,
                detail_qty=cart_qty
            )
            # 주문 생성
            order = Order.objects.create(
                product=product,
                order_qty=cart_qty,
                order_amount=product.product_price * cart_qty
            )
            # 주문 생성 후 주문 결제 페이지로 이동
            return redirect('vending_app:order_payment', order_id=order.pk)
    else:
        form = AddToCartForm()

    cart_qty = request.session.get('cart', {}).get(product_id, 1)
    product.cart_qty = cart_qty

    return render(request, 'main/product_detail.html', {'product': product, 'form': form})

def add_to_detail(request, product_id):
    if request.method == 'POST':
        # POST 요청일 때, 상품 수량을 받아서 주문 생성
        product = get_object_or_404(Product, product_id=product_id)
        qty = int(request.POST.get('qty', 1))  # 클라이언트에서 전송된 수량 값 가져오기

        # 주문 생성
        order = Order.objects.create(
            product=product,
            order_qty=qty,
            order_amount=product.product_price * qty
        )

        # 주문 생성 후 주문 결제 페이지로 이동
        return redirect('vending_app:order_payment', order_id=order.pk)
    else:
        # POST 요청이 아닌 경우, 상품 상세 페이지로 리다이렉트
        return redirect('vending_app:product_detail', product_id=product_id)

def update_detail_qty(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_qty = request.POST.get('new_qty')

        # 상품을 가져옵니다.
        product = get_object_or_404(Product, product_id=product_id)

        # 상품의 수량을 업데이트합니다.
        product.product_stock = new_qty
        product.save()

        # 성공적으로 업데이트되었음을 클라이언트에게 알립니다.
        data = {'message': '상품 수량이 업데이트되었습니다.'}
        return JsonResponse(data)
    else:
        # POST 요청이 아닌 경우 에러 메시지를 반환합니다.
        data = {'error': 'POST 요청이 필요합니다.'}
        return JsonResponse(data, status=400)

# 장바구니 view
def view_cart(request):
    print("준혁")
    cart_session_id = request.session.get('cart_session_id')
    cart_items, total_product_payment, total_payment = get_cart_items(cart_session_id)

    carts = Cart.objects.filter(cart_session_id=cart_session_id)
    count = carts.count()

    if request.method == 'POST':
        action = request.POST.get('action')
        select_all = 'select_all' in request.POST
        selected_items = request.POST.getlist('cart_num')
        
        print("Action:", action)
        print("Select all:", select_all)
        print("Selected items:", selected_items)
        
        if select_all:
            selected_items = [str(item.cart_id) for item in cart_items]
        
        handle_cart_post_action(action, request, selected_items)
        print("설마 여기?")
        print(action)
        if action == 'delete_selected':
            return redirect('vending_app:view_cart')   
        elif action == 'delete_all':
            return redirect('vending_app:view_cart')
        elif action == 'select_buy':
            return redirect('vending_app:orderPayment')
        elif action == 'all_buy':
            return redirect('vending_app:orderPayment')
        print("다미")
    context = {
        'cart_items': cart_items,
        'total_product_payment': total_product_payment,
        'total_payment': total_payment,
        'count': count,
    }
    return render(request, 'main/view_cart.html', context)


# 장바구니 항목 가져오기 및 계산
def get_cart_items(cart_session_id):
    cart_items = Cart.objects.filter(cart_session_id=cart_session_id, user=None)
    total_product_payment = sum(item.total_price() for item in cart_items)
    total_payment = total_product_payment
    #total_price를 계산하는 로직
    for cart_item in cart_items:
        cart_item.total_price = cart_item.cart_qty * cart_item.product.product_price

    return cart_items, total_product_payment, total_payment

# 장바구니 POST 요청 처리
def handle_cart_post_action(action, request, selected_items):
    if selected_items and all(selected_items):  # 선택된 항목이 비어있지 않은지 확인
        if action == 'delete_selected':
            Cart.objects.filter(cart_id__in=selected_items).delete()
        elif action == 'delete_all':
            Cart.objects.all().delete()
        elif action == 'select_buy':
            print("뭉치")
            # 선택 상품 구매 처리 로직
            handle_select_buy(request, selected_items)
        elif action == 'all_buy':
            # 전체 상품 구매 처리 로직
            handle_all_buy(request)
    elif action == 'all_buy': # 선택된 항목이 비어 있어도 실행
            # 전체 상품 구매 처리 로직
            handle_all_buy(request)
    elif action == 'delete_all':
            Cart.objects.all().delete()

# 선택한 상품 구매 처리
def handle_select_buy(request, selected_items):
    # 선택한 상품들을 가져옵니다.
    cart_items = Cart.objects.filter(cart_id__in=selected_items)

    # 각 상품에 대한 주문을 생성합니다.
    for cart_item in cart_items:
        # 기존 주문에서 동일한 제품을 찾습니다.
        current_order = Order.objects.filter(
            product=cart_item.product,
        ).first()

        if current_order:
            # 기존 주문이 있으면 수량과 총액을 업데이트합니다.
            current_order.order_qty += cart_item.cart_qty
            current_order.order_amount = current_order.order_qty * current_order.product.product_price
            current_order.save()
        else:
            # 기존 주문이 없으면 새 주문을 생성합니다.
            order = Order.objects.create(
                product=cart_item.product,
                order_qty=cart_item.cart_qty,
                order_amount=cart_item.total_price(),  # 주문 총액을 입력합니다
            )
            order.save()
        print("1")
        print("10")

# 전체 상품 구매 처리
def handle_all_buy(request):
    # 장바구니에 있는 모든 상품들을 가져옵니다.
    cart_session_id = request.session.get('cart_session_id')
    cart_items = Cart.objects.filter(cart_session_id=cart_session_id, user=None)

    for cart_item in cart_items:
        # 기존 주문에서 동일한 제품을 찾습니다.
        current_order = Order.objects.filter(
            product=cart_item.product,
        ).first()

        if current_order:
            # 기존 주문이 있으면 수량과 총액을 업데이트합니다.
            current_order.order_qty += cart_item.cart_qty
            current_order.order_amount = current_order.order_qty * current_order.product.product_price
            current_order.save()
        else:
            # 기존 주문이 없으면 새 주문을 생성합니다.
            order = Order.objects.create(
                product=cart_item.product,
                order_qty=cart_item.cart_qty,
                order_amount=cart_item.total_price(),  # 주문 총액을 입력합니다.
            )
            order.save()

# 장바구니 상품 추가
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, product_id=product_id)

    # 세션에서 cart_session_id 가져오기 또는 생성
    cart_session_id = request.session.get('cart_session_id')
    if not cart_session_id:
        cart_session_id = get_random_string(32)
        request.session['cart_session_id'] = cart_session_id

    # Cart 아이템 가져오기 또는 생성
    cart_item, created = Cart.objects.get_or_create(
        cart_session_id=cart_session_id,
        product=product,
        defaults={'cart_qty': 1}
    )
    if not created:
        cart_item.cart_qty += 1
        cart_item.save()
    print("view_cart 이동")
    return redirect('vending_app:view_cart')

# 장바구니 상품 업데이트
def update_cart(request, product_id, change):
    print("제발")
    cart_session_id = request.session.get('cart_session_id')
    try:
        change = int(change)
    except ValueError:
        return JsonResponse({'error': 'Invalid change value'}, status=400)
    
    # 세션 ID 가져오기
    cart_session_id = request.session.get('cart_session_id')
    if not cart_session_id:
        return JsonResponse({'error': 'No cart session'}, status=400)
    
    cart_item = get_object_or_404(Cart, cart_session_id=cart_session_id, product_id=product_id, user=None)
    cart_item.cart_qty += change
    if cart_item.cart_qty <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    print(f"update_cart called with product_id: {product_id}, change: {change}")
    return redirect('vending_app:view_cart')


# 장바구니 상품 삭제
def delete_cart_item(request, product_id):
    # 세션 ID 가져오기
    cart_session_id = request.session.get('cart_session_id')
    if not cart_session_id:
        return JsonResponse({'error': 'No cart session'}, status=400)
    
    cart_item = get_object_or_404(Cart, cart_session_id=cart_session_id, product_id=product_id, user=None)
    cart_item.delete()

    return redirect('vending_app:view_cart')


# # 주문 결제
# def orderPayment(request):
#     #order 초기화
#     if request.method == 'GET':
#         # Order.objects.all().delete()
#         # clear_cart 매개변수가 있는지 확인
#         if 'clear_cart' in request.GET and request.GET['clear_cart'] == 'true':
#             # 주문 테이블을 비웁니다.
#             Order.objects.all().delete()
#         else:
#             # 주문 결제 페이지를 보여줍니다.
#             orders = Order.objects.all() # 모든 주문 가져옴
#             count = len(orders)  # 주문의 개수 계산

        
#     order_total_payment = sum(order.order_total_price() for order in orders)

#     # 주문의 총 가격을 계산합니다.
#     for order in orders:
#         order.order_total_price = order.order_qty * order.product.product_price
    
#     return render(request, 'main/orderPayment.html', {'orders': orders, 'count': count, 'order_total_payment': order_total_payment})
# # 주문 결제
# def orderPayment(request):
#     # GET 요청일 때의 처리
#     if request.method == 'GET':
#         # 주문 정보를 조회하고 주문 총 가격을 계산합니다.
#         orders = Order.objects.all()  # 모든 주문 가져오기
#         count = len(orders)  # 주문 개수 계산
#         order_total_payment = sum(order.order_total_price() for order in orders)  # 주문 총 가격 계산

#         # 주문의 총 가격을 계산합니다.
#         for order in orders:
#             order.order_total_price = order.order_qty * order.product.product_price

#     # POST 요청 처리
#     elif request.method == 'POST':
#         # GET 요청과 동일한 로직을 수행합니다.
#         if 'clear_cart' in request.POST and request.POST['clear_cart'] == 'true':
#             Order.objects.all().delete()
#         else:
#             orders = Order.objects.all() 
#             count = len(orders)  
#             order_total_payment = sum(order.order_total_price() for order in orders)  

#         for order in orders:
#             order.order_total_price = order.order_qty * order.product.product_price

#         return render(request, 'main/orderPayment.html', {'orders': orders, 'count': count, 'order_total_payment': order_total_payment})
    
#     # 주문 결제 페이지를 보여줍니다.
#     return render(request, 'main/orderPayment.html', {'orders': orders, 'count': count, 'order_total_payment': order_total_payment})

# 주문 결제
def orderPayment(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        count = len(orders)
    elif request.method == 'POST':
        orders = Order.objects.all()
        count = len(orders)

        return redirect('vending_app:orderPayment')

    order_total_payment = sum(order.order_total_price() for order in orders)

    for order in orders:
        order.order_total_price = order.order_qty * order.product.product_price

    return render(request, 'main/orderPayment.html', {'orders': orders, 'count': count, 'order_total_payment': order_total_payment})


# 주문 결제 / 결제 방식
def process_payment(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        receipt = Receipt.objects.all() # 모든 결제를 가져옵니다.
        orders = Order.objects.all()  # 모든 주문을 가져옵니다.
        
        total_deposit_save = 0
        total_deposit_100 = 0
        total_deposit_500 = 0
        total_deposit_1000 = 0

        order_total_payment = sum(order.order_total_price() for order in orders)
        insufficient_deposit = False
        insufficient_stock = False


        # 주문 객체들을 순회하면서 결제 처리를 진행합니다.
        for order in orders:
            print("Processing order:", order.order_id)
            print("Order quantity:", order.order_qty)
            print("Product stock before update:", order.product.product_stock)
            
            # 재고가 부족한 경우 템플릿 렌더링
            if order.order_qty > order.product.product_stock:
                insufficient_stock = True

                context = {
                        'product_name': order.product.product_name,
                        'product_stock': order.product.product_stock,
                        'insufficient_stock': True,
                        
                }
                return render(request, 'main/PaymentFailed.html', context)
            
            # 주문 수량 만큼 재고를 감소시킵니다.
            # order.product.product_stock -= order.order_qty
            # order.product.save()
            
            # 현금 결제일 경우
            if payment_type == 'cash':
                quantity_1000 = int(request.POST.get('quantity_1000', 0) or '0')
                quantity_5000 = int(request.POST.get('quantity_5000', 0) or '0')
                quantity_10000 = int(request.POST.get('quantity_10000', 0) or '0')

                # Receipt 생성
                receipt = Receipt.objects.create(
                    payment_type=payment_type,
                    order=order,
                    receipt_amount=order_total_payment,
                    one_thousand=quantity_1000,
                    five_thousand=quantity_5000,
                    ten_thousand=quantity_10000,
                )
                # 총 입금 금액을 계산합니다.
                total_deposit = receipt.total_deposit()
                order.product.product_stock -= order.order_qty
                order_total_payment -= total_deposit
                print(total_deposit)
                # 결제 금액보다 입금 금액이 적은지 확인하는 코드
                if order_total_payment > 0:
                    insufficient_deposit = True
                    # total_deposit 값 저장
                    total_deposit_save = total_deposit
                    
                    # 1000원짜리 화폐 단위 계산
                    total_deposit_1000 = total_deposit // 1000
                    total_deposit = total_deposit % 1000

                    # 500원짜리 화폐 단위 계산
                    total_deposit_500 = total_deposit // 500
                    total_deposit = total_deposit % 500

                    # 100원짜리 화폐 단위 계산
                    total_deposit_100 = total_deposit // 100
                    total_deposit = total_deposit % 100
                    
                    # change 값 초기화
                    total_deposit = total_deposit_save

                    context = {
                            'total_deposit': total_deposit,
                            'insufficient_deposit': True,
                            'total_deposit_1000':total_deposit_1000,
                            'total_deposit_500':total_deposit_500,
                            'total_deposit_100':total_deposit_100,
                    }
                    # 결제 금액이 0보다 적은 경우 결제 실패 페이지로 이동합니다.
                    return render(request, 'main/PaymentFailed.html', context)
                
                order.product.save()
            
            # 카드 결제일 경우
            elif payment_type == 'card':
                print(order.order_total_price)
                # Receipt 생성
                receipt = Receipt.objects.create(
                    payment_type=payment_type,
                    order=order,
                    receipt_amount=order_total_payment,
                )

                order.product.product_stock -= order.order_qty
                order.product.save()

            print("Product stock after update:", order.product.product_stock)
        # 결제 완료 후 orderComplete 페이지로 이동합니다.
        return redirect('vending_app:orderComplete')
    
    return redirect('vending_app:view_cart')

#주문결제 초기화
def process_order_reset(request):
    if request.method == 'POST':
        # 주문 테이블을 비웁니다.
        Order.objects.all().delete()
        # 뷰나 템플릿에서 적절한 리디렉션을 수행하거나, 응답을 반환합니다.
        return redirect('vending_app:orderPayment')

#주문완료
def orderComplete(request):
    receipt = Receipt.objects.first()
    
    orders = Order.objects.all()
    order_total_payment = sum(order.order_total_price() for order in orders)
    total_deposit = 0
    # 거스룸돈은 100원, 500원, 1000원 가능
    change = 0
    change_save = 0
    change_100 = 0
    change_500 = 0
    change_1000 = 0

    if orders.exists():
        last_order = orders.latest('order_datetime')
        try:
            receipt = Receipt.objects.filter(order=last_order).latest('receipt_datetime')
            if receipt.payment_type == 'cash':
                total_deposit = receipt.total_deposit()
                change = total_deposit - order_total_payment
                # change 값 저장
                change_save = change
                
                # 1000원짜리 화폐 단위 계산
                change_1000 = change // 1000
                change = change % 1000

                # 500원짜리 화폐 단위 계산
                change_500 = change // 500
                change = change % 500

                # 100원짜리 화폐 단위 계산
                change_100 = change // 100
                change = change % 100
                
                # change 값 초기화
                change = change_save
 
        except Receipt.DoesNotExist:
            receipt = None

    order_receipts = {}
    for order in orders:
        try:
            order_receipts[order.order_id] = Receipt.objects.filter(order=order).latest('receipt_datetime')
        except Receipt.DoesNotExist:
            order_receipts[order.order_id] = None

    context = {
        'receipt_datetime': receipt.receipt_datetime,
        'payment_type': receipt.payment_type,
        'orders': orders,
        'order_receipts': order_receipts,
        'order_total_payment': order_total_payment,
        'total_deposit': total_deposit,
        'change': change,
        'change_1000': change_1000,
        'change_500': change_500,
        'change_100': change_100,
    }
    return render(request, 'main/orderComplete.html', context)

# 결제 실패 페이지
def PaymentFailed(request):
    orders = Order.objects.all()

    return render(request, 'main/PaymentFailed.html')

# 영수증 페이지
def orderReceipt(request):
    receipt = Receipt.objects.first()
    
    orders = Order.objects.all()
    order_total_payment = sum(order.order_total_price() for order in orders)
    total_deposit = 0
    # 거스룸돈은 100원, 500원, 1000원 가능
    change = 0
    change_save = 0
    change_100 = 0
    change_500 = 0
    change_1000 = 0

    if orders.exists():
        last_order = orders.latest('order_datetime')
        try:
            receipt = Receipt.objects.filter(order=last_order).latest('receipt_datetime')
            if receipt.payment_type == 'cash':
                total_deposit = receipt.total_deposit()
                change = total_deposit - order_total_payment
                # change 값 저장
                change_save = change
                
                # 1000원짜리 화폐 단위 계산
                change_1000 = change // 1000
                change = change % 1000

                # 500원짜리 화폐 단위 계산
                change_500 = change // 500
                change = change % 500

                # 100원짜리 화폐 단위 계산
                change_100 = change // 100
                change = change % 100
                
                # change 값 초기화
                change = change_save
 
        except Receipt.DoesNotExist:
            receipt = None

    order_receipts = {}
    for order in orders:
        try:
            order_receipts[order.order_id] = Receipt.objects.filter(order=order).latest('receipt_datetime')
        except Receipt.DoesNotExist:
            order_receipts[order.order_id] = None

    context = {
        'receipt_datetime': receipt.receipt_datetime,
        'payment_type': receipt.payment_type,
        'orders': orders,
        'order_receipts': order_receipts,
        'order_total_payment': order_total_payment,
        'total_deposit': total_deposit,
        'change': change,
        'change_1000': change_1000,
        'change_500': change_500,
        'change_100': change_100,
    }

    return render(request, 'main/orderReceipt.html', context)