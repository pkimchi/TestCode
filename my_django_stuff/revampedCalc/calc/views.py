#from django.shortcuts import render

from django.http import HttpResponse

from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, render_to_response
from math import pi
import numpy as np

def index(request):
    #return render(request, 'index.html')
    #return render(request, 'calc/index.html')
    return render_to_response('calc/index.html')


def result(request, test):
    if request.method == "GET":
        con_lvl= request.GET['conLevel']
        me = request.GET['marginError']
        pop = request.GET['popSize']

    tuple = sample_size_calc(float(con_lvl), float(me), float(pop))
    return render(request, 'calc/result.html', {
        'conLevel': con_lvl,
        'marginError': me,
        'popSize' : pop,
        'tuple': tuple,
        'ss': ss
#        'wastedSpace': tuple[1],
#        'numOfCans': tuple[0]
    })

def sample_size_calc(con_lvl, me, pop_size=None):
    P=.5

    if con_lvl == 95 or con_lvl == .95:
        con_lvl = 1.96 # zscore

    if con_lvl == 99 or con_lvl == .99:
        con_lvl = 2.58 # zscore

    ss = np.ceil(con_lvl**2 *P *(1-P)/me**2)

    if pop_size is None:
        print("Minimum sample size you need is: ", ss)
        return ss

    else:
        ss = np.ceil(ss/(1+(ss/pop_size)))
        print("Minimum sample size you need is: ", ss)
        return ss
