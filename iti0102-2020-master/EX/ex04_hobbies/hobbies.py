"""Hobbies."""
import csv


def create_list_from_file(file):
    """
    Collect lines from given file into list.

    :param file: original file path
    :return: list of lines
    """
    ready_list = []
    with open(file, encoding='utf-8') as file:
        list_of_untouched_lines = file.readlines()
    for lines in list_of_untouched_lines:
        if "\n" in lines:
            lines = lines[:-1]
        ready_list.append(lines)
    return ready_list


def create_dictionary(file):
    """
    Create dictionary about given peoples' hobbies as Name: [hobby_1, hobby_2].

    :param file: original file path
    :return: dict
    """
    dictionary_of_values = {}
    list_of_values = sorted(create_list_from_file(file))
    for value in list_of_values:
        value = value.split(":")
        if value[0] in dictionary_of_values.keys():
            if value[1] not in dictionary_of_values.get(value[0]):
                dictionary_of_values[value[0]] += [value[1]]
        else:
            dictionary_of_values[value[0]] = [value[1]]
    return dictionary_of_values


def find_person_with_most_hobbies(file):
    """
    Find the person (or people) who have more hobbies than others.

    :param file: original file path
    :return: list
    """
    list_of_people_with_most_values = []
    dict_of_values = create_dictionary(file)
    the_max_length_values = max(dict_of_values.values(), key=len)
    for key, value in dict_of_values.items():
        if len(value) == len(the_max_length_values):
            list_of_people_with_most_values.append(key)
    return list_of_people_with_most_values


def find_person_with_least_hobbies(file):
    """
    Find the person (or people) who have less hobbies than others.

    :param file: original file path
    :return: list
    """
    list_of_people_with_least_values = []
    dict_of_values = create_dictionary(file)
    the_min_length_values = min(dict_of_values.values(), key=len)
    for key, value in dict_of_values.items():
        if len(value) == len(the_min_length_values):
            list_of_people_with_least_values.append(key)
    return list_of_people_with_least_values


def find_most_popular_hobby(file):
    """
    Find the most popular hobby.

    :param file: original file path
    :return: list
    """
    new_dict = {}
    list_to_return = []
    dict_of_lines = create_dictionary(file)
    for values in dict_of_lines.values():
        for value in values:
            if value in new_dict.keys():
                new_dict[value] += 1
            else:
                new_dict[value] = 1
    for key, val in new_dict.items():
        if val == max(new_dict.values()):
            list_to_return.append(key)
    return list_to_return


def find_least_popular_hobby(file):
    """
    Find the least popular hobby.

    :param file: original file path
    :return: list
    """
    new_dict = {}
    list_to_return = []
    dict_of_lines = create_dictionary(file)
    for values in dict_of_lines.values():
        for value in values:
            if value in new_dict.keys():
                new_dict[value] += 1
            else:
                new_dict[value] = 1
    for key, val in new_dict.items():
        if val == min(new_dict.values()):
            list_to_return.append(key)
    return list_to_return


def write_corrected_database(file, file_to_write):
    """
    Write .csv file in a proper way. Use collected and structured data.

    :param file: original file path
    :param file_to_write: file to write result
    """
    with open(file_to_write, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        name = "Name"
        hobbies = "Hobbies"
        writer.writerow([name, hobbies])
        # your code goes here
        given_dict = create_dictionary(file)
        for key, value in given_dict.items():
            writer.writerow([key, "-".join(value)])


# These examples are based on a given text file from the exercise.


if __name__ == '__main__':
    dic = create_dictionary("hobbies_database.txt")
    print(len(create_list_from_file("hobbies_database.txt")))  # -> 100
    print("Check presence of hobbies for chosen person:")
    print("shopping" in dic["Wendy"])  # -> True
    print("fitness" in dic["Sophie"])  # -> False
    print("gaming" in dic["Peter"])  # -> True
    print("Check if hobbies - person relation is correct:")
    print("Check if a person(people) with the biggest amount of hobbies is(are) correct:")
    print(find_person_with_most_hobbies("hobbies_database.txt"))  # -> ['Jack']
    print(len(dic["Jack"]))  # ->  12
    print(len(dic["Carmen"]))  # -> 10
    print("Check if a person(people) with the smallest amount of hobbies is(are) correct:")
    print(find_person_with_least_hobbies("hobbies_database.txt"))  # -> ['Molly']
    print(len(dic["Molly"]))  # -> 5
    print(len(dic["Sophie"]))  # -> 7
    print("Check if the most popular hobby(ies) is(are) correct")
    print(find_most_popular_hobby("hobbies_database.txt"))  # -> ['gaming', 'sport', 'football']
    print("Check if the least popular hobby(ies) is(are) correct")
    print(find_least_popular_hobby("hobbies_database.txt"))  # -> ['tennis', 'dance', 'puzzles', 'flowers']
    write_corrected_database("hobbies_database.txt", 'correct_hobbies_database.csv')
