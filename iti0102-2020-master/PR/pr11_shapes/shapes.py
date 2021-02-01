"""Shapes."""
from math import pi


class Shape:
    """General shape class."""

    def __init__(self, color: str):
        """Constructor, sets the color."""
        self._color = color

    def set_color(self, color: str):
        """Set the color of the shape."""
        self._color = color

    def get_color(self) -> str:
        """Get the color of the shape."""
        return self._color

    def get_area(self) -> float:
        """Get area method which every subclass has to override."""
        return 15.0


class Circle(Shape):
    """Circle is a subclass of Shape."""

    def __init__(self, color: str, radius: float):
        """
        Constructor of the circle.

        The color is stored using superclass constructor:
        super().__init__(color)

        The radius value is stored here.
        """
        super().__init__(color)
        self._radius = radius

    def __repr__(self) -> str:
        """
        Return representation of the circle.

        For this exercise, this should return a string:
        Circle (r: {radius}, color: {color})
        """
        return f"Circle (r: {self._radius}, color: {self.get_color()})"

    def get_area(self) -> float:
        """
        Calculate the area of the circle.

        Area of the circle is pi * r * r.
        """
        return pi * self._radius * self._radius


class Square(Shape):
    """Square is a subclass of Shape."""

    def __init__(self, color: str, side: float):
        """
        Constructor of the square.

        The color is stored using superclass constructor:
        super().__init__(color)

        The side value is stored here.
        """
        super().__init__(color)
        self._side = side

    def __repr__(self) -> str:
        """
        Return representation of the square.

        For this exercise, this should return a string:
        Square (a: {side}, color: {color})
        """
        return f"Square (a: {self._side}, color: {self.get_color()})"

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the circle is side * side.
        """
        return self._side ** 2


class Rectangle(Shape):
    """Rectangle is a subclass of Shape."""

    def __init__(self, color: str, length: float, width: float):
        """
        Constructor of the rectangle.

        The color is stored using superclass constructor:
        super().__init__(color)

        The length and width values are stored here.
        """
        super().__init__(color)
        self._width = width
        self._length = length

    def __repr__(self):
        """
        Return representation of the rectangle..

        For this exercise, this should return a string:
        Rectangle (w: {width}, l: {length} , color: {color})
        """
        return f"Rectangle (l: {self._length}, w: {self._width}, color: {self.get_color()})"

    def get_area(self) -> float:
        """
        Calculate the area of the rectangle.

        Area of the circle is width * length.
        """
        return self._width * self._length


class Paint:
    """The main program to manipulate the shapes."""

    def __init__(self):
        """Constructor should create a list to store all the shapes."""
        self.list_of_shapes = []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the program."""
        if shape not in self.list_of_shapes:
            self.list_of_shapes.append(shape)

    def get_shapes(self) -> list:
        """Return all the shapes."""
        return self.list_of_shapes

    def calculate_total_area(self) -> float:
        """Calculate total area of the shapes."""
        sum_of_areas = 0
        for value in self.list_of_shapes:
            area = value.get_area()
            sum_of_areas += area
        return sum_of_areas

    def get_shapes_of_type(self, shape: object) -> list:
        """Return list of shapes we need."""
        list_to_return = []
        for value in self.list_of_shapes:
            if isinstance(value, shape):
                list_to_return.append(value)
        return list_to_return

    def get_circles(self) -> list:
        """Return only circles."""
        return self.get_shapes_of_type(Circle)

    def get_squares(self) -> list:
        """Return only squares."""
        return self.get_shapes_of_type(Square)

    def get_rectangles(self) -> list:
        """Return only rectangles."""
        return self.get_shapes_of_type(Rectangle)


if __name__ == '__main__':
    paint = Paint()
    circle = Circle("blue", 10)
    square = Square("red", 11)
    rectangle = Rectangle("grey", 10, 20)  # 'Rectangle (l: 10, w: 20, color: gray)'
    paint.add_shape(rectangle)
    paint.add_shape(circle)
    paint.add_shape(square)
    print(paint.get_squares())
    print(paint.calculate_total_area())
    print(paint.get_shapes_of_type(Circle))
