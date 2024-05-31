from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, User
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProductRegisterForm, AddToCartForm
from .forms import AddToCartForm
from django.utils.crypto import get_random_string

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
    # 상품 정보 조회
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        # POST 요청일 경우, 장바구니에 상품 추가 폼을 처리
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # 폼이 유효한 경우, 상품을 장바구니에 추가하고 장바구니 페이지로 이동
            return redirect('vending_app:add_to_cart')
    else:
        # POST 요청이 아닐 경우, 장바구니에 상품 추가 폼을 생성
        form = AddToCartForm()

    # 상품 상세 정보 페이지를 렌더링하여 반환
    return render(request, 'main/product_detail.html', {'product': product, 'form': form})

# # 장바구니
# def view_cart(request):
#     cart_session_id = request.session.get('cart_session_id')
#     if not cart_session_id:
#         cart_items = []
#         total_price = 0
#     else:
#         cart_items = Cart.objects.filter(cart_session_id=cart_session_id, user=None)
#         total_price = sum(item.product.product_price * item.cart_qty for item in cart_items)

#     return render(request, 'main/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 장바구니
def view_cart(request):
    # 현재 사용자의 장바구니에 있는 상품들을 가져옴
    cart_session_id = request.session.get('cart_session_id')
    cart_items = Cart.objects.filter(cart_session_id= cart_session_id, user=None)

    for cart_item in cart_items:
        cart_item.total_price = cart_item.cart_qty * cart_item.product.product_price
    
    print(cart_item.product.product_id)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'main/view_cart.html', context)

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

    return redirect('vending_app:view_cart')

# 장바구니 상품 업데이트
def update_cart(request, product_id, change):
    # 세션 ID 가져오기
    cart_session_id = request.session.get('cart_session_id')
    if not cart_session_id:
        return JsonResponse({'error': 'No cart session'}, status=400)
    
    cart_item = get_object_or_404(Cart, session_id=cart_session_id, product_id=product_id, user=None)
    cart_item.cart_qty += change
    if cart_item.cart_qty <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    return redirect('vending_app:view_cart')

# 장바구니 상품 삭제
def delete_cart_item(request, product_id):
    # 세션 ID 가져오기
    cart_session_id = request.session.get('cart_session_id')
    if not cart_session_id:
        return JsonResponse({'error': 'No cart session'}, status=400)
    
    cart_item = get_object_or_404(Cart, session_id=cart_session_id, product_id=product_id, user=None)
    cart_item.delete()

    return redirect('vending_app:view_cart')