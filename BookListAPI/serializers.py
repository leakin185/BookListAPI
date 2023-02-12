from rest_framework import serializers
from .models import Bookitem

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookitem
        fields = ['id','title','author','price']