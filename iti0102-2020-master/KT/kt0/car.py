"""Car operations."""


class Car:
    """Car object."""

    def __init__(self, model, year, price):
        """Car constructor."""
        self.year = year
        self.model = model
        self.price = price

    def __str__(self):
        return {"year": self.year, "model": self.model, "price": self.price}


def create_car(model: str, price: int) -> Car:
    """
    Create a new car object with the current year if price is above 0.
    """
    current_year = 2020
    if price > 0:
        return Car(current_year, model, price)


def get_most_expensive_car_below_price(cars: list, max_price: int) -> Car:
    """
    Return the most expensive car with the price lower than max_price.

    If several cars have the same price, return the first.
    If there are no cars with which have the price lower than max_price, return None.
    """
    maximum = 0
    car_to_return = object
    updated_list = []
    for car in cars:
        if car.price < max_price:
            updated_list.append(car)
    if not updated_list:
        return None
    for car_ in updated_list:
        if car_.price > maximum:
            maximum = car_.price
            car_to_return = car_
    return car_to_return


def update_prices(cars: list, discount_per_year: int) -> None:
    """
    Update each car price so that for every year of their age they get discount_per_year lower price.

    If the car year is 2018 and currently it's 2020, then the discount is applied twice.
    The car price can never go below 0.

    Example:
        Currently it's 2020

        Car year is 2015
        Car price is 100
        discount_per_year = 5
        The new price for the car is 75

        Car year is 2000, price is 100, discount_per_year = 7
        The new price for the car is 0.
    """
    current_year = 2020
    for car in cars:
        if car.year == 2018:
            new_price = car.price - ((current_year - car.year) * discount_per_year * 2)
        else:
            new_price = car.price - ((current_year - car.year) * discount_per_year)
        if new_price < 0:
            new_price = 0
        car.price = new_price
    return None


def get_cars_with_model(cars: list, model: str) -> list:
    """Return list of cars with the given model."""
    list_based_on_model = []
    for car in cars:
        if car.model == model:
            list_based_on_model.append(car)
    return list_based_on_model


def get_ordered_cars(cars: list) -> list:
    """Return a new sorted list of cars by: year (newer first), price (cheaper first), model (from a to z)."""
    new_cars = sorted(cars, key=lambda x: (x.year, x.price, x.model), reverse=True)
    return new_cars
