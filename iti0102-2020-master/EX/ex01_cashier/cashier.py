"""EX01."""

# It also can be done like this, but using loops is much more easier and faster:
"""given_money = int(input("Enter a sum: "))
new_list = []
fifty = given_money // 50
twenty = given_money % 50 // 20
ten = given_money % 50 % 20 // 10
five = given_money % 50 % 20 % 10 // 5
one = given_money % 50 % 20 % 10 % 5 // 1
amount_of_coins = 0
if fifty != 0:
    new_list.append(fifty)
if twenty != 0:
    new_list.append(twenty)
if ten != 0:
    new_list.append(ten)
if five != 0:
    new_list.append(five)
if one != 0:
    new_list.append(one)
for i in new_list:
    amount_of_coins += i
print(f"Amount of coins needed: {amount_of_coins}") """


coins = [50, 20, 10, 5, 1]  # All possible coins for a change.
given_money = int(input("Enter a sum: "))
needed_coins = []
for i in coins:
    while i <= given_money:  # while loop helps program counting repeated coins.
        needed_coins.append(i)
        given_money -= i  # after adding an element we should decrease an amount of change we need to give back.
print(f"Amount of coins needed: {len(needed_coins)}")
