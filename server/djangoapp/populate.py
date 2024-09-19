from .models import CarMake, CarModel
from datetime import date


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(name=data['name'], description=data['description'])
        )

    
    car_model_data = [
        {
            "name": "Pathfinder", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[0], "dealer_id": 1
        },
        {
            "name": "Qashqai", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[0], "dealer_id": 1
        },
        {
            "name": "XTRAIL", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[0], "dealer_id": 1
        },
        {
            "name": "A-Class", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[1], "dealer_id": 2
        },
        {
            "name": "C-Class", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[1], "dealer_id": 2
        },
        {
            "name": "E-Class", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[1], "dealer_id": 2
        },
        {
            "name": "A4", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[2], "dealer_id": 3
        },
        {
            "name": "A5", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[2], "dealer_id": 3
        },
        {
            "name": "A6", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[2], "dealer_id": 3
        },
        {
            "name": "Sorrento", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[3], "dealer_id": 4
        },
        {
            "name": "Carnival", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[3], "dealer_id": 4
        },
        {
            "name": "Cerato", "type": "Sedan", "year": date(2023, 1, 1),
            "make": car_make_instances[3], "dealer_id": 4
        },
        {
            "name": "Corolla", "type": "Sedan", "year": date(2023, 1, 1),
            "make": car_make_instances[4], "dealer_id": 5
        },
        {
            "name": "Camry", "type": "Sedan", "year": date(2023, 1, 1),
            "make": car_make_instances[4], "dealer_id": 5
        },
        {
            "name": "Kluger", "type": "SUV", "year": date(2023, 1, 1),
            "make": car_make_instances[4], "dealer_id": 5
        },
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'], make=data['make'], type=data['type'],
            year=data['year'], dealer_id=data['dealer_id']
        )
