import datetime
from models.rental import Rental


class RentalService:
    def __init__(self, rentals, cars):
        self.rentals = rentals
        self.cars = cars

    def rentCar(self, rental):
        price = self.ComputePrice(rental)
        return Rental(rental.id,price)

    def getCarById(self,car_id):
        for car in self.cars:
            if car.id == car_id:
                return car
        raise Exception("car with id:", car_id, "not found")

    def ComputePrice(self, rental):
        car = self.getCarById(rental.car_id)
        rent_period = datetime.datetime.strptime(rental.end_date, '%Y-%m-%d').date() - datetime.datetime.strptime(rental.start_date, '%Y-%m-%d').date()
        return (rent_period.days + 1) * car.price_per_day + rental.distance * car.price_per_km

