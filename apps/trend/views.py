from django.shortcuts import render

# Create your views here.
def trend(request):
    return render(request, 'trend/trend.html')