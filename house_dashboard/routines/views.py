from django.shortcuts import render

def routines(request):
    return render(request, "routines/routines.html")