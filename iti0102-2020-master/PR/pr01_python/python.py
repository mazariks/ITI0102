"""PR01."""


python_born = 2008
ask_name = input("What is your name?")
print(f"Hello, {ask_name}! What year were you born in?")
ask_year = int(input())
if ask_year > python_born:
    written_age = ask_year - python_born
    print(f"Python 3 was {written_age} years old when you were born.")
else:
    written_age = python_born - ask_year
    print(f"You were {written_age} years old when Python 3.0 was released.")
