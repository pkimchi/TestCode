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
        uip1=request.POST.get('val1')
        uip2=request.POST.get('val2')
        uiconlvl=request.POST.get('val3')
        uipower=request.POST.get('val4')
        uitailed=request.POST.get('tvalue')
        dailyv=request.POST.get('val6')
        uiratio=request.POST.get('val7')
        variations=request.POST.get('val8')
        uipop=request.POST.get('val9')
        uirr=float(request.POST.get('val10'))

        lift=(float(uip2)-float(uip1))/float(uip1)*100
### Finite Populatino Correction and float to string error correction
        if uipop == "":
            ss=sample_size_calc(float(uip1),float(uip2),int(uiconlvl),int(uipower),int(uiratio),uitailed)
        else:
            uipop= float(uipop)
            ss=sample_size_calc(float(uip1),float(uip2),int(uiconlvl),int(uipower),int(uiratio),uitailed,uipop)

        if uirr == 100:
            ss=ss
        else:
            uirr=1-(uirr/100)
            ssincr=(ss*uirr)
            ss=ss+int(ssincr)

        days = ""
        if not dailyv == "":
            days=round(ss*int(variations)/int(dailyv))
            days= max(7,days)

        return render_to_json_response({"result":ss,"resultsdays":days,"resultslift":lift})

    mytemplate = loader.get_template('calc/index.html')
    return HttpResponse(mytemplate.render({},request))

def sample_size_calc(p1,p2,con_lvl,power,k,tval,pop=None):
    """Advanced Sample size calculator

    Allows the user to choose p1, p2, confidence level and power

    p1 = baseline % (sample proportion in group 1)
    p2 = anticipated change % (sample proportion in group 2)
    Con_lvl = Confidence level % aka alpha
    s_power = statistical power aka beta
            (set to 80), this is a common industry choice
            zscore of 80% = 0.84

    Returns: the minimum sample size required with the given proportions,
    to ensure that the test results in a significant detectable increase.

    """
    #alpha zscore
    if tval == "t1":
        if con_lvl == 95:
            az = 1.645
        else:
            con_lvl = con_lvl/100
            az = st.norm.ppf(con_lvl)
    else:
        if con_lvl == 95:
            az = 1.96
        else:
            con_lvl = con_lvl/100
            az = st.norm.ppf(1-(1-con_lvl)/2)

    #beta zscore
    if power == 80:
        bz = 0.84
    else:
        power = power/100
        bz = st.norm.ppf(power)

 #   S_power = 0.84 # zscore

    p1 = p1/100

    p2 = p2/100

    #ratio correction
    rC= (p1*(1-p1))/k

    #initial sample size with reponse ratio correction and no
    #finite population correction
    ss = (az + bz)**2 * (rC+p2*(1-p2))/(p1-p2)**2

    if pop is None:
        return int(np.around(ss))

    else:
        # finite population correction for fpc less than .95 bc as the fpc
        # value approaches 1 the value becomes somewhat insignificant
        #Large populations fpc is greater than .95

        X = (az + bz)**2 / (p1-p2)**2

        #This is because both populations are the same
        #to change for fpc for two separate populations alter
        #pop before the p1 for p1 pop & pop before p2 for p2 pop for both
        #fpcA and fpcB
        fpcA = (pop/(pop-1))*(rC) + (pop/(pop-1))*(p2*(1-p2))
#        fpcA = (pop/(pop-1))*(p1*(1-p1)) + (pop/(pop-1))*(p2*(1-p2))
        fpcB =  (1/(pop-1))*(rC) + (1/(pop-1))*(p2*(1-p2))
#        fpcB =  (1/(pop-1))*(p1*(1-p1)) + (1/(pop-1))*(p2*(1-p2))
        ss = (X*fpcA)/(1+X*fpcB)

        return int(np.around(ss))


#        fpc=(pop-ss)/(pop-1)
#        print(fpc)
#        if fpc > .95:
#            return int(np.around(ss))
#        else:
#            ss = (az + bz)**2 * (fpc*p1*(1-p1)+fpc*p2*(1-p2))/(p1-p2)**2
#            return int(np.around(ss))

#creates a json
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)
