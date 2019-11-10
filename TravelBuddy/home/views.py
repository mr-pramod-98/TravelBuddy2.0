from django.shortcuts import render


# Create your views here.
# THIS IS THE HOME PAGE TO THIS WEBSITE
# "index" METHOD IS CALLED WHEN THE USER REQUESTS FOR "index" PAGE
def index(request):
    return render(request, 'index.html')
