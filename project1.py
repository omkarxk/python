import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox

# Read image
image = cv2.imread("cars.jpeg")

# Detect objects
bbox, labels, confidences = cv.detect_common_objects(image)

# Draw bounding boxes
output = draw_bbox(image, bbox, labels, confidences)

# Convert BGR to RGB
output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

# Display image
plt.imshow(output)
plt.axis("off")
plt.show()

# Count cars
print("Number of cars in this image are:", labels.count("car"))
