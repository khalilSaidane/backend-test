from services.carService import CarService
from services.rentalService import RentalService
import json
import datetime
from collections import namedtuple as NAMED_TUPLE
import json as JSON

#load data
with open('data/input.json') as f:
    data = json.load(f)
def _json_object_hook(data):
    """
    JSON Object Hook Configuration.
    """
    return NAMED_TUPLE(
        'X',
        data.keys()
    )(*data.values())
def json_to_object(data):
    """
    Convert JSON to Python Object.
    """
    return JSON.loads(
        JSON.dumps(data),
        object_hook=_json_object_hook
    )
with open('data/input.json') as f:
    if __name__ == '__main__':
        json_data = JSON.load(f)
        object_data = json_to_object(json_data)

carService = CarService(object_data.cars)
rentalService = RentalService(object_data.rentals,object_data.cars)

carService.listCars()

output = {"rentals":[]}
for rental in object_data.rentals:
    output['rentals'].append(rentalService.rentCar(rental))

def obj_dict(obj):
    return obj.__dict__

with open('data/output.json','w') as f:
    json.dump(output, f, indent=2,  default=obj_dict)


