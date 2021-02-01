"""Meta-trees and meta-dragons."""

from turtle import Turtle
from sys import setrecursionlimit

setrecursionlimit(10000)


def tree(length):
    """
    Write a recursive turtle program to draw a binary tree.

    Start with a trunk 200px tall.
    Each new branch should be 3/5 as big as its trunk.
    Minimum branch size is 5px.
    Move turtle with: t.forward(), t.left(), t.right(), tree()

    :param length: height of the trunk or leaf
    """
    # https://www.geeksforgeeks.org/y-fractal-tree-in-python-using-turtle/
    if length > 5:
        # base
        t.forward(length)
        t.left(60)

        # left subtree
        tree(0.6 * length)
        # Angle between branches
        t.right(120)

        # right subtree
        tree(0.6 * length)
        t.left(60)
        # Get back to the start of "trunk" after drawing
        t.forward(-length)


def apply_dragon_rules(string):
    """
    Write a recursive function that replaces characters in string.

    Like so:
        "a" -> "aRbFR"
        "b" -> "LFaLb"
    apply_dragon_rules("a") -> "aRbFR"
    apply_dragon_rules("aa") -> "aRbFRaRbFR"
    apply_dragon_rules("FRaFRb") -> "FRaRbFRFRLFaLb"

    :param string: sentence with "a" and "b" characters that need to be replaced
    :return: new sentence with "a" and "b" characters replaced
    """
    string_to_replace = ""
    if len(string) > 0:
        if string[0] == 'a':
            string_to_replace += "aRbFR"
            return string_to_replace + apply_dragon_rules(string[1:])
        elif string[0] == 'b':
            string_to_replace += "LFaLb"
            return string_to_replace + apply_dragon_rules(string[1:])
        else:
            string_to_replace += string[0]
            return string_to_replace + apply_dragon_rules(string[1:])
    else:
        return string_to_replace


def curve(string, depth):
    """
    Recursively generate the next depth of rules.

    Calls apply_dragon_rules() function `depth` times.
    curve("Fa", 2) -> "FaRbFRRLFaLbFR"

    :param string: current instruction string
    :param depth: how many times the rules are applied
    :return: instructionset at iteration 'depth'
    """
    newer_string = ""
    if depth > 0:
        newer_string += apply_dragon_rules(string)
        string = newer_string
        return curve(string, depth - 1)
    else:
        return string


def format_curve(string):
    """
    Use recursions to remove  a  and  b  symbols from the instruction string.

    format_curve("Fa") -> "F"
    format_curve("FaRbFR") -> "FRFR"

    :param string: instruction string
    :return: clean instructions with only "F", "R", and "L" characters
    """
    newer_string = ""
    if string[0] != "a" and string[0] != "b":
        newer_string += string[0]
    if len(string) > 1:
        return newer_string + format_curve(string[1:])
    else:
        return newer_string


def draw_dragon(string, length):
    """Draw the dragon by reading the string recursively.

    Use t.right(), t.left(), t.forward() and draw_dragon() to move turtle.
        L - means turn 90 degrees to left and go forward
        R - means turn 90 degrees to right and go forward
        F - means don't turn just go forward

    :param string: instructions left to process
    :param length: how many pixels to move forward, left or right
    """
    if string[0] == "F":
        t.forward(length)
    elif string[0] == "R":
        t.right(90)
        t.forward(length)
    elif string[0] == "L":
        t.left(90)
        t.forward(length)
    if len(string) > 1:
        return draw_dragon(string[1:], length)
    else:
        return


def get_line_length(dragon_width, depth):
    """Return one Turtle step length if the width and depth are known."""
    return dragon_width / (2 ** (1 / 2)) ** depth


def save(t: Turtle):
    """Save the turtle graphic to file which can be opened with a image editor like GIMP."""
    t.ht()  # hide him
    t.getscreen().getcanvas().postscript(file='tree.ps')


if __name__ == '__main__':
    t = Turtle()
    t.getscreen().bgcolor("#1c262b")
    t.color("#96004f")
    t.speed(0)
    t.left(90)
    #tree(200)

    s = curve("Fa", 8)
    s = format_curve(s)
    l_ = get_line_length(100, 8)
    print(s)
    draw_dragon(s, l_)

    save(t)
    t.getscreen().exitonclick()
