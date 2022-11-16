'''
The standard form of line is given by-
a*x + b*y + c
Where,
x, and y are variables
a, b, and c are constants
The distance of line from the point (x, y) is calculated by the formula-
(a*x + b*y + c)/ (a**2 + b**2)**0.5

Case - I
If d < r, line will intersect the circle
Case - II
If d > r, line will be outside of the circle
Case - III
If d = 0, line will pass through the center of the circle
Line ax + by + c and diameter of the circle will be colinear.
'''
#import matplotlib.pyplot as plt
import math

# Assuming, the center of circle-
x = 0
y = 0 

a = int(input('Enter the value of variable a:\n'))
b = int(input('Enter the value of variable b:\n'))
c = int(input('Enter the value of variable c:\n'))

# Taking a random value of the radius of circle 
r = 5

# The distance of line from the point (0, 0) is -
d = c/math.sqrt(a**2 + b**2) 

'''
Using if-elif-else ladder
Condition i.e. '(d < r and d != 0)' in if statement is used to make if-elif-else ladder flexible to meet
all the three cases below.
'''
if (d < r and d != 0):
	print('Given line is intersecting circle of center coordinates (0, 0)')

elif (d > r):
	print('Given line lies outside of the circle of center coordinates (0, 0)')
else:
	print('Given line passes through the circle of center coordinates (0, 0)')
