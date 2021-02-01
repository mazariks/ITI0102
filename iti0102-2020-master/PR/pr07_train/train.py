"""Train."""


class Train:
    """Class Train."""

    def __init__(self, passengers: list, carriages: int, seats_in_carriage: int):
        """
        Constructor of class Train.

        :param passengers:
        :param carriages:
        :param seats_in_carriage:
        """
        self.carriages = carriages
        self.seats_in_carriage = seats_in_carriage
        self.passengers = passengers

    @property
    def passengers(self) -> list:
        """
        Getter of passengers.

        :return:
        """
        return self._passengers

    @property
    def carriages(self) -> int:
        """
        Getter of carriages.

        :return:
        """
        return self._carriages

    @property
    def seats_in_carriage(self) -> int:
        """
        Getter of seats in every carriage.

        :return:
        """
        return self._seats_in_carriage

    def get_seats_in_train(self) -> int:
        """
        Amount of seats in train overall.

        :return:
        """
        return self._seats_in_carriage * self._carriages

    def get_number_of_passengers(self) -> int:
        """
        Amount of passengers in a train.

        :return:
        """
        return len(self._passengers)

    def get_passengers_in_carriages(self) -> dict:
        """
        Sort passengers within carriages of train.

        :return:
        """
        dictionary = {}
        for passenger in self.passengers:
            seat = passenger.seat.split("-")
            carriage = seat[0]
            seat_in_carriage = seat[1]
            new_object = {"id": passenger.id, "seat": seat_in_carriage}
            for carriage_in_train in range(1, self.carriages + 1):
                carriage_as_str = str(carriage_in_train)
                if carriage_in_train == int(carriage):
                    if carriage_as_str in dictionary.keys():
                        dictionary[carriage_as_str] += [new_object]
                    else:
                        dictionary[carriage_as_str] = [new_object]
                else:
                    if carriage_as_str not in dictionary.keys():
                        dictionary[carriage_as_str] = []
        return dictionary

    @passengers.setter
    def passengers(self, value_list: list):
        """
        Setter of passengers' list.

        :param value_list:
        :return:
        """
        list_of_invalid_passengers = []
        #  Set the new value to the self.passengers by tickets.
        for x in value_list:
            y = x.seat.split("-")
            if int(y[0]) > self._carriages or int(y[1]) > self._seats_in_carriage:
                list_of_invalid_passengers.append(x)
        self._passengers = list(set(value_list) - set(list_of_invalid_passengers))

    @carriages.setter
    def carriages(self, value: int):
        """
        Setter of amount of carriages.

        :param value:
        :return:
        """
        self._carriages = value

    @seats_in_carriage.setter
    def seats_in_carriage(self, value: int):
        """
        Setter of seats in every carriage.

        :param value:
        :return:
        """
        self._seats_in_carriage = value


class Passenger:
    """Class Passenger."""

    def __init__(self, passenger_id: str, seat: str):
        """
        Constructor of Passenger's class.

        :param passenger_id:
        :param seat:
        """
        self.id = passenger_id
        self.seat = seat

    def __dict__(self):
        """
        Simplify view of class Passenger.

        :return:
        """
        return {"id": self.id, "seat": self.seat}


if __name__ == '__main__':
    p_1 = Passenger('123', '1-9')
    p_2 = Passenger('321', '2-11')
    p_3 = Passenger('456', '4-5')
    t = Train([p_1, p_2, p_3], 3, 10)
    print(t.get_passengers_in_carriages())
    print(t.get_number_of_passengers())
