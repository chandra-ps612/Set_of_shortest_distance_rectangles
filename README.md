# set_of_shortest_distance_rectangles

This repository talks about ``` Classical Computer Vision ``` approach.
The task is to find out the set of the shortest distance rectangles- 
case- I

Overlapping rectangles

case II

Reference: test.png

The steps involved are as follows-
1. ```Thresholding``` method to convert input image to binary format  
2. ```cv2.findContours()``` and ```cv2.drawContours()```methods to find 
   and detect contours
3. Calculate the centroids of each detected rectangle
4. Calculate the euclidean distance between all possible centroids
