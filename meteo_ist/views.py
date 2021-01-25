from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from .services import upload_db
from meteo_ist.models import meteo_data, range_data
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import rangeSerializer
from datetime import date

class RangeViewSet(viewsets.ModelViewSet):
    queryset = range_data.objects.all()
    serializer_class = rangeSerializer

class GetMeteo(TemplateView):
    template_name = 'meteo.html'
    #start = '2020-01-05' 
    #end = '2020-01-08'

    def get_context_data(self, *args, **kwargs):
        range_date, created = range_data.objects.all().get_or_create(id=1)
        start = getattr(range_date, 'start')
        end = getattr(range_date, 'end')
        
        variable = 'pp'
        parameters = {'type':'daily','start': start, 'end': end}
        url = 'http://caboruivo.tecnico.ulisboa.pt:64104/api/obs'
        response = requests.get(url, params = parameters)
        data = response.json()
        print(end)
        upload_db(data)
        temps = []
        pp = []
        pres = []
        rad = []
        rh = []
        wd = []
        wg = []
        ws = []
        dates = []
        obj = meteo_data.objects.filter(date__gte = start, date__lte = end)
        for x in obj:
            temps.append(getattr(x, 'temp'))
            pp.append(getattr(x, 'pp'))
            pres.append(getattr(x, 'pres'))
            rad.append(getattr(x, 'rad'))
            rh.append(getattr(x, 'rh'))
            wd.append(getattr(x, 'wd'))
            wg.append(getattr(x, 'wg'))
            ws.append(getattr(x, 'ws'))
            dates.append(getattr(x, 'date').strftime('%Y-%m-%d'))      # convert date format to string
        
        context = {
            'temp_data' : temps,
            'pp_data' : pp,
            'pres_data' : pres,
            'rad_data' : rad,
            'rh_data' : rh,
            'wd_data' : wd,
            'ws_data' : ws,
            'wg_data' : wg,
            'date_data' : dates,
        }
        
        return context