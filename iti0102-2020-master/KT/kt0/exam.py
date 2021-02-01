"""KT0."""


def nr_of_common_characters(string1: str, string2: str) -> int:
    """
    Return a number of common characters of string1 and string2.

    Do not take into account repeated characters.

    common_characters("iva", "avis") -> 3 # 'a', 'i', 'v' are common
    common_characters("saali", "pall") -> 2  # 'a', 'l' are common
    common_characters("memm", "taat") -> 0
    common_characters("memm", "") -> 0

    """
    list_of_commons = []
    for x in string1:
        if x in string2:
            list_of_commons.append(x)
    updated_list = set(list_of_commons)
    return len(updated_list)


def nr_into_num_list(nr: int, num_list: list) -> list:
    """
    Return a list of numbers where the "nr" is added into the "num_list" so that the list keep going to be sorted.

    Built-in sort methods are not allowed.

    nr_into_num_list(5, []) -> [5]
    nr_into_num_list(5, [1,2,3,4]) -> [1,2,3,4,5]
    nr_into_num_list(5, [1,2,3,4,5,6]) -> [1,2,3,4,5,5,6]
    nr_into_num_list(0, [1,2,3,4,5]) -> [0,1,2,3,4,5,]

    """
    num_list.append(nr)
    updated_list = []
    while num_list:
        smallest = min(num_list)
        index = num_list.index(smallest)
        updated_list.append(num_list.pop(index))
    return updated_list


if __name__ == '__main__':
    print(nr_into_num_list(5, []))