from rest_framework import serializers

from eco.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('category',"slug","name","image","description")
