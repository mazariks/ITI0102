"""EX15. Santa's Workshop."""
import base64
import csv
from urllib import parse, request
import re
import os.path

# Some static methods to operate at data.


def get_data_of_gift_from_url(gift: str) -> dict:
    """Get data of gift from url."""
    url_begin = "http://api.game-scheduler.com:8089/gift?name="
    full_url = url_begin + parse.quote(gift.strip())  # kodeerib sone.
    response = request.urlopen(full_url)
    return eval(response.read())  # eval - makes a dict out of string


def read_data_from_file(file_name: str) -> list:
    """Read file data into list."""
    list_of_data = []
    current_line = []
    if not os.path.exists(file_name):
        raise FileNotFoundError()
    with open(file_name, 'r+') as file:
        for line in csv.reader(file):
            for sub_line in line:
                sub_line = sub_line.strip()
                current_line.append(sub_line)
            list_of_data.append(current_line)
            current_line = []
    return list_of_data


def get_data_of_letter_from_url() -> str:
    """Get data of letter from url."""
    response = request.urlopen("http://api.game-scheduler.com:8089/letter")
    probable_wish = list(eval(response.read()).values())[0]  # details of the letter.
    probable_wish = probable_wish.replace("\n", " ")  # replacing \n with whitespace.
    return probable_wish


def read_wishes_from_file(file_name: str) -> dict:
    """Create dictionary of wishes."""
    final_dict = {}
    if not os.path.exists(file_name):
        raise FileNotFoundError()
    with open(file_name, 'r+') as file:
        for lines in csv.reader(file):
            for index, line in enumerate(lines):
                if index > 0:
                    new_line = line.strip()
                    if lines[0] not in final_dict.keys():
                        final_dict[lines[0]] = [new_line]
                    else:
                        final_dict[lines[0]] += [new_line]
    return final_dict


def prepare_string_for_operations(probable_wish: str) -> list:
    """Operate at letter in order to get particular data (wishes, wisher)."""
    if is_base64_encoded(probable_wish):
        probable_wish = decode_from_base64(probable_wish)  # Decoding from base64 if it is needed.
    elif 'Santa' not in probable_wish and 'Claus!' not in probable_wish and 'North Pole' not in probable_wish:
        probable_wish = caesar_decoder(probable_wish)  # If there are not clean words, decode from Caesar cipher
    if "I want" in probable_wish or "I wish for" in probable_wish or "wishlist:" in probable_wish:
        # Split according to the words inside string.
        if "wishlist:" in probable_wish:
            probable_wish = probable_wish.split("wishlist: ")
        elif "I want" in probable_wish:
            probable_wish = probable_wish.split("I want ")
        elif "I wish for" in probable_wish:
            probable_wish = probable_wish.split("I wish for ")
        new_state = [prob.split(".") for prob in probable_wish][1]  # Get list with Wishes and Wisher
        probable_wish = new_state[0].split(",")  # Get the list of wishes.
        probable_wisher_name = new_state[1].split(",")[-2].strip()  # get the string of Wisher's name
        probable_wisher_citizenship = new_state[1].split(",")[-1].strip()  # get the string of wisher's country
        return [probable_wish, probable_wisher_name, probable_wisher_citizenship]
    return []


def is_base64_encoded(string: str) -> bool:
    """Check if string is encoded with base64."""
    if not string or len(string) < 1:
        return False
    pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
    if pattern.match(string):
        return True
    else:
        return False


def decode_from_base64(string: str) -> str:
    """Decode from base64."""
    base64_bytes = string.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')


def caesar_decoder(encoded_string: str, shift=4) -> str:
    """Decode from Caesar encoding."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    decoded_string = ''
    for char in encoded_string:
        if char in [' ', '!', '?', '\n', '.', ',', '-', '_', '\t', ':', "'", ';'] or char in numbers:
            decoded_string += char
        else:
            index = alphabet.index(char) - shift
            while index < 0:
                index += len(alphabet)
            decoded_string += alphabet[index]
    return decoded_string


class Person:
    """Class of the person."""

    def __init__(self, name: str, citizenship: str):
        """Constructor of the class person."""
        self.name = name
        self.citizenship = citizenship
        self.is_naughty = None
        self.wishes = []

    def __repr__(self):
        """String representation of class person."""
        return self.name


class Gift:
    """Class of the gift."""

    def __init__(self, name: str, material_cost: int, production_time: int, weight: int):
        """Constructor of the gift class."""
        self.name = name
        self.costs = material_cost
        self.production_time = production_time
        self.weight = weight

    def __repr__(self):
        """Representation of class gift."""
        return self.name

    def add_wish_to_person(self, person: Person) -> bool:
        """Add this gift to the person's wishes."""
        for gift in person.wishes:
            if gift.name == self.name:
                return False
        person.wishes.append(self)
        return True


class Data:
    """Class of getting data from csv files."""

    def __init__(self, nice_file: str, naughty_file: str, wishes_file: str):
        """Constructor of csv files."""
        # load data from files.
        self.nice_data = read_data_from_file(nice_file)
        self.naughty_data = read_data_from_file(naughty_file)
        self.wishes_data = read_wishes_from_file(wishes_file)

        # create people.
        self.naughty_people = self.arrange_naughty_people()
        self.nice_people = self.arrange_nice_people()
        self.total_people = self.nice_people + self.naughty_people

        # create gifts and warehouse of gifts (gifts are waiting for departure).
        self.gifts = self.arrange_gifts()
        self.warehouse = self.create_warehouse_arrange_wishes()
        self.get_wishes_from_post()
        self.logistics()

    def create_warehouse_arrange_wishes(self) -> dict:
        """Create warehouse of gifts and people."""
        final_dict = {x: [] for x in self.total_people}
        for key, value in self.wishes_data.items():  # {name: [gifts]}
            for person in self.total_people:  # [person1, person2, etc.]
                if person.name == key:
                    for person_wish in value:  # gift1, gift2, gift3, ...
                        for gift in self.gifts:  # [{name}]
                            if person_wish == gift.name:
                                final_dict[person] += [gift]
                                gift.add_wish_to_person(person)
        return final_dict

    def arrange_gifts(self):
        """Create gifts' objects."""
        gifts_names = []
        list_to_return = []
        for list_value in self.wishes_data.values():
            for value in list_value:
                gifts_names.append(value)
        gifts_names = list(set(gifts_names))

        for name in gifts_names:
            info_about_gift = list(get_data_of_gift_from_url(name).values())
            # 0 - name; 1 - costs; 2 - time; 3 - weight.
            gift = Gift(info_about_gift[0], info_about_gift[1], info_about_gift[2], info_about_gift[3])
            list_to_return.append(gift)
        return list_to_return

    def arrange_naughty_people(self):
        """Create people from naughty list."""
        list_of_naughty_people = []
        list_of_seen_names = []
        for line in self.naughty_data:
            name = line[0]
            country = line[1]
            if name not in list_of_seen_names:
                naughty_person = Person(name, country)
                naughty_person.is_naughty = True
                list_of_naughty_people.append(naughty_person)
                list_of_seen_names.append(name)
        return list_of_naughty_people

    def arrange_nice_people(self):
        """Create people from nice list."""
        list_of_nice_people = []
        list_of_seen_names = []
        for line in self.nice_data:
            name = line[0]
            country = line[1]
            if name not in list_of_seen_names:
                nice_person = Person(name, country)
                nice_person.is_naughty = False
                list_of_nice_people.append(nice_person)
                list_of_seen_names.append(name)
        return list_of_nice_people

    def get_wishes_from_post(self):
        """Get some wishes from post."""
        for _ in range(151):  # We will be receiving 150 letters from children.
            letter_text = get_data_of_letter_from_url()
            if prepare_string_for_operations(letter_text):
                probable_wisher_name = prepare_string_for_operations(letter_text)[1]
                probable_wisher_citizenship = prepare_string_for_operations(letter_text)[2]
                probable_wish = prepare_string_for_operations(letter_text)[0]
                for person, gifts in self.warehouse.items():  # iterate through warehouse {person1: [gifts1], ...}
                    person_name = person.name.lower()
                    wisher_name = probable_wisher_name.lower()
                    person_citizenship = person.citizenship.lower()
                    wisher_citizenship = probable_wisher_citizenship.lower()
                    if person_name == wisher_name and person_citizenship == wisher_citizenship:
                        list_of_presents_to_add = []  # additional presents (objects) to be added if needed.
                        for prob_wish in probable_wish:  # iterate through every additional gift.name
                            prob_wish = prob_wish.strip()  # remove whitespace (HATE THEM ALREADY)
                            for gift in self.gifts:  # iterate through every gift (object) in db
                                if gift.name.lower() == prob_wish.lower():  # if they equal, then append to add. list.
                                    list_of_presents_to_add.append(gift)
                        for gift_i in list_of_presents_to_add:
                            # if this person has some gifts that are not still added, then add this gift there.
                            if gift_i not in gifts:
                                self.warehouse[person] += gift_i
        return ""

    def logistics(self):
        """Send gifts to children."""
        # filter children (keep only those who deserves a present).
        # https://thispointer.com/python-filter-a-dictionary-by-conditions-on-keys-or-values/
        filtered_dict = dict(filter(lambda x: not x[0].is_naughty, self.warehouse.items()))

        # sort them by their citizenship.
        sorted_filtered_dict = dict(sorted(filtered_dict.items(), key=lambda x: x[0].citizenship))

        # Now we group people by their citizenship (gifts objects are remained in the people 'wishes'.
        grouped_dictionary = {}
        for key in sorted_filtered_dict.keys():
            if key.citizenship not in grouped_dictionary.keys():
                grouped_dictionary[key.citizenship] = [key]
            else:
                grouped_dictionary[key.citizenship] += [key]

        # find width of column (gifts).
        dictionary_of_width = {country: 0 for country in grouped_dictionary.keys()}
        for key_x, value_x in grouped_dictionary.items():
            for person_x in value_x:
                max_of_values_x = sum([len(x.name) for x in person_x.wishes])
                if max_of_values_x > dictionary_of_width[key_x]:
                    # if we add comas and whitespaces, then should be +5
                    dictionary_of_width[key_x] = max_of_values_x + 5

        for key, value in grouped_dictionary.items():  # key: country, value: [name1, name2, name3]
            country = key
            writings_country = "\n" + f"TO: {country}" + "\n"
            writings_top_border = "//" + "=" * 11 + "[]" + "=" * (dictionary_of_width[country] + 2)
            writings_top_border += "[]" + '=' * 19 + r"\\" + "\n"
            centralize_picture = len(writings_top_border) // 2
            delivery_order_string = " " * centralize_picture + "DELIVERY ORDER" + "\n"

            santa_image_string = " " * 58 + "_v" + "\n" + " " * 53 + "__* (__)" + "\n" + " " * 13 + "ff" + " " * 5 \
                                 + "ff" + " " * 5 + "ff" + " " * 5 + "ff" + " " * 16 + r"{\/ (_(__).-." + "\n" + " " \
                                 * 6 + "ff" + " " * 4 + r"<_\__," + " " * 1 + r"<_\__," + " " * 1 + r"<_\__," + " " \
                                 * 1 \
                                 + r"<_\__," + " " * 6 + r"__,~~.(`>|-(___)/ ,_)" + "\n" + " " * 4 + r"o<_\__," + " " \
                                 * 2 + r'(_ ff ~(_ ff ~(_ ff ~(_ ff~~~~~@ )\/_;-"``     |     HAPPY NEW YEAR! ' \
                                       'HO-HO-HO!' + "\n" + " " * 6 + r'(___)~~//<_\__, <_\__, <_\__, <_\__,    | ' \
                                                                      r'\__________/|     ' \
                                                    'GIFTS FOR (ALMOST) EVERYONE!' + "\n" + " " * 6 + r"// >>" + " " \
                                 * 5 + r"(___)~~(___)~~(___)~~(___)~~~~\.\_/_______\_//" + "\n" + " " \
                                 * 16 + r"// >>  // >>  // >>  // >>" + " " * 5 + r"`'---------'`" + "\n"

            file_of_country = open(f"ticket_of_{country}.txt", "w+")

            writings1 = "FROM: NORTH POLE CHRISTMAS CHEER INCORPORATED"

            left_align = (dictionary_of_width[country] - 3) // 2
            right_align = (dictionary_of_width[country] - 3) // 2
            if left_align + right_align < dictionary_of_width[country] - 3:
                right_align = left_align + 1

            writings_namings = "||" + " " * 3 + "Name" + " " * 4 + "||"
            writings_namings += " " * left_align + "Gifts" + " " * right_align + "||"
            writings_namings += " " + "Total Weight (KG)" + " " + "||\n"
            writings_section = "|]===========[]" + "=" * (dictionary_of_width[country] + 2) + "[]" + '=' * 19 + "[|\n"
            list_to_append = [delivery_order_string, santa_image_string, writings1, writings_country,
                              writings_top_border, writings_namings, writings_section]
            file_of_country.writelines(list_to_append)
            for person in value:
                name = person.name
                gifts_weights = sum([y.weight for y in person.wishes]) / 1000
                gifts_namings = [x.name for x in person.wishes]
                gifts = ", ".join(gifts_namings)
                writings_data = "||" + " " + name + " " * (10 - len(name)) + "||"
                writings_data += " " + gifts + " " * (dictionary_of_width[country] - len(gifts)) + " " + "||"
                writings_data += " " * (16 - len(str(gifts_weights))) + str(gifts_weights) + " " * 3 + "||\n"
                file_of_country.write(writings_data)

            writings_bottom_border = r"\\===========[]" + "=" * (dictionary_of_width[country] + 2)
            writings_bottom_border += "[]===================//"
            file_of_country.write(writings_bottom_border)
            file_of_country.close()


if __name__ == '__main__':
    data = Data("ex15_nice_list.csv", "ex15_naughty_list.csv", "ex15_wish_list.csv")
