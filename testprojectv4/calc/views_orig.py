#from django.shortcuts import render

from django.http import HttpResponse

from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, render_to_response
from math import pi

def index(request):
    #return render(request, 'index.html')
    #return render(request, 'calc/index.html')
    return render_to_response('calc/index.html')


# def result(request, can_height):
#     return render(request, 'calc/result.html', {'canHeight': can_height})

# def result(request):
#     if request.method == "POST":
#         list_values = request.POST.getlist('my_list')
#     return render(request, 'calc/result.html', {'list': list_values})

def result(request, test):
    if request.method == "GET":
        can_height= request.GET['canHeight']
        can_radius = request.GET['canRadius']
    tuple = calculate(float(can_radius), float(can_height))
    return render(request, 'calc/result.html', {
        'canHeight': can_height,
        'canRadius': can_radius,
        'tuple': tuple,
        'wastedSpace': tuple[1],
        'numOfCans': tuple[0]
    })


def calculate(Cd, Ch ):
    # Cd = 0.02
    # Ch = 0.10
    # volume of can/box
    Vb = (Cd * Cd * Ch)
    Vs = 32.2514

    # maximun number of cans that will fit in the shipping container
    maxCans = int(Vs / Vb)
    print("maximun number of cans that will fit in the shipping container: ", maxCans)

    wasteSp = (32.2514 - (maxCans * Ch * pi * (Cd / 2) ** 2))
    # volume of wasted space
    print("volume of wasted space: ", wasteSp, "m^3")

    return (maxCans, wasteSp)
    # General concensus: long skinny cans create less wasted space.
