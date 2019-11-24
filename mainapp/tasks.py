from celery import task
from .models import MainModel
from ESW_Campus_Energy_and_Demand_Dashboard.settings import OneM2M_IP
import requests
from datetime import datetime, timedelta

@task()
def import_values():
    model = MainModel()
    URL = "http://" + OneM2M_IP + "/~/in-cse/in-name/Team32_Campus_energy_and_demand_dashboard/pr_1_esp32_1/la/"
    headers = {
        "X-M2M-Origin": "admin:admin",
        "Accept": "application/json"
    }
    data = requests.get(URL, headers=headers).json()
    l = data['m2m:cin']['con'].split()
    model.temp = l[1]
    model.humidity = l[0]
    model.energy_1 = l[4]
    model.energy_2 = l[5]
    model.energy_3 = l[6]
    model.energy_4 = l[7]
    model.energy_5 = l[8]
    model.power_1 = l[3]
    model.power_2 = l[9]
    model.power_3 = l[10]
    model.power_4 = l[11]
    model.power_5 = l[12]
    model.save()


@task()
def delete_values():
    time_threshold = datetime.now() - timedelta(hours=24)
    MainModel.objects.filter(time__lt=time_threshold).delete()
