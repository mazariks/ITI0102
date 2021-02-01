"""Train Station."""


class Passenger:
    """Class Passenger."""

    def __init__(self, passenger_id: str, seat: str):
        """Passenger constructor."""
        self.id = passenger_id
        self.seat = seat

    def __str__(self):
        """Turn object appearance into string."""
        return {"id": self.id, "seat": self.seat}.__str__()

    @property
    def id(self) -> str:
        """
        Getter of the passenger ID.

        :return:
        """
        return self._id

    @property
    def seat(self) -> str:
        """
        Getter of the passenger's seat.

        :return:
        """
        return self._seat

    @id.setter
    def id(self, value: str):
        """
        Setter of the passenger's ID.

        :param value:
        :return:
        """
        self._id = value

    @seat.setter
    def seat(self, value: str):
        """
        Setter of the passenger's seat.

        :param value:
        :return:
        """
        self._seat = value


class Train:
    """Class Train."""

    def __init__(self, train_id: str, carriages: int, seats_in_carriage: int):
        """Class Train's constructor."""
        self.train_id = train_id
        self.carriages = carriages
        self.seats_in_carriage = seats_in_carriage
        self.passengers = []

    def __str__(self):
        """Make objects of Train class look nicer."""
        return {"train_id": self._train_id, "carriages": self._carriages, "seats in carraiages":
                self._seats_in_carriage, "passengers": self.passengers}

    @property
    def carriages(self) -> int:
        """
        Getter of number of carriages in train.

        :return:
        """
        return self._carriages

    @property
    def train_id(self) -> str:
        """
        Getter of train's ID.

        :return:
        """
        return self._train_id

    @property
    def seats_in_carriage(self) -> int:
        """
        Getter of seats in every carriage of the train.

        :return:
        """
        return self._seats_in_carriage

    def get_seats_in_train(self) -> int:
        """
        Find amount of seats in train.

        :return:
        """
        return self._carriages * self._seats_in_carriage

    def get_number_of_passengers(self) -> int:
        """
        Find amount of passengers in train.

        :return:
        """
        return len(self.passengers)

    def get_passengers_in_carriages(self) -> dict:
        """
        Put passengers into their carriages according to tickets.

        :return:
        """
        dictionary = {str(key): [] for key in range(1, self._carriages + 1)}
        for passenger in self.passengers:
            seat = passenger.seat.split("-")
            carriage = seat[1]
            for key in dictionary.keys():
                if key == carriage:
                    dictionary[key] += [passenger]
        return dictionary

    @train_id.setter
    def train_id(self, value: str):
        """
        Setter of train_id.

        :param value:
        :return:
        """
        self._train_id = value

    @carriages.setter
    def carriages(self, value: int):
        """
        Setter of carriages.

        :param value:
        :return:
        """
        self._carriages = value

    @seats_in_carriage.setter
    def seats_in_carriage(self, value: int):
        """
        Setter of seats in carriage.

        :param value:
        :return:
        """
        self._seats_in_carriage = value

    def add_passenger(self, passenger: Passenger) -> Passenger:
        """
        Add Passenger's object to the list of passengers in Train object.

        :param passenger:
        :return:
        """
        list_of_used_seats = []
        for x in self.passengers:
            list_of_used_seats.append(x.seat)
        if passenger.seat not in list_of_used_seats:
            splitted_seat = passenger.seat.split("-")  # 0 - train_id, 1 - carriage, 2 - seat in carriage.
            if splitted_seat[0] == self._train_id and 0 < int(splitted_seat[1]) <= self._carriages and \
                    0 < int(splitted_seat[2]) <= self._seats_in_carriage:
                self.passengers.append(passenger)
                return passenger


class TrainStation:
    """Class TrainStation."""

    def __init__(self, trains: list, passengers: list):
        """TrainStation constructor."""
        self.trains = trains
        self.passengers = passengers

    def __str__(self):
        """
        Make TrainStation's object look better.

        :return:
        """
        return {"trains": self._trains, "passengers": self._passengers}

    def get_station_overview(self) -> list:
        """
        Get the status of each train and its passengers inside.

        :return:
        """
        list_to_return = []  # [{"train_id": train_id, "carriages": carriages, "seats": kinni/kokku}]
        for x in self._trains:
            dictionary = {"train_id": x.train_id, "carriages": x.carriages, "seats": str(x.get_number_of_passengers())
                                                                            + "/" + str(x.get_seats_in_train())}
            list_to_return.append(dictionary)
        return list_to_return

    def get_number_of_passengers(self):
        """
        Return number of passengers in trains.

        :return:
        """
        return len(self._passengers)

    @property
    def passengers(self):
        """
        Getter of passengers in TrainStation.

        :return:
        """
        return self._passengers

    @passengers.setter
    def passengers(self, value_list: list):
        """
        Setter of passengers in TrainStation.

        :param value_list:
        :return:
        """
        valid_pass = []
        for train in self._trains:
            for passenger in value_list:
                if train.add_passenger(passenger):
                    valid_pass.append(passenger)
        self._passengers = valid_pass

    @property
    def trains(self):
        """
        Getter of trains in TrainStation.

        :return:
        """
        return self._trains

    @trains.setter
    def trains(self, value_list: list):
        """
        Setter of trains in TrainStation.

        :param value_list:
        :return:
        """
        self._trains = value_list


if __name__ == "__main__":
    # passengers
    p1 = Passenger("10", "AA-1-0")
    p2 = Passenger("11", "AA-1-1")
    p3 = Passenger("12", "AA-1-1")
    p4 = Passenger("13", "AA-1-2")
    p5 = Passenger("14", "AA-2-5")
    p6 = Passenger("15", "AB-2-4")
    p7 = Passenger("16", "AB-10-4")
    p8 = Passenger("17", "AB-0-0")
    passengers = [p1, p2, p3, p4, p5, p6, p7, p8]
    valid_passengers = [p2, p4, p5, p6]

    # trains
    t1 = Train("AA", 5, 5)
    t2 = Train("AB", 2, 4)
    trains = [t1, t2]

    # stations
    s1 = TrainStation(trains, passengers)
    stations = [s1]
