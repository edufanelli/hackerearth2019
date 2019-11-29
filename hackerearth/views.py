from django.shortcuts import render
from .models import Failure

# Create your views here.
def load_scenario_data():
    import os
    from datetime import datetime
    print("No Failure history data detected. Importing...")
    data = open(os.getcwd()+"\\Scenario2f6bf40f.csv")
    data.readline()
    for line in data:
        failure = Failure(
            sensor = line.split(",")[0],
            timestamp = datetime.strptime(line.split(",")[1] + " " + line.split(",")[2], "%m-%d-%y %I:%M:%S %p"),
            conveyor_belt = line.split(",")[3],
            machine = line.split(",")[4],
            unit  = line.split(",")[5],
            group = line.split(",")[6],
            component = line.split(",")[7],
            failure_mode = line.split(",")[8],
            discipline = line.split(",")[9],
            comments = line.split(",")[10],
            delay_min = line.split(",")[11],
            avg_repair_time = line.split(",")[12],
            avg_repair_cost = line.split(",")[13].replace("\n", ""),
        )
        failure.save()

if len(Failure.objects.all()) == 0:
    load_scenario_data()

