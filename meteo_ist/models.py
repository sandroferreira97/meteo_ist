from django.db import models
from datetime import date, timedelta

# Create your models here.
class meteo_data(models.Model):
    date = models.DateField(primary_key=True, max_length=60, blank=True)
    pp = models.CharField(max_length=60, default='', null= True)
    pres = models.CharField(max_length=60, default='', null= True)
    rad = models.CharField(max_length=60, default='', null= True)
    rh = models.CharField(max_length=60, default='', null= True)
    temp = models.CharField(max_length=60, default='', null= True)
    wd = models.CharField(max_length=60, default='', null= True)
    wg = models.CharField(max_length=60, default='', null= True)
    ws = models.CharField(max_length=60, default='', null= True)

class range_data(models.Model):
    start = models.DateField(max_length=60, default=date.today() - timedelta(days=20), null=True)
    end = models.DateField(max_length=60, default=date.today(), null=True)
    
 