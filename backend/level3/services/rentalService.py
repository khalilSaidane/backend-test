import datetime
from models.rental import Rental
from itertools import count
from models.commission import Commission


class RentalService:
    _ids = count(1)

    def __init__(self, rentals, cars):
        self.rentals = rentals
        self.cars = cars

    def rentCar(self, rental):
        car = self.getCarById(rental.car_id)
        rent_period = datetime.datetime.strptime(rental.end_date, '%Y-%m-%d').date() - datetime.datetime.strptime(
            rental.start_date, '%Y-%m-%d').date()
        rent_days = rent_period.days + 1
        price = rent_days * car.price_per_day + rental.distance * car.price_per_km

        price = self.decreasePrice(price, rent_days, car, rental)

        totalCommission = 0.3 * price
        insurance_fee = totalCommission / 2
        assistance_fee = rent_days * 100
        drivy_fee = totalCommission - (insurance_fee + assistance_fee)
        commission = Commission(insurance_fee, assistance_fee, drivy_fee)

        return Rental(rental.id, price, commission)


    def getCarById(self,car_id):
        for car in self.cars:
            if car.id == car_id:
                return car
        raise Exception("car with id:", car_id, "not found")

    def decreasePrice(self,price, rent_days, car, rental):
        if rent_days >= 11:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            days_price = 5 * (car.price_per_day * 0.7) + days_price
            days_price = (rent_days - 5) * (car.price_per_day * 0.5) + days_price
            price = days_price + rental.distance * car.price_per_km
        elif 5 <= rent_days < 11:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            days_price = (rent_days - 2) * (car.price_per_day * 0.7) + days_price
            price = days_price + rental.distance * car.price_per_km
        elif 2 <= rent_days < 5:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            price = days_price + rental.distance * car.price_per_km
        return price



