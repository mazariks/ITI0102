"""Test 1 (K14)."""


def workday_count(days):
    """
    Given number of days.

    Return how many of these days are workdays.
    Workdays are first five days of the weeks, last two are not.
    Always start from the start of the week.

    workday_count(9) => 7
    workday_count(3) => 3
    workday_count(7) => 5
    workday_count(15) => 11

    :param days: given number of days
    :return: workdays in given days
    """
    if days <= 5:
        return days
    elif days in range(5, 8):
        return 5
    else:
        day = days % 7
        weeks = days // 7
        print(f"{day}")
        print(f"{weeks}")
        if day == 0:
            return days - (2 * weeks)
        else:
            return 5 * weeks + day


def caught_speeding(speed, is_birthday):
    """
    Return which category speeding ticket you would get.

    You are driving a little too fast, and a police officer stops you.
    Write code to compute the result, encoded as an int value:
    0=no ticket, 1=small ticket, 2=big ticket.
    If speed is 60 or less, the result is 0.
    If speed is between 61 and 80 inclusive, the result is 1.
    If speed is 81 or more, the result is 2.
    Unless it is your birthday -- on that day, your speed can be 5 higher in all cases.

    caught_speeding(60, False) => 0
    caught_speeding(65, False) => 1
    caught_speeding(65, True) => 0

    :param speed: Speed value.
    :param is_birthday: Whether it is your birthday (boolean).
    :return: Which category speeding ticket you would get (0, 1, 2).
    """
    allowed_speed = 60
    wrong1 = range(61, 81)
    if is_birthday:
        allowed_speed = 65
        wrong1 = range(65, 86)
    if speed <= allowed_speed:
        return 0
    elif speed in wrong1:
        return 1
    else:
        return 2


def first_half(text):
    """
    Return the first half of an string.

    The length of the string is even.

    first_half('HaaHoo') => 'Haa'
    first_half('HelloThere') => 'Hello'
    first_half('abcdef') => 'abc'
    """
    middle_index = len(text) // 2
    return text[:middle_index]


def last_indices_elements_sum(nums):
    """
    Return sum of elements at indices of last two elements.

    Take element at the index of the last element value
    and take element at the index of the previous element value.
    Return the sum of those two elements.

    If the index for an element is out of the list, use 0 instead.

    The list contains at least 2 elements.

    last_indices_elements_sum([0, 1, 2, 0]) => 2 (0 + 2)
    last_indices_elements_sum([0, 1, 1, 7]) => 1 (just 1)
    last_indices_elements_sum([0, 1, 7, 2]) => 7 (just 7)
    last_indices_elements_sum([0, 1, 7, 8]) => 0 (indices too large, 0 + 0)

    :param nums: List of non-negative integers.
    :return: Sum of elements at indices of last two elements.
    """
    first_value = 0
    second_value = 0
    first_index = nums[-1]
    second_index = nums[-2]
    if first_index <= len(nums) - 1:
        first_value = nums[first_index]
    if second_index <= len(nums) - 1:
        second_value = nums[second_index]
    return first_value + second_value


def max_duplicate(nums):
    """
    Return the largest element which has at least one duplicate.

    If no element has duplicate element (an element with the same value), return None.

    max_duplicate([1, 2, 3]) => None
    max_duplicate([1, 2, 2]) => 2
    max_duplicate([1, 2, 2, 1, 1]) => 2

    :param nums: List of integers
    :return: Maximum element with duplicate. None if no duplicate found.
    """
    list_of_duplicates = []
    for i in nums:
        if nums.count(i) >= 2:
            list_of_duplicates.append(i)
    list_of_duplicates_set = set(list_of_duplicates)
    if not list_of_duplicates_set:
        return None
    return max(list_of_duplicates_set)


if __name__ == '__main__':
    print(workday_count(13))
    print(caught_speeding(50, False))
    print(caught_speeding(65, False))
    print(caught_speeding(65, True))
    print(first_half("HelloThere"))
    print(first_half("HaaHoo"))
    print(first_half("abcdef"))
    print(last_indices_elements_sum([0, 1, 2, 0]))
    print(last_indices_elements_sum([0, 1, 1, 7]))
    print(last_indices_elements_sum([0, 1, 7, 2]))
    print(last_indices_elements_sum([0, 1, 7, 8]))
    print(max_duplicate([1, 2, 3, 1]))
    print(max_duplicate([1, 2, 2, 1, 1]))
    print(max_duplicate([1, 2, 3]))
    print(max_duplicate([]))
