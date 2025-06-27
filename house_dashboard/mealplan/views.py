from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin, UpdateView, CreateView
from .forms import GroceryItemForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import GroceryItem, Meal


class MealPlanView(TemplateView):
    template_name = "mealplan/meal_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meals"] = Meal.objects.all().order_by("date_planned")
        context["active_items"] = GroceryItem.objects.filter(completed=False)
        context["completed_items"] = GroceryItem.objects.filter(completed=True)
        return context



@require_POST
@csrf_exempt
def toggle_grocery_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(GroceryItem, pk=item_id)

        item.completed = not item.completed
        item.save()

        row_html = render_to_string("mealplan/groceries/item_list_item.html", {"item": item})
        return JsonResponse({
            "completed": item.completed,
            "html": row_html,
            "id": item.id
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



class GroceryListView(ListView):
    model = GroceryItem
    template_name = 'mealplan/meal_list.html'
    context_object_name = 'items'
    success_url = reverse_lazy('meal-plan')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_items'] = GroceryItem.objects.filter(completed=False)
        context['completed_items'] = GroceryItem.objects.filter(completed=True)

        return context



@require_POST
def grocery_add(request):
    title = request.POST.get('title')
    if title:
        item = GroceryItem.objects.create(title=title)
        return JsonResponse({
            'success': True,
            'id': item.id,
            'title': item.title,
            'completed': item.completed
        })
    return JsonResponse({'success': False, 'error': 'Missing title'})


class GroceryDeleteView(DeleteView):
    model = GroceryItem
    success_url = reverse_lazy('grocery_list')


class GroceryUpdateView(UpdateView):
    model = GroceryItem
    form_class = GroceryItemForm

    def form_valid(self, form):
        item = form.save()
        return JsonResponse({'id': item.id, 'title': item.title})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

