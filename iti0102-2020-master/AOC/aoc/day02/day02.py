with open("day02.txt", "r+") as file:
    list_of_data = []
    final_dict = {}
    for line in file.readlines():
        if "\n" in line:
            line = line[:-1]
        splitted_line = [x.strip() for x in line.split(":")]
        list_of_data.append(splitted_line)
        if splitted_line[0] in final_dict.keys():
            final_dict[splitted_line[0]] += [splitted_line[1]]
        else:
            final_dict[splitted_line[0]] = [splitted_line[1]]

counter = 0
for key, value in final_dict.items():
    watched_char = key.split(" ")[1]
    allowed_counting = key.split(" ")[0].split("-")
    first_occurence = int(allowed_counting[0]) - 1
    last_occurence = int(allowed_counting[1]) - 1
    for every_value in value:
        if (every_value[first_occurence] == watched_char and every_value[last_occurence] != watched_char) or \
                (every_value[last_occurence] == watched_char and every_value[first_occurence] != watched_char):
            counter += 1

print(counter)
