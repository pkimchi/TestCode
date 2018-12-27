from django.http import HttpResponse
from .models import Question
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from math import pi

import scipy.stats as st
import numpy as np
import json

def index(request):
    if request.is_ajax():
        s=request.POST.get('val1')
        r=request.POST.get('val2')
        f=request.POST.get('val3')
        ss=sample_size_calc(float(s),float(r),int(f))
        return render_to_json_response({"result":ss})
    #return render(request, 'index.html')
    #return render(request, 'calc/index.html'
    mytemplate = loader.get_template('calc/index.html')
    return HttpResponse(mytemplate.render({},request))

#def result(request, test):
#    if request.method == "GET":
#        con_lvl= request.GET['conLevel']
#        me = request.GET['marginError']
#        pop = request.GET['popSize']
#    tuple = sample_size_calc(float(con_lvl), float(me), float(pop))
#    return render(request, 'calc/result.html', {
#        'con_Level': con_asd,
#        'marginError': me,
#        'popSize' : pop,
#        'tuple': tuple,

#    })

#advance_calc_v1 10/16/18
def sample_size_calc(p1,p2,con_lvl):
    """Advanced Sample size calculator

    Currently for Confidence level 95 or 99

    p1 = baseline % (sample proportion in group 1)
    p2 = anticipated change % (sample proportion in group 2)
    Con_lvl = Confidence level % aka alpha
    s_power = statistical power aka beta
            (set to 80), this is a common industry choice
            zscore of 80% = 0.84

    Returns: the minimum sample size required with the given proportions,
    to ensure that the test results in a significant detectable increase.

    """

    if con_lvl == 95 or con_lvl == .95:
        con_lvl = 1.96 # zscore

    if con_lvl == 99 or con_lvl == .99:
        con_lvl = 2.58 # zscore

    S_power = 0.84 # zscore

    p1 = p1/100

    p2 = p2/100

    ss = (con_lvl + S_power)**2 * (p1*(1-p1)+p2*(1-p2))/(p1-p2)**2

    return int(np.ceil(ss))

#creates a json
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)
