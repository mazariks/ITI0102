"""Tests for Santa's workshop."""
import pytest
import santas_workshop
import os.path

santa_workshop_correct_example = santas_workshop.Data("ex15_nice_list.csv", "ex15_naughty_list.csv",
                                                      "ex15_wish_list.csv")


def test_files_not_found():
    """."""
    with pytest.raises(FileNotFoundError):
        santas_workshop.Data("ex16.csv", "x.csv", "sd.csv")


def test_get_data_of_gift_from_url():
    """."""
    dict_of_data = santas_workshop.get_data_of_gift_from_url("Toy truck")
    assert type(dict_of_data) == dict
    assert "gift" in dict_of_data.keys() and "material_cost" in dict_of_data.keys() \
           and "production_time" in dict_of_data.keys() and "weight_in_grams" in dict_of_data.keys()
    assert type(dict_of_data["gift"]) == str
    assert type(dict_of_data["production_time"]) == int


def test_read_nice_data_from_file():
    """."""
    list_of_data = santas_workshop.read_data_from_file("ex15_nice_list.csv")
    assert len(list_of_data) == 291
    assert len(list_of_data[0]) == 2


def test_get_data_of_letter_from_url():
    """."""
    letter_text = santas_workshop.get_data_of_letter_from_url()
    assert type(letter_text) == str
    assert len(letter_text) > 0
    assert "\n" not in letter_text


def test_read_wishes_from_file():
    """."""
    with pytest.raises(FileNotFoundError):
        santas_workshop.read_wishes_from_file("xyz.csv")
    dict_of_wishes = santas_workshop.read_wishes_from_file("ex15_wish_list.csv")
    assert type(dict_of_wishes) == dict
    assert len(dict_of_wishes.keys()) == 399


def test_prepare_string_for_operations():
    """."""
    test_string1 = "lm, werxe!\n\nm eq zivc xlerojyp jsv xli rmgi tviwirxw csy fvsyklx qi pewx ciev, m wxmpp tpec " \
                   "amxl xliq izivc hec!\n\nger'x aemx xs wii csy,\nipwmi, gerehe"

    test_string2 = "Greetings to the North Pole!\n\nI saw an elf the other day, he was just making it out through " \
                   "the window when I spotted him\n\nCan't wait to see you,\nDaniel, Puerto Rico"

    test_string3 = "Hi Santa and Elves!\n\nI would really love to get some nice presents this year, but I would love " \
                   "most if my little sisters got their dream gifts!\n\nThis year I wish for Princess dress, " \
                   "Polyhedral dice set, Fortnite t-shirt.\n\nCan't wait to see you,\nLaurence, Sweden"

    test_string4 = "SGkgU2FudGEgYW5kIEVsdmVzIQoKSSBoYXZlIGJlZW4gdmVyeSBuaWNlIHRvIG15IGZhbWlseSBhbmQgZnJpZW5kc" \
                   "ywgYW5kIGV2ZW4gc29tZSBwZW9wbGUgd2hvIGhhdmUgbm90IGJlZW4gdmVyeSBuaWNlIHRvIG1lLCBsaWtlIG9" \
                   "1ciBuZWlnaGJvciB3aG8geWVsbHMgYXQgbWUgd2hlbiBJIHBsYXkgd2l0aCB0aGUgd2F0ZXJob3NlLgoKU2luY2VyZW" \
                   "x5IHlvdXJzLApHZW5lLCBBdXN0cmFsaWE="

    test_string5 = "Dear Santa!\n\nI have been very nice to my family and friends, " \
                   "and even some people who have not been very nice to me, like our neighbor who yells at " \
                   "me when I play with the waterhose.\n\nThis year, I want Basketball, New phone.\n\nCan't wait " \
                   "to see you,\nCallum, Peru"

    operate1 = santas_workshop.prepare_string_for_operations(test_string1)
    assert not operate1

    operate2 = santas_workshop.prepare_string_for_operations(test_string2)
    assert not operate2

    operate3 = santas_workshop.prepare_string_for_operations(test_string3)
    assert operate3 and "Laurence" in operate3 and "Sweden" in operate3
    assert "Princess dress" in operate3[0]

    operate4 = santas_workshop.prepare_string_for_operations(test_string4)
    assert not operate4

    operate5 = santas_workshop.prepare_string_for_operations(test_string5)
    assert operate5


def test_is_base64_encoded():
    """."""
    empty_text = ""
    one_char_text = "A"
    assert not santas_workshop.is_base64_encoded(empty_text)
    assert not santas_workshop.is_base64_encoded(one_char_text)
    full_text1 = "SGkgU2FudGEgYW5kIEVsdmVzIQoKSSBoYXZlIGJlZW4gdmVyeSBuaWNlIHRvIG15IGZhbWlseSBhbmQgZnJpZW5kcywgYW5kIG" \
                 "V2ZW4gc29tZSBwZW9wbGUgd2hvIGhhdmUgbm90IGJlZW4gdmVyeSBuaWNlIHRvIG1lLCBsaWtlIG91ciBuZWlnaGJvciB3aG8" \
                 "geWVsbHMgYXQgbWUgd2hlbiBJIHBsYXkgd2l0aCB0aGUgd2F0ZXJob3NlLgoKU2luY2VyZWx5IHlvdXJzLApHZW5lLCBBdXN" \
                 "0cmFsaWE="
    assert santas_workshop.is_base64_encoded(full_text1)

    full_text2 = "Dear Santa!\n\nI would really love to get some nice presents this year, but I would love most if " \
                 "my little sisters got their dream gifts!\n\nThe following is my wishlist: Pink fluffy pen, Book " \
                 "about dinosaurs.\n\nThank you,\nDanielle, South Africa"
    assert not santas_workshop.is_base64_encoded(full_text2)


def test_decode_from_base64():
    """."""
    test_text1 = "SGkgU2FudGEgYW5kIEVsdmVzIQoKSSBoYXZlIGJlZW4gdmVyeSBuaWNlIHRvIG15IGZhbWlseSBhbmQgZnJpZW5kcywgYW5" \
                 "kIGV2ZW4gc29tZSBwZW9wbGUgd2hvIGhhdmUgbm90IGJlZW4gdmVyeSBuaWNlIHRvIG1lLCBsaWtlIG91ciBuZWlnaGJvciB3a" \
                 "G8geWVsbHMgYXQgbWUgd2hlbiBJIHBsYXkgd2l0aCB0aGUgd2F0ZXJob3NlLgoKVGhlIGZvbGxvd2luZyBpcyBteSB3aXNob" \
                 "GlzdDogSG9yc2UgcmlkaW5nIGhlbG1ldCwgUmVtb3RlIGNvbnRyb2xsZWQgY2FyLgoKVGhhbmtzLCBTYW50YSwKS2VsbHksI" \
                 "FB1ZXJ0byBSaWNv"

    assert santas_workshop.decode_from_base64(test_text1).replace("\n", "") == "Hi Santa and Elves!I have been very " \
                                                                               "nice to my family and friends, and " \
                                                                               "even some people who have not " \
                                                                               "been very nice to me, like our " \
                                                                               "neighbor who yells at me when I " \
                                                                               "play with the waterhose.The following" \
                                                                               " is my wishlist: Horse riding helmet," \
                                                                               " Remote controlled car.Thanks, " \
                                                                               "Santa,Kelly, Puerto Rico"


def test_caesar_decoder():
    """."""
    innormal_text = "lipps, werxe!\n\nepxlsykl m lezi leh wsqi wpmt-ytw, m fipmizi m lezi fiir kssh irsykl " \
                    "xlmw ciev xs hiwivzi wsqi tviwirxw.\n\nxlmw ciev m amwl jsv xefpix gsqtyxiv, fvyrixxi fevfmi " \
                    "hspp, xsc hmrsweyv tpec wix.\n\nger'x aemx xs wii csy,\nkisvkme, kivqerc"

    assert santas_workshop.caesar_decoder(innormal_text) == "hello, santa!\n\nalthough i have had some slip-ups, " \
                                                            "i believe i have been good enough this year to deserve " \
                                                            "some presents.\n\nthis year i wish for tablet " \
                                                            "computer, brunette barbie doll, toy dinosaur play " \
                                                            "set.\n\ncan't wait to see you,\ngeorgia, germany"

    normal_text = "hello, world!"
    assert santas_workshop.caesar_decoder(normal_text) == "dahhk, sknhz!"


def test_create_person():
    """."""
    person1 = santas_workshop.Person("Ago", "Estonia")
    assert isinstance(person1, santas_workshop.Person)
    assert person1.citizenship == "Estonia"
    assert person1.__repr__() == "Ago"
    assert person1.is_naughty is None


def test_create_gift():
    """."""
    gift1 = santas_workshop.Gift("Pyytoni 6pik", 25, 3, 1332)
    assert isinstance(gift1, santas_workshop.Gift)
    assert gift1.__repr__() == "Pyytoni 6pik"
    assert gift1.weight == 1332


def test_add_wish_to_person():
    """."""
    gift1 = santas_workshop.Gift("Pyytoni 6pik", 25, 3, 1332)
    person1 = santas_workshop.Person("Ago", "Estonia")
    operation1 = gift1.add_wish_to_person(person1)
    assert operation1
    assert person1.wishes


def test_check_if_files_exist():
    """."""
    for x in ["Australia", "Canada", "Estonia", "Germany", "Peru", "Puerto Rico", "South Africa", "Sweden",
              "United Kingdom", "United States of America"]:
        assert os.path.exists(f"ticket_of_{x}.txt")
