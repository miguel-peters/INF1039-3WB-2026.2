from django.shortcuts import render

def login_view(request):
    return render(request, "login.html")

def feed(request):
    return render(request, "feed.html")
