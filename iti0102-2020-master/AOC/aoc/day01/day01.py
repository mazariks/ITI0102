

with open("input.txt", "r+") as file:
    final_list = []
    for line in file.readlines():
        if "\n" in line:
            line = line[:-1]
        final_list.append(int(line))
print(final_list)

amount = 2020
for first_index in range(len(final_list)):
    for second_index in range(first_index, len(final_list)):
        for third_index in range(second_index, len(final_list)):
            if final_list[first_index] + final_list[second_index] + final_list[third_index] == amount:
                print(final_list[first_index] * final_list[second_index] * final_list[third_index])
