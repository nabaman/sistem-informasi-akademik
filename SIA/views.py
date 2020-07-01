from django.shortcuts import render

def IndexView(request):


    return render(request, 'landing_page.html')