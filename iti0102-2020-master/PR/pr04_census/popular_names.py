"""Order names by popularity."""


def read_from_file() -> list:  #
    """
    Create the list of all the names.

    :return: list
    """
    names = []
    with open("popular_names.txt", encoding='utf-8') as file:
        for line in file:
            names.append(line.strip())
    return names


def to_dictionary(names: list) -> dict:
    """
    Make a dictionary from a list of names.

    :param names: list of all the names
    :return: dictionary {"name:sex": number}
    """
    dictionary = {}
    for name in names:
        if name in dictionary.keys():
            dictionary[name] += 1
        else:
            dictionary[name] = 1
    return dictionary


def to_sex_dicts(names_dict: dict) -> tuple:
    """
    Divide the names by sex to 2 different dictionaries.

    :param names_dict: dictionary of names
    :return: two dictionaries {"name": number}, {"name": number}
    first one is male names, seconds is female names.
    """
    dict_of_males = {}
    dict_of_females = {}
    for key, values in names_dict.items():
        key = key.split(":")  # key[0] - nimi; key[1] - sugu.
        if key[1] == "M":
            dict_of_males[key[0]] = values
        else:
            dict_of_females[key[0]] = values
    return dict_of_males, dict_of_females


def most_popular(names_dict: dict) -> str:
    """
    Find the most popular name in the dictionary.

    If the dictionary is empty, return "Empty dictionary."
    :param names_dict: dictionary of names (key is name, value is count)
    :return: string
    """
    if len(names_dict) == 0:
        return "Empty dictionary."
    list_of_numbers = []
    for values in names_dict.values():
        list_of_numbers.append(values)
    max_number = max(list_of_numbers)
    for keys, value in names_dict.items():
        if value == max_number:
            return keys


def number_of_people(names_dict: dict) -> int:
    """
    Calculate the number of people in the dictionary.

    :param names_dict: dictionary of names (key is name, value is count)
    :return: int
    """
    summary = 0
    for values in names_dict.values():
        summary += values
    return summary


def names_by_popularity(names_dict: dict) -> str:
    r"""
    Create a string used to print the names by popularity.

    Format:
        1. name: number of people + "\n"
        ...
    Example:
        1. Kati: 100
        2. Mati: 90
        3. Nati: 80
        ...
    :param names_dict: dictionary of the names (key is name, value is count)
    :return: string
    """
    # Sain natukene abi sõnastiku filtreerimise kohta siit.
    # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/#:~:text=To%20sort%20a%20dictionary%20by%20value%20in%20Python%20you%20can,Dictionaries%20are%20unordered%20data%20structures.
    string = ''
    counter = 1
    sorted_tuple_of_names_and_values = sorted(names_dict.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_tuple_of_names_and_values:
        string += f"{counter}. {i[0]}: {i[1]}\n"
        counter += 1
    return string


if __name__ == '__main__':
    example_names = ("Kati:F\n" * 1000 + "Mati:M\n" * 800 + "Mari:F\n" * 600 + "Tõnu:M\n" * 400 + "Andrei:M\n" * 800)\
        .rstrip("\n").split("\n")
    people = to_dictionary(example_names)
    print(people)  # -> {'Kati:F': 1000, 'Mati:M': 800, 'Mari:F': 600, 'Tõnu:M': 400}
    male_names, female_names = to_sex_dicts(people)
    print(to_sex_dicts(people))
    print(male_names)  # -> {'Mati': 800, 'Tõnu': 400}
    print(female_names)  # -> {'Kati': 1000, 'Mari': 600}
    print(most_popular(male_names))  # -> "Mati"
    print(number_of_people(people))  # -> 2800
    print(names_by_popularity(male_names))  # ->   1. Mati: 800
#                                                  2. Tõnu: 400
#                                                  (empty line)
    print(names_by_popularity({}))
