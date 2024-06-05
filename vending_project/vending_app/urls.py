from django.urls import path
from . import views

app_name = 'vending_app'

urlpatterns = [
    #상품 리스트
    path('', views.ProductList, name="ProductList"),
    #상품 등록
    path('productmanage', views.productmanage, name='productmanage'),
    #상품 상세 정보 페이지
    path('product_detail/<uuid:product_id>/', views.product_detail, name='product_detail'),
    
    #장바구니
    path('view_cart', views.view_cart, name="view_cart"),
    #장바구니 상품 추가
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),

    path('update_cart/<uuid:product_id>/<str:change>/', views.update_cart, name='update_cart'),
    path('delete_cart_item/<uuid:product_id>/', views.delete_cart_item, name='delete_cart_item'),

    #주문 결제
    path('orderPayment', views.orderPayment, name="orderPayment"),

    #현금 입금을 위한 URL 패턴
    #결제 처리를 위한 URL
    path('process_payment', views.process_payment, name='process_payment'),
    
    #주문결제 초기화
    path('process_order_reset', views.process_order_reset, name='process_order_reset'),

]