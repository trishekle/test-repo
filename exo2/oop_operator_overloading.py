# OOP Problems
## Operator Overloading
### Problem 1
# Implement a complex number class. Overload the addition and subtraction operators to add and subtract two complex numbers.
def __add__(self, other):
    if isinstance(other, ComplexNumber):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)
    return NotImplemented

def __sub__(self, other):
    if isinstance(other, ComplexNumber):
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)
    return NotImplemented

def __repr__(self):
    return f"{self.real} + {self.imaginary}i"

### Problem 2
# Create a class `Person` with `name`, `age` and `gender` as its attributes. Overload the `>` operator to compare two persons based on their age, such that `p1 > p2` returns `True` if the age of `p1` is greater than `p2` and `False` otherwise.

def __person_init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

def __gt__(self, other):
    if isinstance(other, Person):
        return self.age > other.age
    return NotImplemented

### Problem 3
# Create a class `Vector` that represents a vector in space, with `x`, `y`, and `z` as its attributes. Overload the `*` operator to return the dot product of two vectors, such that `vector1 * vector2` returns the dot product of the two input vectors.
def __vector_init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

def __mul__(self, other):
    if isinstance(other, Vector):
        return self.x * other.x + self.y * other.y + self.z * other.z
    return NotImplemented

### Problem 4
# Overload all comparison operators (`<`, `>`, `==`, `!=`, `>=`, `<=`) for a `Circle` class based on radius.

def __circle_init__(self, radius): # this is the constructor for the Circle class
    self.radius = radius

def __lt__(self, other): # overloading the less than operator
    if isinstance(other, Circle):
        return self.radius < other.radius
    return NotImplemented

def __gt__(self, other): # overloading the greater than operator
    if isinstance(other, Circle):
        return self.radius > other.radius
    return NotImplemented

def __eq__(self, other): # overloading the equality operator
    if isinstance(other, Circle):
        return self.radius == other.radius
    return NotImplemented

def __ne__(self, other): # overloading the not equal operator
    if isinstance(other, Circle):
        return self.radius != other.radius
    return NotImplemented

def __ge__(self, other): # overloading the greater than or equal to operator
    if isinstance(other, Circle):
        return self.radius >= other.radius
    return NotImplemented

def __le__(self, other): # overloading the less than or equal to operator
    if isinstance(other, Circle):
        return self.radius <= other.radius
    return NotImplemented

### Problem 5
#Implement a 2D point class. Overload the comparison operators to compare two points based on their Euclidean distance from the origin.
#Euclidean distance = `sqrt(x² + y²)`

def _point_init__(self, x, y): # this is the constructor for the Point class
    self.x = x
    self.y = y

def _distance_from_origin(self): # this method calculates the Euclidean distance of the point from the origin (0, 0)
    return (self.x ** 2 + self.y ** 2) ** 0.5


### Problem 6
# Overload the multiplication operator for two matrices.

def _matrix_init__(self, data): # this is the constructor for the Matrix class
    self.data = data
    self.rows = len(data)
    self.cols = len(data[0]) if data else 0

def _matrix_mul__(self, other): # overloading the multiplication operator for matrix multiplication
    if isinstance(other, Matrix):
        if self.cols != other.rows:
            raise ValueError("Incompatible dimensions for matrix multiplication.")
        result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)
    return NotImplemented
