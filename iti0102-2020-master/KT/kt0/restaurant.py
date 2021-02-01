"""Restaurant system."""


class Restaurant:
    """Restaurant."""

    def __init__(self, name: str):
        """Restaurant constructor."""
        self.name = name
        self.dishes = []
        self.menus = []

    def add_dish(self, dish: 'Dish') -> bool:
        """Add a dish if not already in restaurant."""
        if dish not in self.dishes:
            self.dishes.append(dish)
            return True
        return False

    def get_dishes(self) -> list:
        """Return all the dishes in the restaurant."""
        return self.dishes

    def add_menu(self, menu: 'Menu') -> bool:
        """
        Add a menu to the restaurant if all the dishes are available.

        Menu cannot be added if:
        - it has no dishes
        - the menu with the same dishes (in any order) already exists
        """
        newer_list = []
        if menu not in self.menus and menu != []:
            for values in menu.dishes:
                if values in self.dishes:
                    newer_list.append(values)
            if newer_list == self.dishes:
                self.menus.append(menu)
                return True
        return False

    def get_menus(self) -> list:
        """Return all the menus in the restaurant."""
        return self.menus

    def get_dishes_available_in_menu(self) -> list:
        """Return unique dishes which are in one of the menus."""
        list_of_dishes = []
        for dish in self.dishes:
            if dish in self.menus and dish not in list_of_dishes:
                list_of_dishes.append(dish)
        return list_of_dishes

    def get_menus_ordered_by_price(self) -> list:
        """A new list of menus ordered by total price (highest first), then by dish count (lower first)."""

        new_menus = sorted(self.menus, key=lambda x: (x.price, len(x.dishes)))
        return new_menus


class Dish:
    """Dish (food)."""

    def __init__(self, name: str, price: int):
        """Dish constructor."""
        self.name = name
        self.price = price

    def get_name(self) -> str:
        """Return the name of the dish."""
        return self.name

    def get_price(self) -> int:
        """Return the price of the dish."""
        return self.price


class Menu:
    """Menu which holds different dishes."""

    def __init__(self):
        """Menu constructor."""
        self.dishes = []
        self.price = 0

    def add_dish(self, dish: Dish) -> bool:
        """Add dish to menu if it does not exist already."""
        if dish not in self.dishes:
            self.dishes.append(dish)
            self.price += dish.get_price()
            return True
        return False

    def get_dishes(self) -> list:
        """Return all the dishes in menu."""
        return self.dishes

    def compare_to(self, menu: 'Menu') -> bool:
        """
        Compare the current menu with the given menu.

        Menus are the same if:
        - they have the same dishes (instances)
        - they have the same dishes (name-price are the same)
        - the order is not important (menu A,B is the same as B,A)
        If the menus are the same, return True. Oterhwise False.
        """
        list_of_truth = []
        if isinstance(menu, Menu):
            for base_dishes in self.dishes:
                for given_dishes in menu.dishes:
                    if base_dishes.name == given_dishes.name and base_dishes.price == given_dishes.price:
                        list_of_truth.append(base_dishes)
            if list_of_truth == self.dishes:
                return True
        return False


if __name__ == '__main__':
    d1 = Dish("Pasta", 10)
    d2 = Dish("Pizza", 15)
    m1 = Menu()
    m1.add_dish(d1)
    m1.add_dish(d2)
    m2 = Menu()
    m2.add_dish(d1)
    m2.add_dish(d2)
    print(m1.compare_to(m2))
    r1 = Restaurant("Pizza-Fuego")
    r2 = Restaurant("Pasta-Macarena")
    r1.add_dish(d1)
    r1.add_dish(d2)
    r1.add_menu(m1)
    print(r1.get_menus_ordered_by_price())
