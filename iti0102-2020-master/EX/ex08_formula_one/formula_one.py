"""Formula One."""
import re
import csv


class Driver:
    """Driver class."""

    def __init__(self, name: str, team: str):
        """
        Driver constructor.

        Here you should save driver's results as dictionary,
        where key is race number and value is points from that race.
        You must also save driver's points into a variable "points".

        :param name: Driver name
        :param team: Driver team
        """
        self.name = name
        self.team = team
        self._results = {}
        self._points = 0

    def get_results(self) -> dict:
        """
        Get all driver's results.

        :return: Results as dictionary
        """
        return self._results

    def get_points(self) -> int:
        """
        Return calculated driver points.

        :return: Calculated points
        """
        return self._points

    def calculate_points(self) -> int:
        """Calculating logic of driver points."""
        counter = 0
        for value in self._results.values():
            counter += value
        return counter

    def set_points(self):
        """Set points for driver."""
        self._points = self.calculate_points()

    def add_result(self, race_number: int, points: int):
        """
        Add new result to dictionary of results.

        Dictionary is located in the constructor.

        :param race_number: Race number
        :param points: Number of points from the race
        """
        if race_number in self._results.keys():
            self._results[race_number] += points
        else:
            self._results[race_number] = points
        self.set_points()


class Race:
    """Race class."""

    def __init__(self, file):
        """
        Race constructor.

        Here you should keep data collected from file.
        You must read file rows to list.

        :param file: File with race data
        """
        self.file = file
        self.data = self.read_file_to_list()

    def read_file_to_list(self):
        """
        Read file data to list in constructor.

        First line shows number of races in data file.
        Rest of the data follows same rules. Each line consists of 'Driver Team Time Race'.
        There are 2 or more spaces between each 'category'.
        E.g. "Mika Häkkinen  McLaren-Mercedes      42069   3"

        If file does NOT exist, throw FileNotFoundError with message "No file found!".
        """
        try:
            final_list = []
            with open(self.file, encoding="utf-8") as file:
                for index, line in enumerate(file):
                    if "\n" in line:
                        line = line[:-1]
                    if index > 0:
                        dictionary = self.extract_info(line)
                        final_list.append(dictionary)
            return final_list

        except FileNotFoundError:
            raise FileNotFoundError("No file found!")

    @staticmethod
    def extract_info(line: str) -> dict:
        """
        Helper method for read_file_to_list.

        Here you should convert one data line to dictionary.
        Dictionary must contain following key-value pairs:
            'Name': driver's name as string
            'Team': driver's team as string
            'Time': driver's time as integer (time is always in milliseconds)
            'Diff': empty string
            'Race': race number as integer

        :param line: Data string
        :return: Converted dictionary
        """
        list_of_line = re.split(r"\s{2,}", line)
        return {"Name": list_of_line[0], "Team": list_of_line[1], "Time": int(list_of_line[2]), "Diff": "",
                "Race": int(list_of_line[3])}

    def filter_data_by_race(self, race_number: int) -> list:
        """
        Filter data by race number.

        :param race_number: Race number
        :return: Filtered race data
        """
        final_list = []
        for values in self.data:
            dict_race_number = values.get("Race")
            if dict_race_number == race_number:
                final_list.append(values)
        return final_list

    @staticmethod
    def format_time(time: str) -> str:
        """
        Format time from milliseconds to M:SS.SSS.

        format_time('12') -> 0:00.012
        format_time('1234') -> 0:01.234
        format_time('123456') -> 2:03.456

        :param time: Time in milliseconds
        :return: Time as M:SS.SSS string
        """
        time_as_integer = int(time)
        time_in_seconds = float("{:.3f}".format(time_as_integer / 1000))  # 123456 -> 123.456
        minutes = int(time_in_seconds // 60)  # 123.456 -> 2
        seconds_milliseconds = round(time_in_seconds - (60 * minutes), 3)  # 123.456 - 60 * 2 -> 3.456
        if seconds_milliseconds < 10:
            return f"{minutes}:0{'{:.3f}'.format(seconds_milliseconds)}"
        return f"{minutes}:{'{:.3f}'.format(seconds_milliseconds)}"

    @staticmethod
    def calculate_time_difference(first_time: int, second_time: int) -> str:
        """
        Calculate difference between two times.

        First time is always smaller than second time. Both times are in milliseconds.
        You have to return difference in format +M:SS.SSS

        calculate_time_difference(4201, 57411) -> +0:53.210

        :param first_time: First time in milliseconds
        :param second_time: Second time in milliseconds
        :return: Time difference as +M:SS.SSS string
        """
        difference_in_seconds = abs(first_time - second_time) / 1000
        minutes_difference = int(difference_in_seconds // 60)
        seconds_milliseconds_difference = difference_in_seconds - (60 * minutes_difference)
        if seconds_milliseconds_difference < 10:
            return f"+{minutes_difference}:0{'{:.3f}'.format(seconds_milliseconds_difference)}"
        return f"+{minutes_difference}:{'{:.3f}'.format(seconds_milliseconds_difference)}"

    @staticmethod
    def sort_data_by_time(results: list) -> list:
        """
        Sort results data list of dictionaries by 'Time'.

        :param results: List of dictionaries
        :return: Sorted list of dictionaries
        """
        # https://www.tutorialspoint.com/How-do-I-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-Python
        return sorted(results, key=lambda x: x["Time"])

    def get_results_by_race(self, race_number: int) -> list:
        """
        Final results by race number.

        This method combines the rest of the methods.
        You have to filter data by race number and sort them by time.
        You must also fill 'Diff' as time difference with first position.
        You must add 'Place' and 'Points' key-value pairs for each dictionary.

        :param race_number: Race number for filtering
        :return: Final dictionary with complete data
        """
        dictionary_of_points = {0: 25, 1: 18, 2: 15, 3: 12, 4: 10, 5: 8, 6: 6, 7: 4, 8: 2, 9: 1}
        sorted_data_by_race_time = self.sort_data_by_time(self.filter_data_by_race(race_number))
        first_place_time = sorted_data_by_race_time[0].get("Time")
        for index, lines in enumerate(sorted_data_by_race_time):
            if "Points" not in lines.keys():
                if index > 9:
                    lines["Points"] = 0
                else:
                    lines["Points"] = dictionary_of_points.get(index)
            if "Place" not in lines.keys():
                lines["Place"] = index + 1
            for key in lines.keys():
                if key == "Diff":
                    drivers_pos = lines.get("Time")
                    if index != 0:
                        lines[key] = self.calculate_time_difference(first_place_time, drivers_pos)
                    lines["Time"] = self.format_time(drivers_pos)
                    break
        return sorted_data_by_race_time


class FormulaOne:
    """FormulaOne class."""

    def __init__(self, file):
        """
        FormulaOne constructor.

        It is reasonable to create Race instance here to collect all data from file.

        :param file: File with race data
        """
        self.file = file

    def write_race_results_to_file(self, race_number: int):
        """
        Write one race results to a file.

        File name is 'results_for_race_{race_number}.txt'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        race = Race(self.file)
        with open(f"results_for_race_{race_number}.txt", "w+", encoding="utf-8") as file:
            file.write("PLACE     NAME                     TEAM                     TIME           DIFF           "
                       "POINTS")
            file.write("\n")
            file.write("-" * 96)
            file.write("\n")
            for x in race.get_results_by_race(race_number):
                file.write(
                    "{0}{1}{2}{3}{4}{5}\n".format(str(x.get("Place")) + " " * (10 - len(str(x.get("Place")))),
                                                  x.get("Name") + " " * (25 - len(x.get("Name"))),
                                                  x.get("Team") + " " * (25 - len(x.get("Team"))),
                                                  x.get("Time") + " " * (15 - len(x.get("Time"))),
                                                  x.get("Diff") + " " * (15 - len(x.get("Diff"))),
                                                  str(x.get("Points")) + " " * (6 - len(str(x.get("Points"))))))

    def write_race_results_to_csv(self, race_number: int):
        """
        Write one race results to a csv file. Hello.

        File name is 'race_{race_number}_results.csv'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        race = Race(self.file)
        with open(f"race_{race_number}_results.csv", "w", encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(["Place", "Name", "Team", "Time", "Diff", "Points", "Race"])
            for z in race.get_results_by_race(race_number):
                writer.writerow([str(z.get("Place")), z.get("Name"), z.get("Team"),
                                 z.get("Time"), z.get("Diff"), z.get("Points"),
                                 race_number])

    def write_championship_to_file(self):
        """
        Write championship results to file.

        It is reasonable to create Driver class instance for each unique driver name and collect their points
        using methods from Driver class.
        Exact specifications are described in the text.
        """
        race = Race(self.file)
        amount_of_races = []
        for lines in race.read_file_to_list():
            amount_of_races.append(lines.get("Race"))
        amount_of_races = list(set(amount_of_races))
        max_races = max(amount_of_races)
        list_of_drivers = []
        with open("championship_results.txt", "w", encoding="utf-8") as file:
            for values in race.read_file_to_list():
                if len(list_of_drivers) < len(race.read_file_to_list()) / max_races:
                    driver = Driver(values.get("Name"), values.get("Team"))
                    list_of_drivers.append(driver)

            for index in range(1, max_races + 1):
                for lines in race.get_results_by_race(index):
                    for drivers in list_of_drivers:
                        if lines.get("Name") == drivers.name:
                            drivers.add_result(index, lines.get("Points"))
                            drivers.set_points()
                            break

            list_of_sorted_drivers = sorted(list_of_drivers, key=lambda y: y.calculate_points(), reverse=True)
            file.write("PLACE     NAME                     TEAM                     POINTS")
            file.write("\n")
            file.write("-" * 66)
            file.write("\n")
            for index, x in enumerate(list_of_sorted_drivers):
                file.write("{0}{1}{2}{3}\n".format(str(index + 1) + " " * (10 - len(str(index + 1))),
                                                   x.name + " " * (25 - len(x.name)),
                                                   x.team + " " * (25 - len(x.team)),
                                                   str(x.get_points()) + " " * (6 - len(str(x.get_points())))))


if __name__ == '__main__':
    f1 = FormulaOne("example.txt")
