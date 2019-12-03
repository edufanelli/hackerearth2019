from django.shortcuts import render
from .models import Failure
from .models import Client
from .models import Product
from .models import Order
from .models import Conveyor_belt
from .models import Alocation
from .models import Conversation_bot_context

# Create your views here.
def load_scenario_data():
    import os
    from datetime import datetime
    print("No Failure history data detected. Importing...")
    data = open(os.getcwd()+"/failure.csv")
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
            avg_repair_cost = line.split(",")[13],
            status = line.split(",")[14].replace("\n", ""),
        )
        failure.save()

    print("No Client history data detected. Importing...")
    data = open(os.getcwd()+"/client.csv")
    data.readline()
    for line in data:
        client = Client(
            name = line.split(",")[0].replace("\n", ""),
         )
        client.save()

    print("No Product history data detected. Importing...")
    data = open(os.getcwd()+"/product.csv")
    data.readline()
    for line in data:
        product = Product(
            name = line.split(",")[0],
            production_time = line.split(",")[1].replace("\n", ""),
         )
        product.save()

    print("No Order history data detected. Importing...")
    data = open(os.getcwd()+"/order.csv")
    data.readline()
    for line in data:
        order = Order(
 	      order_number = line.split(",")[0],
          client = line.split(",")[1],
          product = line.split(",")[2],
          quantity = line.split(",")[3],
          deadline = line.split(",")[4],
          status = line.split(",")[5].replace("\n", ""),
          )
        order.save()

    print("No Conveyor_belt history data detected. Importing...")
    data = open(os.getcwd()+"/conveyor_belt.csv")
    data.readline()
    for line in data:
        conveyor_belt = Conveyor_belt(
            conveyor_belt = line.split(",")[0].replace("\n", ""),
         )
        conveyor_belt.save()

if len(Failure.objects.all()) == 0:
    load_scenario_data()
