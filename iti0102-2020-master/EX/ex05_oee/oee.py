"""EX05 - OEE."""
import csv


def read_production_data(filename: str) -> dict:
    """
    Open the file in the provided path, read in values and return them as a dictionary.

    where the key is the machine name and value is a list of integers for the production data for each shift.
    {
    'Machine Name': [Run Time (minutes), Ideal Run Rate (pcs/min), Total Count (pcs), Good Count (pcs)]
    }

    :param filename: string file path for the CSV file to be read
    :return: dictionary with the production data per machine
    """
    list_with_editing = []
    ready_dict = {}
    try:
        with open(filename, encoding='utf-8') as file:
            list_without_editing = file.readlines()
        for predefined_items in list_without_editing:
            if '\n' in predefined_items:
                predefined_items = predefined_items[:-1]
                list_with_editing.append(predefined_items)
            else:
                list_with_editing.append(predefined_items)
        for edited_items in list_with_editing:
            items_parts = edited_items.split(",")  # 0 - Machine name; 1 - Run time(minutes);
            # 2 - Ideal run rate(pcs/min); # 3 - Total count (pcs), 4 - Good count (pcs)
            ready_dict[items_parts[0]] = [int(items_parts[1]), int(items_parts[2]), int(items_parts[3]),
                                          int(items_parts[4])]
        return ready_dict
    except FileNotFoundError:
        return {}


def calculate_quality(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Quality percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Quality.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Quality value per machine
    """
    dict_of_qualities = {}
    for machine_name, values in production_data.items():
        # values[2] - Total; values[3] - Good. Quality = Good / Total * 100%.
        if values[2] == 0:
            dict_of_qualities[machine_name] = 0.0
        else:
            dict_of_qualities[machine_name] = round(values[3] / values[2], 3) * 100
    return dict_of_qualities


def calculate_availability(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Availability percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Availability.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Availability value per machine
    """
    length_of_workday = 420  # 7 tundi korrutatud 8-ga.
    dict_of_availabilities = {}
    for machine_name, values in production_data.items():
        # values[0] - Run time. Availability = Run time / length_of_day * 100%
        dict_of_availabilities[machine_name] = round(values[0] / length_of_workday, 3) * 100
    return dict_of_availabilities


def calculate_performance(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Performance percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Performance.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Performance value per machine
    """
    dict_of_performances = {}
    for machine_name, values in production_data.items():
        # values[0] - run time; values[1] - ideal run rate; values[2] - total count.
        # Performance = (Total Count / Run Time) / Ideal Run Rate
        if values[0] == 0 or values[1] == 0:
            dict_of_performances[machine_name] = 0.0
        else:
            dict_of_performances[machine_name] = float("{:.1f}".format(values[2] / values[0] / values[1] * 100))
    return dict_of_performances


def calculate_oee(production_data: dict) -> dict:
    """
    Using the previously defined functions, calculate the final OEE percentage for each machine.

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Performance.
    Return the newly created dictionary.

    :return: dictionary with OEE percentage value per machine
    """
    dict_of_qualities = calculate_quality(production_data)
    dict_of_availabilities = calculate_availability(production_data)
    dict_of_performances = calculate_performance(production_data)
    dict_of_oees = {}
    for machine_name in production_data.keys():
        quality = dict_of_qualities.get(machine_name)
        availability = dict_of_availabilities.get(machine_name)
        performance = dict_of_performances.get(machine_name)
        dict_of_oees[machine_name] = round(quality * availability * performance / 10000, 1)
    return dict_of_oees


def write_results_to_file(production_data: dict, filename: str):
    """
    Write the calculation results to a CSV formatted file.

    :param filename: string file path for the CSV file to be written to
    :param production_data: dictionary with production data
    """
    full_dict = {}
    dict_of_qualities = calculate_quality(production_data)
    dict_of_availabilities = calculate_availability(production_data)
    dict_of_performances = calculate_performance(production_data)
    dict_of_oees = calculate_oee(production_data)
    for machine_name in production_data.keys():
        quality = dict_of_qualities.get(machine_name)
        availability = dict_of_availabilities.get(machine_name)
        performance = dict_of_performances.get(machine_name)
        oee = dict_of_oees.get(machine_name)
        full_dict[machine_name] = [availability, performance, quality, oee]

    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["Liin", "Saadavus", "Tootlus", "Kvaliteet", "OEE"])
        for keys, values in full_dict.items():
            writer.writerow([keys, *values])


if __name__ == '__main__':
    prod_data = read_production_data("reedene_vahetus.csv")
    print('\n- Production data -')
    print('[Run Time (minutes), Ideal Run Rate (pcs/min), Total Count (pcs), Good Count (pcs)]')
    for key, value in prod_data.items():
        print(f"{key}: {value}")

    # Sildistaja: [358, 57, 18602, 18388]
    # Hapukurgipurgitaja: [415, 12, 4800, 2013]
    # Autoklaav: [450, 10, 4500, 4500]
    # Supivillija: [402, 36, 14230, 14214]
    # Makaronikeetja: [410, 25, 10230, 10230]
    # Kartulikoorija: [420, 111, 46620, 44123]
    # Mahlapress: [0, 0, 0, 0]

    quality_dict = calculate_quality(prod_data)
    print('\n- Quality calculation results -')
    for key, value in quality_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 98.8
    # Hapukurgipurgitaja: 41.9
    # Autoklaav: 100.0
    # Supivillija: 99.9
    # Makaronikeetja: 100.0
    # Kartulikoorija: 94.6
    # Mahlapress: 0.0

    availability_dict = calculate_availability(prod_data)
    print('\n- Availability calculation results -')
    for key, value in availability_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 85.2
    # Hapukurgipurgitaja: 98.8
    # Autoklaav: 107.1
    # Supivillija: 95.7
    # Makaronikeetja: 97.6
    # Kartulikoorija: 100.0
    # Mahlapress: 0.0

    performance_dict = calculate_performance(prod_data)
    print('\n- Performance calculation results -')
    for key, value in performance_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 91.2
    # Hapukurgipurgitaja: 96.4
    # Autoklaav: 100.0
    # Supivillija: 98.3
    # Makaronikeetja: 99.8
    # Kartulikoorija: 100.0
    # Mahlapress: 0.0

    oee_dict = calculate_oee(prod_data)
    print('\n- Total OEE calculation results -')
    for key, value in oee_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 76.8
    # Hapukurgipurgitaja: 39.9
    # Autoklaav: 107.1
    # Supivillija: 94.0
    # Makaronikeetja: 97.4
    # Kartulikoorija: 94.6
    # Mahlapress: 0.0

    write_results_to_file(prod_data, 'reedene_oee.csv')

    # contents of 'reedene_oee.csv':
    # Liin, Saadavus, Tootlus, Kvaliteet, OEE
    # Sildistaja, 85.2, 91.2, 98.8, 76.8
    # Hapukurgipurgitaja, 98.8, 96.4, 41.9, 39.9
    # Autoklaav, 107.1, 100.0, 100.0, 107.1
    # Supivillija, 95.7, 98.3, 99.9, 94.0
    # Makaronikeetja, 97.6, 99.8, 100.0, 97.4
    # Kartulikoorija, 100.0, 100.0, 94.6, 94.6
    # Mahlapress, 0.0, 0.0, 0.0, 0.0
