from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    visited_pages = request.session.get("visited_pages", [])
    context = {
        "visited_pages": visited_pages[::-1],
    }
    return render(request, "www/home.html", context=context)
