"""KT1."""


def positive_or_not(nums: list, pos: bool) -> list:
    """
    Given a list of integers and a boolean pos.

    If pos is True, return a new list containing only positive numbers of the first list.
    Otherwise return a new list containing all the other numbers but positive of the given list.

    print(positive_or_not([9, 5, 0, 6, -5, -1], True))  => [9, 5, 6]
    print(positive_or_not([3, 4, -2, 1, -78, 0], False))  => [-2, -78, 0]

    :param pos:
    :param nums:
    :return:
    """
    list_to_return = []
    if pos:
        for x in nums:
            if x > 0:
                list_to_return.append(x)
    if not pos:
        for x in nums:
            if x <= 0:
                list_to_return.append(x)
    return list_to_return


def sum_half_evens(nums: list) -> int:
    """
    Return the sum of first half of even ints in the given array.

    If there are odd number of even numbers, then include the middle number.

    sum_half_evens([2, 1, 2, 3, 4]) => 4
    sum_half_evens([2, 2, 0, 4]) => 4
    sum_half_evens([1, 3, 5, 8]) => 8
    sum_half_evens([2, 3, 5, 7, 8, 9, 10, 11]) => 10
    """
    even_list = []
    for value in nums:
        if value % 2 == 0:
            even_list.append(value)
    middle_index = len(even_list) // 2
    correct_list = even_list[:middle_index + 1]
    return sum(correct_list)


def max_block(s: str) -> int:
    """
    Given a string, return the length of the largest "block" in the string.

    A block is a run of adjacent chars that are the same.

    max_block("hoopla") => 2
    max_block("abbCCCddBBBxx") => 3
    max_block("") => 0
    """
    summary = 0
    for i in range(len(s)):
        current_count = 1
        for j in range(i + 1, len(s)):
            if s[i] == s[j]:
                current_count += 1
        if current_count > summary:
            summary = current_count
    return summary


class Person:
    """Person class."""

    def __init__(self, firstname: str, lastname: str, phone_number: str):
        """Constructor."""
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number

    def get_full_name(self) -> str:
        """
        Get full name of the person.

        Return firstname and lastname separated by space.
        If the lastname is empty, then return only the firstname.
        """
        if self.lastname == "":
            return self.firstname
        return self.firstname + " " + self.lastname


class ContactBook:
    """Contacat book class."""

    def __init__(self):
        """Constructor."""
        self.contacts = []

    def add_person_to_contacts(self, person: Person) -> None:
        """Add person to contact book if phone number and firstname are not empty strings."""
        if person.firstname != "" and person.phone_number != "":
            self.contacts.append(person)
            return None

    def find_contact_by_number(self, number) -> Person:
        """
        Return person who has the given number.

        If there are several people with the given number, return the first.
        If there is no person with the given number, return None.
        """
        for people in self.contacts:
            if number == people.phone_number:
                return people
        return None

    def get_sorted_contacts(self) -> list:
        """Sort contacts alphabetically by full name."""
        updated_list = sorted(self.contacts, key=lambda x: (x.firstname, x.lastname))
        return updated_list


class FridgeItem:
    """Fridge item class."""

    def __init__(self, name: str, type: str, days_till_expiration: int):
        """Constructor."""
        self.name = name
        self.type = type
        self.days_till_expiration = days_till_expiration

    def __repr__(self):
        """
        Return FridgeItem in nice string form.

        For example:
        name = "apple", type = "fruit", days_till_expiration = 4
        "Name: apple, type: fruit, expires in 4 days."

        If the item expires today (expires in 0 days):
        name = "apple", type = "fruit", days_till_expiration = 0
        "Name: apple, type: fruit, expires today."

        If the item has already expired:
        name = "apple", type = "fruit", days_till_expiration = -2
        "Name: apple, type: fruit, expired 2 days ago."

        If the item expired yesterday (one day ago):
        name = "apple", type = "fruit", days_till_expiration = -1
        "Name: apple, type: fruit, expired 1 day ago."

        If the item expires tomorrow (in one day):
        name = "apple", type = "fruit", days_till_expiration = 1
        "Name: apple, type: fruit, expires in 1 day."

        :return:
        """
        if self.days_till_expiration == 0:
            return f"name = {self.name}, type = {self.type}, expires today."
        elif self.days_till_expiration < -1:
            return f"name = {self.name}, type = {self.type}, expired {self.days_till_expiration} days ago."
        elif self.days_till_expiration == -1:
            return f"name = {self.name}, type = {self.type}, expired 1 day ago."
        elif self.days_till_expiration == 1:
            return f"name = {self.name}, type = {self.type}, expires in 1 day."
        else:
            return f"name = {self.name}, type = {self.type}, expires in {self.days_till_expiration} days."


class Fridge:
    """Fridge class."""

    def __init__(self):
        """Constructor."""
        self.items = []

    def add_items(self, items: list):
        """
        Add given items to items list.

        If an item is in the list already, don't add it.
        """
        for item in items:
            if item not in self.items:
                self.items.append(item)

    def get_items(self) -> list:
        """Return items in the fridge."""
        return self.items

    def remove_item(self, item: FridgeItem) -> None:
        """Remove FridgeItem from items list if it's there."""
        newer_list = []
        if item in self.items:
            for values in self.items:
                if values != item:
                    newer_list.append(values)
        self.items = newer_list
        return None

    def clean_the_fridge(self) -> None:
        """Remove all the items from the fridge that have expired."""
        newer_list = []
        for values in self.items:
            if values.days_till_expiration >= 0:
                newer_list.append(values)
        self.items = newer_list
        return None

    def get_items_that_wont_have_expired_in_n_days(self, n: int) -> list:
        """
        Return list of items that won't have expired in given n days.

        An item hasn't expired on its 0. day till expiration.

        Example:
        item 1 expires in 3 days
        item 2 expires in 4 days
        item 3 expires in 5 days
        calling this method with n = 4 returns items 2 and 3.
        """
        updated_list = []
        self.clean_the_fridge()
        for x in self.items:
            if x.days_till_expiration - n >= 0:
                updated_list.append(x)
        return updated_list

    def get_sorted_items(self) -> list:
        """
        Sort FridgeItems by days till expiration (first should be expired items, then first expiring).

        If they have the same amount of days till expiration, sort them by name (descending).
        :return: sorted list of FridgeItems
        """
        return sorted(self.items, key=lambda x: (x.days_till_expiration, x.name))

    def get_items_of_type(self, type: str) -> list:
        """Return list of items that are the given type (case-sensitive)."""
        updated_list = []
        for item in self.items:
            if item.type == type:
                updated_list.append(item)
        return updated_list

    def get_items_with_name(self, name: str):
        """
        Return list of items with which name you can form the required name by re-arranging letters in the name.

        Capital and non-capital letters are equal here (case-insensitive).
        Example:
        if the parameter name = "milk" then items with names "Milk" and "LIMK" will be returned.
        """
        updated_list = []
        for item in self.items:
            if item.name.upper() == name.upper():
                updated_list.append(item)
        return updated_list


if __name__ == '__main__':
    print(max_block("hoopla"))
    print(max_block("abbCCCddBBBxx"))
    p1 = Person("Peeter", "Mets", "12345678")
    print(p1.get_full_name())  # Peeter Mets

    p2 = Person("Kaarel", "", "54323456")
    print(p2.get_full_name())  # Kaarel

    contact_book = ContactBook()
    contact_book.add_person_to_contacts(p1)
    contact_book.add_person_to_contacts(p2)
    print(len(contact_book.contacts))  # 2

    for contact in contact_book.get_sorted_contacts():
        print(contact.get_full_name())
    """Kaarel
       Peeter Mets"""

    print(contact_book.find_contact_by_number("12345678").get_full_name())  # Peeter Mets
