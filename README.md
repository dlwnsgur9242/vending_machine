# Vending Machine
Customer-specific vending machine project.
<br>
Django의 MTV(Model-Template-View)디자인 패턴을 사용하여 WebApp개발을 하였습니다.
<br><br><br>

# Tech Stack 🛠️
<pre>
  Visual Studio Code 1.82.2
  Django 4.2.1
  Python 3.10.9
  MariaDB 10.11
</pre>
<br><br><br>

# <제한조건>✅
<pre>
  1.현금 안될 경우 신용카드 통해 받을 수 있도록 조정<br>
  2.천원, 오천원, 만원가능, 오만원 불가<br>
  3.거스룸 돈은 100원, 500원, 1000원 가능<br>
  4.영수증 필요한 경우 금액 적힌 영수증 출력
</pre>
<br><br><br>

# <추가한 기능>☑️
<pre>
  1. 상품 리스트 페이지(ProductList.html)
   - 선택한 상품 장바구니 추가
   - 상품 장바구니 추가 시 팝업 창 출력
   - DB product table 연결
  <br>
  2. 상품 상세 페이지(Product_detail.hmtl)
   - 상품 재고, 가격 확인 가능
   - 장바구니 상품 추가
  <br>
  3. 장바구니 페이지(view_cart.hmtl)
   - 선택삭제, 전체삭제
   - 선택 구매, 전체 구매
   - DB cart table 연결
  <br>
  4. 주문결제 페이지(orderPayment.html)
   - 결제 시 재고 소모
   - 상품 초기화
   - DB order table 연결
   - DB receipt table 연결
  <br>
  5. 결제완료 페이지(orderComplete.html)
   - 결제 완료 시 영수증 출력 선택 팝업 창 출력
   - 주문 시간, 결제 방식, 상품 별 총 가격, 결제 총금액, 거스름돈 출력
   - def process_payment로 주문 결제 / 결제 방식 처리
   - def process_payment 재고 부족, 금액 부족, 카드 or 현금 결제 처리
  <br>
  6. 영수증 페이지(orderReceipt.html)
   - 카테고리, 상품명, 구매가, 수량, 금액, 합계, 결제 방식, 거스름 돈, 거래 일시 출력
  <br>
  7. 관리자 페이지(admin_ProductList.html)
   - 상품 관리, 상품 등록 가능
  <br>
  8. 상품 관리 페이지(Product_manage.hmtl)
   - 상품 목록 표시
   - 상품 수정, 삭제 가능
   - DB product table 연결
  <br>
  9. 상품 등록 페이지(Product_registration.html)
   - 상품 등록 가능
   - DB product table 연결
</pre>
<br><br><br>

# 시연 영상 🎬
<br>

### 현금 결제
https://youtu.be/YxDUGy-v1QQ
<br><br>

### 입금한 금액이 적은 경우
https://youtu.be/d61-tC57ksc
<br><br><br><br>

# 상품 리스트 🧸🛍️
![상품리스트1](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/d0c93ca0-02f3-4da4-8758-8b2913b47b8d)
<br>

![상품리스트2](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/9535d3e6-7fee-4d2c-97e9-7550395214e9)
<br>

![상품리스트3](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/0ce8e84f-99d0-4e4d-bf0c-e6bcdf118ded)
<br><br><br>

### 상품 리스트 장바구니 추가 버튼
![상품 장바구니 추가 버튼](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/325b3df0-51e9-46fa-a41a-0dcd058eca7a)
<br>
### 상품 리스트 장바구니 추가 버튼 [ 동작 ]
![상품 장바구니 추가 버튼_동작](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/53abc0a8-bf5a-4f69-854a-eff6f7cc0d6f)
<br><br><br>

# 상품 상세 페이지 🔍
![상품상세페이지_1](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/5f88a25b-be94-4eb3-b11f-f7d88420bbfb)
<br><br><br><br>

# 장바구니 🛒
![장바구니 화면](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/a8a26756-76a0-489a-995f-34bf0b3668e3)
<br>
### 장바구니 결제 금액 계산
![장바구니 화면 결제 금액 계산](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/665fe94a-fc06-45e3-9521-16b5f1d3584a)
<br><br>

### 장바구니 수량 변경
![장바구니 수량 변경](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/6565b468-c667-49f9-a1d1-0559a4211783)
<br><br>

### 장바구니 상품 삭제 버튼
![장바구니 상품 삭제 버튼](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/5518293f-be33-448f-8d3c-1e4991f7f8cc)
<br>

### 장바구니 상품 삭제 버튼 [ 동작 ]
![장바구니 상품 삭제 버튼 동작 후](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/3a313e61-e64a-404e-8fb7-078d9a7ae1dd)
<br><br>

### 장바구니 상품 체크 선택 삭제
![장바구니 상품 체크 선택 삭제](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/5bc32664-2629-47f8-ac46-fe5e02ba5e50)
<br>

### 장바구니 상품 체크 선택 삭제 [ 동작 ]
![장바구니 상품 체크 선택 삭제 동작 후](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/840000cd-bea3-4af5-b87f-9fdad9b82714)
<br><br>

### 장바구니 상품 선택상품 체크 구매 버튼
![장바구니 상품 체크 선택상품 구매 버튼](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/f907b1b7-d274-4063-9a84-c2c92f3076d7)
<br>

### 장바구니 상품 선택상품 체크 구매 버튼 [ 동작 ]
![장바구니 상품 체크 선택상품 구매 버튼 동작 후](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/483ff8dd-bca2-4486-b2c0-feb15503e71b)
<br><br>

### 장바구니 상품 전체 상품 구매 버튼
![장바구니 상품 전체상품 구매 버튼](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/a7fa2c0d-845d-472b-8095-cc7f501a9621)
<br>
### 장바구니 상품 전체 상품 구매 버튼 [ 동작 ]
![장바구니 상품 전체상품 구매 버튼 동작 후](https://github.com/dlwnsgur9242/vending_machine/assets/90494150/56699baa-5812-4c18-974f-3a6bac1221a6)
<br><br><br><br>

# 관리자 페이지 🐱💻
<br>

### 관리자 페이지(메인화면)
![관리자 페이지_메인](https://github.com/user-attachments/assets/e8e19894-86e2-4e27-b52f-e27504447f81)
<br><br>
## 상품 등록 🎈
![관리자 페이지_상품등록](https://github.com/user-attachments/assets/1331b07f-2e13-4104-b186-217db47d9739)
<br>
### 상품 등록 입력 예시
![관리자 페이지_상품등록 시연1](https://github.com/user-attachments/assets/57901f1d-51ae-48e0-91bf-321db3b95bb0)
### 등록한 상품 상품 리스트 출력
![관리자 페이지_상품등록 시연2](https://github.com/user-attachments/assets/b50bc1e9-1315-4958-a97d-747ae53dde34)
### 등록한 상품 값 DB 저장
![관리자 페이지_상품등록 시연3](https://github.com/user-attachments/assets/9739bb46-68c7-41f7-b8a8-1c2bbdb36a7b)
<br><br><br><br>

## 상품 관리 ✈️
<br>

### 상품 관리 페이지 이동 버튼
![관리자 페이지 상품관리 이동 버튼](https://github.com/user-attachments/assets/68975689-8fe8-4f35-8b9d-f757fcc134ea)
<br>
### 상품 관리 페이지(메인화면)
![관리자 페이지 상품 관리 페이지](https://github.com/user-attachments/assets/951a6731-0d9f-42c5-a80d-06be8611f66e)
<br><br><br>

## 상품 관리 페이지 - 수정
![관리자 페이지 상품관리-수정](https://github.com/user-attachments/assets/0782f826-7ab8-497e-a28b-fc4305ad7324)
<br>
### 상품 관리 페이지 - 수정 [ 동작 ]
![관리자 페이지 상품 관리 페이지-수정 전](https://github.com/user-attachments/assets/a32c6cee-b1d5-4f40-a6ca-c85c754bc79c)
<br>
### 상품 관리 페이지 - 수정 [ 동작 - 입력 값 변경 ]
![관리자 페이지 상품 관리 페이지-수정 후](https://github.com/user-attachments/assets/78af0ecc-0b23-4108-b096-841814f6175f)
<br>
### 상품 관리 페이지 - 수정 [ 적용 ]
![관리자 페이지 상품 관리 페이지-수정 후 적용](https://github.com/user-attachments/assets/ebc637b9-f71e-4952-95bb-fe6a3261e087)
<br><br><br>

## 상품 관리 페이지 - 삭제
![관리자 페이지 상품 관리 페이지-삭제](https://github.com/user-attachments/assets/29329419-98cb-442a-8d9b-35142002cd3f)
<br>
### 상품 관리 페이지 - 삭제 [ 동작 ]
![관리자 페이지 상품 관리 페이지-삭제 후](https://github.com/user-attachments/assets/74f20258-83eb-4c74-a85f-b50893d3958e)
