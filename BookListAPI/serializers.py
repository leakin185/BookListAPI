from rest_framework import serializers
from decimal import Decimal
from .models import Bookitem, Category

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
    class Meta:
        model = Bookitem
        fields = ['id','title','author','price','price_after_tax','category','category_id']
    
    def calculate_tax(self, product:Bookitem): 
        return product.price * Decimal(1.1)
        