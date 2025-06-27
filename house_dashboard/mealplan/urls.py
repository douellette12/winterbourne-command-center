from django.urls import path
from . import views
from .views import GroceryListView, GroceryDeleteView, GroceryUpdateView, MealPlanView

urlpatterns = [
    path("", MealPlanView.as_view(), name="meal-plan"),
    path("grocery-list/", GroceryListView.as_view(), name="grocery_list"),
    path("grocery-list/add/", views.grocery_add, name="grocery_add"),
    path('grocery-list/toggle/', views.toggle_grocery_item, name='toggle_grocery_item'),
    path("grocery-list/delete/<int:pk>/", GroceryDeleteView.as_view(), name="delete-grocery-item"),
    path('grocery-list/edit/<int:pk>/', GroceryUpdateView.as_view(), name='grocery_edit')
]
