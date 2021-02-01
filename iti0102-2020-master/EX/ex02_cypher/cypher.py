"""Shifting letters."""


def encode(message: str, key: int) -> str:
    """
    Encode a message using a Caesar cipher.

    Presume the message is already lowercase.
    For each letter of the message, shift it forward in the alphabet by key amount.
    If the character isn't a letter, keep it the same.

    E.g. key = 3 a->d, b->e
    encode('i like turtles', 6) -> 'o roqk zaxzrky'
    encode('example', 1) -> 'fybnqmf'
    encode('the quick brown fox jumps over the lazy dog.', 7) -> 'aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.'

    :param message: message to be encoded
    :param key: key for encoding
    :return: encoded message
    """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    new_string = ''
    for i in message:
        if i not in alphabet:
            new_string += i
        elif key > 35:
            amount_of_needed_alphabets = key // (len(alphabet) - 1)
            new_string += alphabet[alphabet.index(i) + key - len(alphabet) * amount_of_needed_alphabets]
        elif alphabet.index(i) + key > len(alphabet) - 1:
            new_string += alphabet[alphabet.index(i) + key - len(alphabet)]
        else:
            new_string += alphabet[alphabet.index(i) + key]
    return new_string


if __name__ == '__main__':
    print(encode('hello', 100))
    print(encode('hello', 36))
    print(encode("i like turtles", 6))  # -> o roqk zaxzrky
    print(encode("o roqk zaxzrky", 20))  # -> i like turtles
    print(encode("example", 1))  # -> fybnqmf
    print(encode("don't change", 0))  # -> don't change
    print(encode('the quick brown fox jumps over the lazy dog.', 7))  # -> aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.
