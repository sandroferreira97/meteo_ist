from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from .services import upload_db
from meteo_ist.models import meteo_data, range_data
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import rangeSerializer
from datetime import date
import xlwt

class RangeViewSet(viewsets.ModelViewSet):
    queryset = range_data.objects.all()
    serializer_class = rangeSerializer

class GetMeteo(TemplateView):
    template_name = 'meteo.html'

    def get_context_data(self, *args, **kwargs):
        range_date, created = range_data.objects.all().get_or_create(id=1)
        start = getattr(range_date, 'start')
        end = getattr(range_date, 'end')

        variable = 'pp'
        parameters = {'type':'daily','start': start, 'end': end}
        url = 'http://caboruivo.tecnico.ulisboa.pt:64104/api/obs'
        response = requests.get(url, params = parameters)
        data = response.json()
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

def download_excel_data(request):

    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="MeteoData_IST.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['date','temp', 'pp', 'pres', 'rad', 'rh', 'wd', 'ws', 'wg',]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    range_date = range_data.objects.all().get(id=1)
    start = getattr(range_date, 'start')
    end = getattr(range_date, 'end')
    data = meteo_data.objects.filter(date__gte = start, date__lte = end) #dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.date.strftime('%Y-%m-%d'), font_style)
        ws.write(row_num, 1, my_row.temp, font_style)
        ws.write(row_num, 2, my_row.pp, font_style)
        ws.write(row_num, 3, my_row.pres, font_style)
        ws.write(row_num, 4, my_row.rad, font_style)
        ws.write(row_num, 5, my_row.rh, font_style)
        ws.write(row_num, 6, my_row.wd, font_style)
        ws.write(row_num, 7, my_row.ws, font_style)
        ws.write(row_num, 8, my_row.wg, font_style)

    wb.save(response)
    return response
