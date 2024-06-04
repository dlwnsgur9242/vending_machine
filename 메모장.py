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