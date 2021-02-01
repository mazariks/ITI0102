"""Secret Garden tests."""
from secret_garden import Decoder, SecretGarden
import random

filename = "pr08_example_data.txt"
key = "Fat Chocobo"
d = Decoder(filename, key)
s = SecretGarden(filename, key)


def test_read_from_file():
    """
    Test of function of reading data from file.

    :return:
    """
    reading_file = d.read_code_from_file()
    assert type(reading_file) == list
    assert len(reading_file) == 7
    assert "\n" not in d.read_code_from_file()


def test_decode_from_base64():
    """
    Test of function of decoding messages from base64 to utf-8.

    :return:
    """
    list_to_be_checked = []
    list_of_truth = [")-.7)-AOO", "-57)-0JASJAOOASJ", ")07)2AJSAJAJOAJJAAO", ".7)/AJSSAJSJOOSSOOOS",
                     "-,70", ",7)-,OAASSOSOAAASAAAAA", ".7).SOSAOJAOOO"]
    for x in d.read_code_from_file():
        list_to_be_checked.append(d.decode_from_base64(x))
    assert list_to_be_checked == list_of_truth


def test_calculate_cipher_step():
    """
    Test of function of calculating the cipher step.

    :return:
    """
    given_value = d.calculate_cipher_step()
    assert type(given_value) == int
    assert given_value == 1016
    new_decoder = Decoder(filename, "HELLO THERE!")
    new_value = new_decoder.calculate_cipher_step()
    assert new_value != given_value
    random_number = random.Random()
    assert given_value != random_number


def test_decode():
    """
    Test of function of decoding.

    :return:
    """
    decoding = d.decode()
    assert type(decoding) == list
    assert len(decoding) == 7
    assert decoding[0] == '-12;-1\n\nESS'
    assert decoding[-1] == '2;-2\n\nWSWESNESSS'
    for x in decoding:
        assert "\n" in x


def test_decode_messages():
    """
    Test of function of decoding messages in SecretGarden class.

    :return:
    """
    decoding1 = d.decode()
    decoding2 = s.decode_messages()
    assert decoding1 == decoding2
    decoding3 = SecretGarden(filename, "HELLO, STUDENTS.").decode_messages()
    assert decoding1 != decoding3


def test_find_secret_locations():
    """
    Test of function of finding secret locations in SecretGarden class.

    :return:
    """
    list_of_random = [(random.Random(), random.Random()), (random.Random(), random.Random()), (random.Random(),
                                                                                               random.Random()),
                      (random.Random(), random.Random()), (random.Random(), random.Random()),
                      (random.Random(), random.Random()), (random.Random(), random.Random())]
    list_of_truth = [(-11, -3), (20, -13), (1, -3), (-2, -5), (10, 4), (6, -13), (2, -6)]
    secrets = s.find_secret_locations()
    assert type(secrets) == list
    for x in secrets:
        assert type(x) == tuple
    assert secrets == list_of_truth
    assert list_of_random != secrets
    assert len(list_of_random) == len(secrets)
