import datetime
from models.rental import Rental
from itertools import count


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
        rent_days = rent_period.days + 1
        price = rent_days * car.price_per_day + rental.distance * car.price_per_km
        if rent_days >= 11:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            days_price = 5 * (car.price_per_day  * 0.7) + days_price
            days_price =(rent_days - 5) * (car.price_per_day  * 0.5) + days_price
            price = days_price + rental.distance * car.price_per_km
        elif 5 <= rent_days < 11:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            days_price =(rent_days - 2) * (car.price_per_day  * 0.7) + days_price
            price = days_price + rental.distance * car.price_per_km
        elif 2 <= rent_days < 5:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            price = days_price + rental.distance * car.price_per_km

        return price
