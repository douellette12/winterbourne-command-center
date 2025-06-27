from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormMixin, UpdateView
from .forms import GroceryItemForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # or use CSRF token via JS
from .models import GroceryItem, Meal


class MealPlanView(ListView):
    model = Meal


@require_POST
@csrf_exempt  # You can remove this if you use a real CSRF token via JS
def toggle_grocery_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(GroceryItem, pk=item_id)

        item.completed = not item.completed
        item.save()

        row_html = render_to_string("mealplan/item_list_item.html", {"item": item})
        return JsonResponse({
            "completed": item.completed,
            "html": row_html,
            "id": item.id
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



class GroceryListView(FormMixin, ListView):
    model = GroceryItem
    template_name = 'mealplan/grocery_list.html'
    context_object_name = 'items'
    form_class = GroceryItemForm
    success_url = reverse_lazy('grocery_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_items'] = GroceryItem.objects.filter(completed=False)
        context['completed_items'] = GroceryItem.objects.filter(completed=True)

        for item in GroceryItem.objects.all():
            print(item.title, item.completed)

        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


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

