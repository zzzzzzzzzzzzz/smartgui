from django.shortcuts import render, render_to_response


# Create your views here.

def charts(request):
    return render_to_response("charts.html",
                              {"Testing": "Django Template Inheritance ",
                               "HelloHello": "Hello World - Django"})