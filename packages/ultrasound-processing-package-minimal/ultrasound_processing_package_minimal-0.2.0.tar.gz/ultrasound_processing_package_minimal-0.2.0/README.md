Ultrasound Processing Package
Ultrasound processing package is a Python toolbox designed for the purpose of preprocessing and transformation of ultrasound images. It provides three core capabilities: Convert curved ultrasound scans into flat images, Filtering the contour of a selected object by intensity thresholding, Convert back to curved ultrasound scans. The transformations are essential for the thresholding so we can search for peaks using Cartesian coordinates instead of polar coordinates. These modules will be the fundamentals of point cloud generation based on ultrasound images.

Modules

Transformation
Masking
Backtransformation
Description
In this module we are preprocessing the image and we transform it to a “flat” format. We convert the input image to grayscale and detect centimeter calibration marks along both axes. The image is then cleaned by removing irrelevant top and side regions and outlier pixel values. Based on peak detection, the module estimates the geometric parameters of the scan area and transducer settings, such as the offset and scanning depth. Using trigonometric relations, it constructs a polar-to-Cartesian grid. We use bilinear interpolation to project the image onto a uniform Cartesian space.

In this module, we first generate a binary mask by thresholding the input image: pixels with intensity at or above the specified threshold are set to white (255), and those below are set to black (0). After removing noise components, we scan each column to select the very first pixel whose intensity exceeds the threshold, building an initial contour mask. Next, we apply OpenCV’s functions to thicken that contour for clear visualization. Finally, we apply the dilated contour as a mask to preserve and display the original pixel intensities.

In this module we reverse the transformation process, converting polar image data back into Cartesian coordinates. We first initialize key transformation parameters and build a 3D volume grid using spherical coordinates. The grid is filtered to exclude regions outside the region of interest. Using bilinear interpolation, we project back the masked image to the grid.

Description for screen readers
Usage
Installation
To install:

pip install ultrasound-processing
Make sure to set the proper paths to the files.

Requirements
Python 3.7 or higher

NumPy

OpenCV

Matplotlib

Scikit-image

Scipy

Example
Hyperlinked notebook: Example notebook: https://colab.research.google.com/drive/1oPVk-Xz7DNJN8D62u-W9EvBfp888eNbn?usp=drive_link&fbclid=IwZXh0bgNhZW0CMTAAYnJpZBExd01nUUQwS1BnTHRZVm9nWAEelMZ_Ceij4MhnwL6WAQnS0KMlBrRlq8caeR8p16TLadw5SM7CTunasN43ViY_aem_I1iV0fEzjY5-xPhcnNtlHw

Github repository link:

https://github.com/Mart-SciecPyt/ScPytone_ultrasound_processing

Readthedocs:
https://ultrasound-processing-minimal.readthedocs.io/en/latest/