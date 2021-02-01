"""Booksortation."""


def booksortation(books: list) -> dict:
    """
    Given a list of books (strings). Your task is to categorize and sort them.

    There are five books categories: spell books, history books, relics books, potion books and other books.

    If a book doesn't belong to any named categories, it goes to 'other books' category.

    However, if one book belongs to multiple categories, they should appear in only one
    (starting from up, whichever occurs first).

    :param books: given books as a list, list contains of strings
    :return: categorised and sorted books as a dict, where keys are categories and values are
    list of books that match this category. Lists should be sorted alphabetically.
    """
    dict_of_books = {}
    dict_to_store_details_about_every_book = {}
    categories = ["spell books", "history books", "relics books", "potion books", "other books"]
    books = sorted(books)
    n = 0
    for book in books:
        if is_other_book(book):
            add_book_to_category(book, categories[-1], dict_of_books)
            n += 1
        else:
            dict_to_store_details_about_every_book[n] = [is_spell_book(book), is_history_book(book),
                                                         is_relics_book(book), is_potion_book(book)]
            n += 1
    for key, value in dict_to_store_details_about_every_book.items():
        if categories[value.index(True)] in dict_of_books.keys():
            dict_of_books[categories[value.index(True)]] += [books[key]]
        else:
            dict_of_books[categories[value.index(True)]] = [books[key]]
    return dict_of_books


def add_book_to_category(book: str, category: str, categorised_books: dict) -> dict:
    """
    Adding books to a category.

    :param book:
    :param category:
    :param categorised_books:
    :return:
    """
    if category in categorised_books.keys():
        categorised_books[category] += [book]
    else:
        categorised_books[category] = [book]
    return categorised_books


def is_spell_book(book: str) -> bool:
    """
    Book is a spell book if its title starts with '*' (a star, without quotes) and ends with '*' (a star, no quotes).

    However, if the starting and ending star is the same star, it is not a spell book.

    For example: '*The Horrible Spells*' is a spell book.

    :param book: given book as a string
    :return: True if given book is a spell book, False otherwise
    """
    if len(book) >= 2:
        return True if book[0] == "*" and book[-1] == "*" else False
    return False


def is_other_book(book: str) -> bool:
    """
    Function to find whether the book is suitable for category other or not.

    :param book: String
    :return: return True if book is not suitable for main topics.
    """
    if not is_relics_book(book) and not is_potion_book(book) and not is_spell_book(book) and not is_history_book(book):
        return True
    return False


def is_history_book(book: str) -> bool:
    """
    Book is a history book if its title matches the pattern where each new word starts with a capital letter.

    Word is considered anything after a whitespace.

    For example: 'The Mighty King' and 'The Age Of The Wonderbolts' are both history books.
    Then again, 'the Ugly Duckling' isn't a history books because the word 'the' doesn't start with a capital letter.

    :param book: given book as a string
    :return: True if given book is a history book, False otherwise
    """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', 'ä', 'ü', 'õ', 'ö']
    new_list = []
    splitted_book = book.split()
    for i in splitted_book:
        if i[0].isupper() or i[0] not in alphabet:
            new_list.append(i)
    if len(new_list) == len(splitted_book):
        return True
    return False


def is_relics_book(book: str) -> bool:
    """
    Book is a relics book if its title matches the uppercase-lowercase-uppercase-lowercase... pattern.

    It can start from both upper- and lowercase letters.
    PS! Pay attention to whitespaces.

    For example: 'ThE StAfF' and 'rAiNiNg dUmPlInGs' are both relics books.
    However 'ThE sTaFf' and 'rAiNiNg DuMpLiNgS' are not relics books.

    :param book: given book as a string
    :return: True if given book is a relics book, False otherwise
    """
    new_string = ''
    for i, letter in enumerate(book):
        if not book[i].isalpha():
            new_string += book[i]
            continue
        if book[0].isupper():
            if i % 2 == 0:  # Kui sõna algus on SUUR täht, siis iga teine täht peale seda on SUUR.
                new_string += book[i].upper()
            else:
                new_string += book[i].lower()  # Ülejäänud teeme väikesteks.
        if book[0].islower():
            if i % 2 == 0:  # Kui sõna algus on VÄIKE täht, siis iga teine täht peale seda on VÄIKE
                new_string += book[i].lower()
            else:
                new_string += book[i].upper()  # Ülejäänud teeme suurteks.
    return True if book == new_string else False


def is_potion_book(book: str) -> bool:
    """
    Book is a potion book if its title contains the same amount of vowels and consonants or the amount differs by one.

    However, it may contain as many symbols as it likes.

    The vowels are a, e, i, o, u.
    The consonants are b, c, d, f, g, h, j, k, l, m, n, p, q, r, s, t, v, x, z, w, y.

    For example: 'The Banana Juice' is a potion book (7 vowels, 7 consonants)
    and so is 'The tomato potion' (7 vowels, 8 consonants -> differ by 1).
    However, 'The Green Liquid' isn't a potion book (6 vowels, 8 consonants -> differ by 2).

    :param book: given book as a string
    :return: True if given book is a potion book, False otherwise
    """
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y',
                  'z']
    vowels = ["a", "e", "i", "o", "u"]
    count_vowels, count_consonants = 0, 0
    for i in book:
        if i.lower() in consonants:
            count_consonants += 1
        elif i.lower() in vowels:
            count_vowels += 1
    if count_consonants == count_vowels or count_consonants - count_vowels == 1 or count_vowels - count_consonants == 1:
        return True
    return False


if __name__ == '__main__':
    # All True.
    print(booksortation(['*kana*', 'This Is A History Book', 'ThE StAfF', 'The Banana Juice']))
