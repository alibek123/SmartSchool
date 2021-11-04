from rest_framework import serializers
from .models import Meal, Category


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'productID',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'get_image',
            'get_thumbnail'
        )


class CategorySerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'meals',
        )
