import cv2
import numpy as np
import math

input_image_path = 'The path of input image'
output_image_path = 'The path to save output image'

# Reading image
img = cv2.imread(input_image_path)
print(img.shape)

# Converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
'''
Here, Simple thresholding method is using to convert gray-scale image to binary format(either 0 or 255). Pixel
values greater than 200 will be converted in 255 and pixel values less than 200 will be converted in 0.
'''
T, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
'''
Contours can be explained simply as a curve joining all the continuous points(along boundary) having the same
colour and intensity.
cv2.findContours() method return three values viz. input image array, contours, and hierarchy
It is used to find all boundary points(x, y) of objects in a image.
I used cv2.CHAIN_APPROX_NONE method of Contours Approximation Methods to capture all boundary points.
I used cv2.RETR_TREE mode of Contours Retrieval Modes to get retrieves all the contours and creates a
full family hierarchy list.
'''
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contours))

# Using contours i.e. list in enumerate() function to iteratively get each contour along with index values
contour_centroids = {}  # Empty dictionary to store each contour centroid value
contour_area = []  # Empty list to store each contour area
keys = []  # Empty list to store contour_centroids dictionary key iteratively
values = []  # Empty list to store contour_centroids dictionary value iteratively

for idx, contour in enumerate(contours):
	'''
	cv2.findContours() method considers whole image as a shape so
	ignoring index value = 0.
	'''
	if idx == 0:
		idx = 1
		continue

	# cv2.approxPloyDP() function to approximate the shape
	# Here, the perimeter of each contour is caluculated by cv2.arcLength(contour, True) method
	approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
	print(len(approx))

	# Using drawContours() function
	# Negative contourIDx is used to draw all the contours
	cv2.drawContours(img, [contour], -1, (255, 0, 0), 2)

	'''cv2.moments() method returns a dictionary
	Here,
	m00 = count of non-zero pixels in input image array
	m10 = sum of all non-zero pixels (x-axis) in input image array
	m01 = sum of all non-zero pixels (y-axis) in input image array
	'''
	M = cv2.moments(contour)
	if M['m00'] != 0.0:
		x = int(M['m10']/M['m00'])
		print(f'x-{str(idx)}:{x}')
		y = int(M['m01']/M['m00'])
		print(f'y-{str(idx)}:{y}')
		contour_area.append(M['m00'])
		keys.append('R-'+str(idx))
		values.append((x, y))

		# Dictionary comprehension method to update contour_centroids iteratively
		contour_centroids = {key: value for key, value in zip(keys, values)}

		# Writing name of each rectangle shape with abbreviation 'R' followed by index value
		if len(approx) == 4:
			cv2.putText(img, 'R-'+str(idx), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
			cv2.circle(img, (x, y), 0, (0, 0, 0), 5)

'''
Using Euclidean distance formula to calculate distance among centroids of rectangles to
find out the closest set of rectangles.
For the time being, logic is created for 4 rectangles to find out the closest set of rectangles
based on euclidean distance calculated wrt all four centroids. If the euclidean distance between
two centroids is minimum compare to others then both rectangles will be the closest or the case of
overlapping rectangles.
Here,
R12 - Euclidean distance between centroids R1 and R2
R13 - Euclidean distance between centroids R1 and R3
R14 - Euclidean distance between centroids R1 and R4
R23 - Euclidean distance between centroids R2 and R3
R24 - Euclidean distance between centroids R2 and R4
R34 - Euclidean distance between centroids R3 and R4
If there are 4 rectangles in a given scene. so technically, we will have 6 ways to calculate distance
among all four rectangles wrt centroids.
'''
cnt_1 = 1
cnt_2 = 1
cnt_3 = 1
d_wrt_R1 = {}
d_wrt_R2 = {}
d_wrt_R3 = {}
values_1 = []
values_2 = []
values_3 = []
for k, v in contour_centroids.items():
	#k = contour_centroids.keys()
	v = list(contour_centroids.values())
	if v == v[:] and cnt_1 != 4:
		d_1 = math.sqrt((v[0][0] - v[cnt_1][0])**2 + (v[0][1] - v[cnt_1][1])**2)
		cv2.line(img, (v[0][0], v[0][1]), (v[cnt_1][0], v[cnt_1][1]), (0, 0, 255), 2)
		keys = ['R12', 'R13', 'R14']
		values_1.append(int(d_1))
		d_wrt_R1 = {key: value for key, value in zip(keys, values_1)} # Dict Comprehension to create Dict
		cnt_1 += 1

	if v == v[:] and cnt_2 != 3:
		d_2 = math.sqrt((v[1][0] - v[cnt_2+1][0])**2 + (v[1][1] - v[cnt_2+1][1])**2)
		cv2.line(img, (v[1][0], v[1][1]), (v[cnt_2+1][0], v[cnt_2+1][1]), (0, 255, 0), 2)
		keys = ['R23', 'R24']
		values_2.append(int(d_2))
		d_wrt_R2 = {key: value for key, value in zip(keys, values_2)} # Dict Comprehension to create Dict
		cnt_2 += 1

	if v == v[:] and cnt_3 != 2:
		d_3 = math.sqrt((v[2][0] - v[cnt_3+2][0])**2 + (v[2][1] - v[cnt_3+2][1])**2)
		cv2.line(img, (v[2][0], v[2][1]), (v[cnt_3+2][0], v[cnt_3+2][1]), (255, 0, 0), 2)
		keys = ['R34']
		values_3.append(int(d_3))
		d_wrt_R3 = {key: value for key, value in zip(keys, values_3)} # Dict Comprehension to create Dict
		cnt_3 += 1

print(f'Distance wrt centroid R-1:\n{d_wrt_R1}')
print(f'Distance wrt centroid R-2:\n{d_wrt_R2}')
print(f'Distance wrt centroid R-3:\n{d_wrt_R3}')
print(f'contour_area: {contour_area}')
print(f'contour_centroids: {contour_centroids}')

# Displaying the image after drawing contours
cv2.imshow('shapes', img)
cv2.imwrite(output_image_path, img)
cv2.waitKey(0)
cv2.destroyAllWindows()