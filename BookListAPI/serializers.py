from rest_framework import serializers
from decimal import Decimal
from .models import Bookitem, Category
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','slug']

class BookSerializer(serializers.ModelSerializer):
    # cost = serializers.IntegerField(source ='price')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name='category-detail'
    # )
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        return super().validate(attrs)
    class Meta:
        model = Bookitem
        fields = ['id','title','author','price','price_after_tax','category','category_id']
        validators = [
            UniqueTogetherValidator(
                queryset=Bookitem.objects.all(),
                fields=['title', 'price']
                ),
            ]
        extra_kwargs = {
            'price': {'min_value': 2},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=Bookitem.objects.all()
                        )
                    ]
                }
        }
    
    def calculate_tax(self, product:Bookitem): 
        return product.price * Decimal(1.1)
        