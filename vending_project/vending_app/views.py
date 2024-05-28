from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import ProductRegisterForm, AddToCartForm
from .forms import AddToCartForm
from django.contrib.auth.models import User

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
            # 여기서는 장바구니 추가 로직을 작성하지 않고, 단순히 장바구니 페이지로 리다이렉트함
            return redirect('vending_app:add_to_cart')
    else:
        # POST 요청이 아닐 경우, 장바구니에 상품 추가 폼을 생성
        form = AddToCartForm()

    # 상품 상세 정보 페이지를 렌더링하여 반환
    return render(request, 'main/product_detail.html', {'product': product, 'form': form})

# 장바구니
def view_cart(request):
    cart_items = Cart.objects.filter(user=None)  # 익명의 사용자의 장바구니 항목 가져오기
    total_price = sum(item.product.product_price * item.cart_qty for item in cart_items)

    return render(request, 'main/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 장바구니 상품 추가
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, product_id=product_id)

            # 사용자 정보를 사용하지 않으므로 장바구니 항목을 데이터베이스에 저장
            cart_item, created = Cart.objects.get_or_create(
                user=None,  # 익명의 사용자를 위해 user를 None으로 설정
                product=product,
                defaults={'cart_qty': 1}
            )
            if not created:
                cart_item.cart_qty += 1
                cart_item.save()

            return redirect('vending_app:view_cart')
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 장바구니 상품 업데이트
def update_cart(request, product_id, change):
    if request.user.is_authenticated:
        user = request.user
        cart_item = get_object_or_404(Cart, user=user, product_id=product_id)
        cart_item.cart_qty += change
        if cart_item.cart_qty <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart_item = cart.get(product_id)
        if cart_item:
            cart_item['quantity'] += change
            if cart_item['quantity'] <= 0:
                del cart[product_id]
        request.session['cart'] = cart
    return redirect('vending_app:view_cart')

# 장바구니 상품 삭제
def delete_cart_item(request, product_id):
    if request.user.is_authenticated:
        user = request.user
        cart_item = get_object_or_404(Cart, user=user, product_id=product_id)
        cart_item.delete()
    else:
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
    return redirect('vending_app:view_cart')