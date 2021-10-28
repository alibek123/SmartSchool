from django.urls import path

from api_basic import views

urlpatterns = [
    path('meals/', views.MealAPIView.as_view()),
    # path('meals/', views.MealList.as_view()),
    path('meals/search/', views.search),
    path('meals/<slug:category_slug>/<slug:meal_slug>/', views.MealDetails.as_view()),
    path('meals/<slug:category_slug>/', views.CategoryDetail.as_view()),
]
