import argparse
import cv2
import numpy as np
import transform

# -----------------------------------------------------------------------------
# WORKSHOP: KICK-ASS MOBILE DOCUMENT SCANNER
# -----------------------------------------------------------------------------
# In this codelab, we will build a 7-step document scanner using OpenCV.
# We've provided the boilerplate for argument parsing, image loading, and resizing.
# Your job is to fill in the missing OpenCV functions!
# -----------------------------------------------------------------------------

# Set up argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
args = vars(ap.parse_args())

# Load the image
image = cv2.imread(args["image"])

# Calculate ratio and resize
# Why? We resize the image to speed up processing and make edge detection more accurate.
# We keep the ratio so we can map the coordinates back to the original large image later!
ratio = image.shape[0] / 500.0
orig = image.copy()
new_width = int(image.shape[1] * (500.0 / image.shape[0]))
image = cv2.resize(image, (new_width, 500))

# -----------------------------------------------------------------------------
# STAGE 1: EDGE DETECTION
# -----------------------------------------------------------------------------

# TODO 1: Convert the resized image to grayscale.
# Hint: Use cv2.cvtColor with cv2.COLOR_BGR2GRAY
gray = None

# TODO 2: Apply a Gaussian Blur.
# Why? This removes high-frequency noise so our edge detector only focuses on the structural edges.
# Hint: Use cv2.GaussianBlur with a 5x5 kernel (e.g., (5, 5)) and 0 for sigmaX.
blurred = None

# TODO 3: Apply Canny Edge Detection.
# Why? Canny traces the strong edges in the image. The paper usually has strong edges against a dark background!
# Hint: Use cv2.Canny. Recommend thresholds 75 for minVal and 200 for maxVal.
edged = None
orig_edged = None # Keep a copy for visualization if you'd like

# -----------------------------------------------------------------------------
# STAGE 2: FINDING THE DOCUMENT CONTOUR
# -----------------------------------------------------------------------------

# TODO 4: Find contours in the edged image.
# Hint: Use cv2.findContours with cv2.RETR_LIST and cv2.CHAIN_APPROX_SIMPLE.
# Important: Sort the contours by area (cv2.contourArea) in descending order and keep only the top 5.
contours = None

# TODO 5: Loop through the contours and approximate the polygon.
# Why? We know a piece of paper is a rectangle (4 points). A rough contour might have dozens of points.
# The Douglas-Peucker algorithm simplifies the contour into fewer points.
# Hint: 
# 1. Use cv2.arcLength(c, True) to calculate the perimeter.
# 2. Use cv2.approxPolyDP(c, 0.02 * perimeter, True) to get the approximated polygon.
# 3. Stop (break) when you find a contour with exactly 4 points.
target = None

if target is not None:
    # Draw the contour we found to verify!
    cv2.drawContours(image, [target], -1, (0, 255, 0), 2)

# -----------------------------------------------------------------------------
# STAGE 3: PERSPECTIVE TRANSFORM & THRESHOLDING
# -----------------------------------------------------------------------------

# TODO 6: Apply the 4-point perspective transform.
# We provided a `transform.py` helper because the math is a bit hairy!
# Hint: Reshape your `target` to (4, 2) and multiply it by `ratio` to scale the points 
# back up to match the original, un-resized image `orig`.
dst = None

# TODO 7: Apply adaptive thresholding to the warped image.
# Why? This gives it that classic "black-and-white scanned document" look, removing shadows.
# Hint: First, convert `dst` to grayscale. Then use cv2.adaptiveThreshold or standard cv2.threshold.
th1 = None
th2 = None
th3 = None
th4 = None

# -----------------------------------------------------------------------------
# VISUALIZATION BOILERPLATE
# -----------------------------------------------------------------------------
# This code safely renders your images at each step so you can see your progress.

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
