class CarService:
    def __init__(self,cars):
        self.cars = cars
        
    def listCars(self):
        for car in self.cars:
            print("Car id:",car.id,
                  "price per day:", car.price_per_day,
                  "price per km:", car.price_per_km)
