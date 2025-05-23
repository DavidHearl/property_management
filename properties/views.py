from django.shortcuts import render
        
def home(request):
    return render(request, 'properties/home.html')