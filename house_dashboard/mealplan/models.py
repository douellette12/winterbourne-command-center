from django.db import models


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_planned = models.DateField(null=True, blank=True)
    meal_type = models.CharField(max_length=10, choices=[("breakfast", "Breakfast"), ("lunch", "Lunch"), ("dinner", "Dinner")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, related_name="ingredients", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GroceryItem(models.Model):
    title = models.CharField(max_length=100)
    from_meal = models.ForeignKey(Ingredient, null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)
    added_manually = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title