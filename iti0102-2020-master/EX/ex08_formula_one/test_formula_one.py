"""Test FormulaOne."""
import csv
import pytest
from formula_one import Driver, Race, FormulaOne
import random

file = "example.txt"
race = Race(file)
f1 = FormulaOne(file)


def test_get_results():
    """Testing of how drivers get their results."""
    d1 = Driver("Andrew", "Audi A6")
    assert type(d1.get_results()) == dict
    assert d1.get_results() == {}
    d1.add_result(1, 25)
    assert d1.get_results() == {1: 25}
    d2 = Driver("Werdna", "6A Idua")
    assert d2.get_results() == {}
    d2.add_result(1, int(random.random()) + 1)
    assert d1.get_results() != d2.get_results()


def test_get_points():
    """Testing of how dirvers get their points."""
    d1 = Driver("Andrew", "Audi A6")
    initial_points = d1.get_points()
    assert type(d1.get_points()) == int
    assert d1.get_points() == 0
    d1.add_result(1, 18)
    assert d1.get_points() == 18
    d1.add_result(1, 25)
    assert d1.get_points() == 43
    assert initial_points != d1.get_points()


def test_calculate_points():
    """Testing of logic of calculating driver's points."""
    d1 = Driver("Andrew", "Audi A6")
    assert type(d1.calculate_points()) == int
    assert d1.calculate_points() == 0
    d1.add_result(1, 25)
    assert d1.calculate_points() == 25
    d1.add_result(2, int(random.random()) + 1)
    assert d1.calculate_points() > 25


def test_add_result():
    """Testing of how results are added to drivers."""
    d1 = Driver("Andrew", "Audi A6")
    assert d1.get_results() == {}
    d1.add_result(1, 18)
    assert 18 in d1.get_results().values()
    assert 1 in d1.get_results().keys()
    assert d1.get_results() == {1: 18}
    d1.add_result(3, 10)
    assert 18 and 10 in d1.get_results().values()
    assert 1 and 3 in d1.get_results().keys()
    assert d1.get_results() == {1: 18, 3: 10}
    assert random.random() not in d1.get_results().items()


def test_read_file_to_list():
    """Testing reading data from file."""
    new_file = "Hello,World"
    data = race.read_file_to_list()
    assert type(data) == list
    for x in data:
        assert type(x) == dict
    assert len(data) == 33
    with pytest.raises(FileNotFoundError):
        Race(new_file).read_file_to_list()


def test_extract_info():
    """Testing of how dicts of drivers are being made."""
    string = "Mika Hakkinen  Mclaren-Mercedes   79694  1"
    assert type(race.extract_info(string)) == dict
    assert race.extract_info(string) == {"Name": "Mika Hakkinen", "Team": "Mclaren-Mercedes", "Time": 79694, "Diff": "",
                                         "Race": 1}
    assert "Hello, world!" not in race.extract_info(string)


def test_filter_data_by_race():
    """Testing of how drivers' data is being filtered by specific race."""
    data = race.filter_data_by_race(random.randint(1, 3))
    assert len(data) == 11
    assert type(data) == list
    for datum in data:
        assert type(datum) == dict


def test_format_time():
    """Testing of how time in milliseconds is formatted into correct format."""
    number = random.randint(10000, 99999)
    formatted_number = race.format_time(str(number))
    assert type(formatted_number) == str
    assert ":" in formatted_number and "." in formatted_number


def test_calculate_time_difference():
    """Testing of how difference of time of the drivers is calculated."""
    first_position = 1
    second_position = 1235
    difference = race.calculate_time_difference(first_position, second_position)
    assert type(difference) == str
    assert ":" in difference and "." in difference
    first_position_random = random.randint(10000, 99999)
    second_position_random = random.randint(10000, 99999)
    difference_random = race.calculate_time_difference(first_position_random, second_position_random)
    assert type(difference_random) == str
    assert ":" in difference_random and "." in difference_random


def test_sort_data_by_time():
    """Testing of how drivers' data is sorted by time."""
    data = race.read_file_to_list()
    sorted_data = race.sort_data_by_time(data)
    assert data != sorted_data
    assert len(data) == len(sorted_data)
    assert type(sorted_data) == list
    for lines in sorted_data:
        assert type(lines) == dict


def test_get_results_by_race():
    """Testing of getting all drivers results in a specific race."""
    data = race.get_results_by_race(random.randint(1, 3))
    assert type(data) == list
    for lines in data:
        assert type(lines) == dict
        assert len(lines) == 7
        assert "Points" in lines.keys() and "Place" in lines.keys()
    assert len(data) == 11


def test_write_race_results_to_file():
    """Testing of writing specific race's results into a text file as a beautiful table."""
    number = random.randint(1, 3)
    f1.write_race_results_to_file(number)
    with open(f"results_for_race_{number}.txt", encoding="utf-8") as opened_file:
        list_of_lines = opened_file.readlines()
        assert len(list_of_lines) == 13


def test_write_race_results_to_csv():
    """Testing writing data of specific race into csv file."""
    number = random.randint(1, 3)
    f1.write_race_results_to_csv(number)
    with open(f"race_{number}_results.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            assert len(row) == 7


def test_write_championship_to_file():
    """Testing of writing whole results to a table."""
    f1.write_championship_to_file()
    with open("championship_results.txt") as new_file:
        list_of_lines = new_file.readlines()
        assert len(list_of_lines) == 13
