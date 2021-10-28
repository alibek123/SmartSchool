from django.db.models import Q

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

from .models import Meal, Category
from .serializers import MealSerializer, CategorySerializer


class MealList(ListAPIView):
    serializer_class = MealSerializer
    queryset = Meal.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']


class MealAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']

    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = MealSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealDetails(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_object(self, category_slug, meal_slug):
        try:
            return Meal.objects.filter(category__slug=category_slug).get(slug=meal_slug)
        except Meal.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, category_slug, meal_slug):
        meal = self.get_object(category_slug, meal_slug)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    # def put(self, request, id):
    #     meal = self.get_object(id)
    #     serializer = MealSerializer(meal, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, id):
    #     meal = self.get_object(id)
    #     meal.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Meal.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, category_slug):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query','')
    print(query)
    if query:
        meals = Meal.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
    else:
        return Response({"meals": []})
