from django import forms
from .models import Product

class ProductRegisterForm(forms.ModelForm):
    FLAG_CHOICES = [
        ('글루텐', '글루텐'),
        ('할랄', '할랄'),
        ('일반', '일반'),
    ]

    product_flag = forms.ChoiceField(choices=FLAG_CHOICES, label='상품 종류')
    product_image = forms.ImageField(label='이미지')
    product_price = forms.DecimalField(label='가격', decimal_places=0)
    
    class Meta:
        model = Product
        fields = ['product_name', 'product_stock', 'product_price', 'product_flag', 'product_image']
        labels = {
            'product_name': '상품명',
            'product_stock': '재고량',
            'product_price': '가격',
            'product_flag': '상품 종류',
            'product_image': '이미지',
        }

    def clean_product_image(self):
        product_image = self.cleaned_data.get('product_image', False)
        if not product_image:
            raise forms.ValidationError("이미지를 업로드해야 합니다.")
        return product_image

class AddToCartForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput)