from django.shortcuts import render

# Create your views here.
def abouthome(request):
    return render(request ,"about/abouthome.html")
