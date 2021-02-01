"""Secret Garden."""
import base64


class Decoder:
    """Decoder class."""

    def __init__(self, file: str, key: str):
        """
        Decoder constructor.

        :param file: Input file
        :param key: Very secret key
        """
        self._file = file
        self._key = key

    def read_code_from_file(self) -> list:
        """
        Read file lines to a list.

        File comes from class constructor.

        :return: List of file lines
        """
        edited_list = []
        with open(self._file, encoding="utf-8") as file:
            newer_list = file.readlines()
        for values in newer_list:
            if "\n" in values:
                values = values[:-1]
            edited_list.append(values)
        return edited_list

    @staticmethod
    def decode_from_base64(data: str) -> str:
        """
        Decode base64 string to utf-8 string.

        :param data: Base64 format string
        :return: Utf-8 format string
        """
        # https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
        newer_string = data.encode("utf-8")
        sample = base64.b64decode(newer_string)
        sample_string = sample.decode("utf-8")
        return sample_string

    def calculate_cipher_step(self) -> int:
        """
        Calculate cipher step.

        Cipher key comes from constructor.
        Formula is sum of UNICODE value of each letter.
        Example: "Hi" -> 72 + 105 -> 177

        :return: Cipher step as integer
        """
        # https://thecodingbot.com/how-to-get-unicode-code-of-a-character-in-python/
        list_of_unicode_values = []
        newer_string = self._key
        for char in newer_string:
            list_of_unicode_values.append(ord(char))
        return sum(list_of_unicode_values)

    def decode(self) -> list:
        """
        Decode file with key.

        For correct answer you have to convert file lines from base64 to utf-8.

        To decode one line you have to take a UNICODE value of a letter, subtract cipher step and take mod of 255.
        After that you have to convert that number back to a character.
        Example: key = 'test', decoded_data = "+%'"
        '+' -> (43 - 448) % 255 -> 'i' -> ... -> 'ice'

        :return: List of decoded lines
        """
        newer_string = ""
        list_decoded_ones = []
        list_of_lines = self.read_code_from_file()
        for line in list_of_lines:
            if newer_string != "":
                list_decoded_ones.append(newer_string)
                newer_string = ""
            decoded_line = self.decode_from_base64(line)
            for char in decoded_line:
                newer_string += chr((ord(char) - self.calculate_cipher_step()) % 255)
        list_decoded_ones.append(newer_string)
        return list_decoded_ones


class SecretGarden:
    """SecretGarden class."""

    def __init__(self, file: str, key: str):
        """
        SecretGarden constructor.

        :param file: Input file
        :param key: Very secret key
        """
        self._file = file
        self._key = key

    def decode_messages(self) -> list:
        """
        Use Decoder class to decode messages.

        :return: List of decoded lines
        """
        decoder = Decoder(self._file, self._key)
        return decoder.decode()

    def find_secret_locations(self) -> list:
        """
        Find all secret locations.

        You have to use decoded messages here. These messages contain a starting coordinate on first line e.g. '1;4'.
        First number shows position on east-west scale and second number shows position on north-south scale.
        Second line is empty.
        Third line contains steps to reach to the secret location e.g. 'NEEWSS'.
        Possible steps are 'N' (north), 'E' (east), 'S' (south) and 'W' (west). Each step moves your position by 1.

        :return: List of tuples with secret location coordinates
        """
        final_list = []
        dictionary = {}
        list_of_magic = self.decode_messages()
        for values in list_of_magic:
            newer_list = values.split("\n")
            dictionary[newer_list[2]] = newer_list[0].split(";")
        for key, value in dictionary.items():
            coordinate1 = int(value[0])
            coordinate2 = int(value[1])
            for char in key:
                if char.lower() == "e":
                    coordinate1 += 1
                elif char.lower() == "w":
                    coordinate1 -= 1
                elif char.lower() == "n":
                    coordinate2 += 1
                elif char.lower() == "s":
                    coordinate2 -= 1
            final_list.append((coordinate1, coordinate2))
        return final_list


if __name__ == '__main__':
    d = Decoder('pr08_example_data.txt', 'Fat Chocobo')
    for x in d.read_code_from_file():
        print(d.decode_from_base64(x))
    print(d.read_code_from_file())  # ['KS0uNyktWGpYakFPTw==', ...]
    print(d.decode_from_base64('MDsyCgpOTlNXV0U='))  # 0;2\n\nNNSWWE
    print(d.calculate_cipher_step())  # 70 + 97 + 116 + 32 + ... -> 1016
    print(d.decode())  # ['-12;-1\n\nESS', ...]

    sg = SecretGarden('pr08_example_data.txt', 'Fat Chocobo')
    print(sg.decode_messages())  # ['-12;-1\n\nESS', ...]
    print(sg.find_secret_locations())  # [(-11, -3), (20, -13), (1, -3), (-2, -5), (10, 4), (6, -13), (2, -6)]
