from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to my Django app 1!")
