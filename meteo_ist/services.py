import os
from meteo_ist.models import meteo_data, range_data
from django.utils.dateparse import parse_date

def upload_db(data):
    for i in range(0, len(data['datetime'])):
        date = parse_date(data['datetime'][i])     # parse string do date format
        pp = data['data']['pp'][i]
        pres = data['data']['pres'][i]
        rad = data['data']['rad'][i]
        rh = data['data']['rh'][i]
        temp = data['data']['temp'][i]
        wd = data['data']['wd'][i]
        wg = data['data']['wg'][i]
        ws = data['data']['ws'][i]


        b = meteo_data(date, pp, pres, rad, rh, temp, wd, wg, ws)
        b.save()
