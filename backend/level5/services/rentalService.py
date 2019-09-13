import datetime
from models.rental import Rental
from itertools import count
from models.commission import Commission
from models.action import Action


class RentalService:

    def __init__(self, rentals, cars, options):
        self.rentals = rentals
        self.cars = cars
        self.options = options

    def rentCar(self, rental):
        car = self.getCarById(rental.car_id)
        rent_period = datetime.datetime.strptime(rental.end_date, '%Y-%m-%d').date() - datetime.datetime.strptime(
            rental.start_date, '%Y-%m-%d').date()
        rent_days = rent_period.days + 1
        price = rent_days * car.price_per_day + rental.distance * car.price_per_km

        price = self.decreasePrice(price, rent_days, car, rental)

        totalCommission = 0.3 * price
        owner_credit = price - totalCommission

        rental_options = []
        for option in self.options:
            if option.rental_id == rental.id:
                rental_options.append(option.type)
                new_values = self.computeOptionCost(totalCommission, owner_credit, option, rent_days)
                totalCommission = new_values["totalCommission"]
                owner_credit = new_values["owner_credit"]

        insurance_fee = totalCommission / 2
        assistance_fee = rent_days * 100
        drivy_fee = totalCommission - (insurance_fee + assistance_fee)
        commission = Commission(insurance_fee, assistance_fee, drivy_fee)

        actions = []

        actions.append(Action("driver", "debit", price))
        actions.append(Action("owner", "credit", owner_credit))
        actions.append(Action("insurance", "credit", insurance_fee))
        actions.append(Action("drivy", "credit", drivy_fee))
        actions.append(Action("assistance", "credit", assistance_fee))

        rental = Rental(rental.id, actions, rental_options)
        return rental



    def getCarById(self,car_id):
        for car in self.cars:
            if car.id == car_id:
                return car
        raise Exception("car with id:", car_id, "not found")

    def decreasePrice(self,price, rent_days, car, rental):
        if rent_days >= 11:
            days_price = car.price_per_day
            days_price += car.price_per_day * 0.9
            days_price += 5 * (car.price_per_day * 0.7)
            days_price += (rent_days - 5) * (car.price_per_day * 0.5)
            price = days_price + rental.distance * car.price_per_km
        elif 5 <= rent_days < 11:
            days_price = car.price_per_day
            days_price += car.price_per_day * 0.9
            days_price += (rent_days - 2) * (car.price_per_day * 0.7)
            price = days_price + rental.distance * car.price_per_km
        elif 2 <= rent_days < 5:
            days_price = car.price_per_day
            days_price = car.price_per_day * 0.9 + days_price
            price = days_price + rental.distance * car.price_per_km
        return price

    def computeOptionCost(self, totalCommission, owner_credit,option, rent_days):
        gps_euro_per_day = 5
        baby_seat_euro_per_day = 2
        additional_insurance_per_day = 10
        if option.type == "gps":
            owner_credit = owner_credit + gps_euro_per_day * rent_days
            totalCommission = totalCommission - gps_euro_per_day * rent_days
        elif option.type == "baby_seat":
            owner_credit = owner_credit + baby_seat_euro_per_day * rent_days
            totalCommission = totalCommission - baby_seat_euro_per_day * rent_days
        else:
            owner_credit = owner_credit - additional_insurance_per_day * rent_days
            totalCommission = totalCommission + additional_insurance_per_day * rent_days
        return {"totalCommission": totalCommission,
                "owner_credit": owner_credit}

