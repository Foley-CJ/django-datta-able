# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.urls import reverse



from app import CJF_helpers

from json import dumps


import csv, logging, pandas


logger = logging.getLogger(__name__)


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( '000CJF_fileLoader.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login")
def upload_csv(request):
    context = {}

    r = CJF_helpers.twitter()
    print(r)
    context['twitterData'] = r




    if "GET" == request.method:
        logger.critical('Get Request - Data Loadz')
        logger.critical(context['twitterData'])
        html_template = loader.get_template( '000CJF_fileLoader.html')
        return HttpResponse(html_template.render(context, request))

    # try:
    else:
        logger.critical('Post Request - Data Processing')
        csv_file = request.FILES["csv_file"]

        # QA Checks 
        #QA001 - if file is not of csv, return
        if not csv_file.name.endswith('.csv'):
            logger.critical('File is not CSV type')
            return HttpResponse(reverse("upload_csv"))
        #QA002 - if file is too large, return
        # if csv_file.multiple_chunks():
        #     logger.critical(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        #     return HttpResponse(reverse("upload_csv"))


        # Data Processing
        #logger.critical('made it this far')
        #data = csv.reader(csv_file)
        dF = pandas.read_csv(csv_file)
        
        #dF = dF.head()

       
        data_html =  dF.to_html()


        # dump data
        context['data'] = dF.to_dict(orient='records')




        #Graph 1
        dF_Graph1 = CJF_helpers.graph1(dF)
        context['graph1'] = dF_Graph1

        #Graph 2
        dF_Graph2 = CJF_helpers.graph2(dF)
        context['graph2'] = dF_Graph2
        
        #Graph 3
        dF_Graph3 = CJF_helpers.graph3(dF)
        context['graph3'] = dF_Graph3

        #Graph 4
        dF_Graph4 = CJF_helpers.graph4(dF)
        context['graph4'] = dF_Graph4
    
       # print(dF_Graph3)





   
        #print(data_html)
        #logger.critical('fucked')
    html_template = loader.get_template( '000CJF_passData.html' )
    return HttpResponse(html_template.render(context, request))




 