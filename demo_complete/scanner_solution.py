import argparse
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import transform

# Set up argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
args = vars(ap.parse_args())

# Load the image
image = cv2.imread(args["image"])

# Calculate ratio and resize
ratio = image.shape[0] / 500.0
orig = image.copy()
new_width = int(image.shape[1] * (500.0 / image.shape[0]))
image = cv2.resize(image, (new_width, 500))

# TODO 1: Convert the resized image to grayscale.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# TODO 2: Apply a Gaussian Blur (recommend a 5x5 kernel) to remove high-frequency noise.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# TODO 3: Apply Canny Edge Detection (recommend thresholds 75 and 200).
edged = cv2.Canny(blurred, 75, 200)
orig_edged = edged.copy()

# TODO 4: Find contours (cv2.findContours) using RETR_LIST and CHAIN_APPROX_SIMPLE. Sort them by area in descending order and keep only the top 5.
(contours, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

# TODO 5: Loop through the contours and approximate the polygon using the Douglas-Peucker algorithm (cv2.approxPolyDP). Hint: Use cv2.arcLength to calculate the perimeter first, and set epsilon to 0.02 * perimeter. Stop when you find a contour with exactly 4 points.
target = None
for c in contours:
    p = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * p, True)

    if len(approx) == 4:
        target = approx
        break

# TODO 6: Apply the 4-point perspective transform using the helper function. Hint: Remember to reshape the 4 points and multiply them by the ratio to scale them back to the original, un-resized image.
if target is not None:
    cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
    target_scaled = target.reshape(4, 2) * ratio
    dst = transform.four_point_transform(orig, target_scaled)
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
else:
    dst = orig.copy()
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

# TODO 7: Apply adaptive thresholding to the warped image to give it a black-and-white scanned look (Hint: use cv2.adaptiveThreshold or threshold_local).
ret, th1 = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
ret2, th4 = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

if orig is not None:
    cv2.imshow("Original.jpg", orig)
if gray is not None:
    cv2.imshow("Original Gray.jpg", gray)
if blurred is not None:
    cv2.imshow("Original Blurred.jpg", blurred)
if orig_edged is not None:
    cv2.imshow("Original Edged.jpg", orig_edged)
if image is not None:
    cv2.imshow("Outline.jpg", image)
if th1 is not None:
    cv2.imshow("Thresh Binary.jpg", th1)
if th2 is not None:
    cv2.imshow("Thresh mean.jpg", th2)
if th3 is not None:
    cv2.imshow("Thresh gauss.jpg", th3)
if th4 is not None:
    cv2.imshow("Otsu's.jpg", th4)
if dst is not None:
    cv2.imshow("dst.jpg", dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
