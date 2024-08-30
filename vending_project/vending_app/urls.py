from django.urls import path
from . import views

app_name = 'vending_app'

urlpatterns = [
    #테스트 페이지
    path('index',views.index, name="index"),

    #상품 리스트
    path('', views.ProductList, name="ProductList"),

    #상품 리스트 관리 페이지
    path('admin', views.admin_ProductList, name='admin'),

    #상품 관리 페이지
    path("Product_manage", views.Product_manage, name="Product_manage"),
    #상품 관리/삭제
    path("admin_product_delete/<uuid:product_id>/",views.admin_product_delete, name="admin_product_delete"),
    #상품 관리/수정
    path("admin_product_modify/<uuid:product_id>/",views.admin_product_modify, name="admin_product_modify"),

    #상품 등록
    path('Product_registration', views.Product_registration, name='Product_registration'),

    #상품 상세 정보 페이지
    path('Product_detail/<uuid:product_id>/', views.Product_detail, name='Product_detail'),
    #상품 상세 페이지 주문으로 추가
    path('add_to_detail/<uuid:product_id>/', views.add_to_detail, name='add_to_detail'),
    #상품 상세 페이지 상품 정보저장
    path('update_detail_qty/', views.update_detail_qty, name='update_detail_qty'),

    #장바구니
    path('view_cart', views.view_cart, name="view_cart"),
    #장바구니 상품 추가/상품리스트
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    #장바구니 상품 추가/상세페이지
    path('add_to_detail_cart', views.add_to_detail_cart, name='add_to_detail_cart'),

    path('update_cart/<uuid:product_id>/<str:change>/', views.update_cart, name='update_cart'),
    path('delete_cart_item/<uuid:product_id>/', views.delete_cart_item, name='delete_cart_item'),
   
    #주문 결제
    path('orderPayment', views.orderPayment, name="orderPayment"),

    #현금 입금을 위한 URL 패턴
    #결제 처리를 위한 URL
    path('process_payment', views.process_payment, name='process_payment'),
    
    #주문결제 초기화
    path('process_order_reset', views.process_order_reset, name='process_order_reset'),

    #결제 완료 페이지
    path('orderComplete', views.orderComplete, name='orderComplete'),

    #결제 오류 페이지
    path('PaymentFailed', views.PaymentFailed, name='PaymentFailed'),

    #영수증 페이지
    path('orderReceipt',views.orderReceipt,name='orderReceipt'),
    
]