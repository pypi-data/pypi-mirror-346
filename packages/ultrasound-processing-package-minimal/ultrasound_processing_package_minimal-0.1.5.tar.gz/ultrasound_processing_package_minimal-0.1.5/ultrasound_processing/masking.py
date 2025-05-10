import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def compute_threshold(image: np.ndarray, top_percent: float) -> int:
    """
    Compute the intensity threshold such that the top top_percent fraction of pixel values
    in the grayscale image will be set to white in the binary mask.

    Args:
        image: 2D numpy array of grayscale pixel intensities (0-255).
        top_percent: Number between 0 and 1 that determines the fraction of pixels to be set to white.

    Returns:
        An integer threshold value in the range [0, 255].
    """
    hist, _ = np.histogram(image.flatten(), bins=256, range=[0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf / float(cdf[-1])
    idx = np.where(cdf_normalized >= top_percent)[0]
    return int(idx[0]) if idx.size > 0 else 255

def threshold_mask(image: np.ndarray, threshold_value: int) -> np.ndarray:
    """
    Create a binary mask by thresholding the image: pixels with intensity >= threshold_value
    become 255 (white), others become 0 (black).

    Args:
        image: 2D numpy array of grayscale pixel intensities.
        threshold_value: Intensity cutoff for binarization.

    Returns:
        A binary mask as a 2D numpy array of 0s and 255s.
    """
    return (image >= threshold_value).astype(np.uint8) * 255


def do_closing(mask: np.ndarray, kernel_size: Tuple[int,int]=(2,2)) -> np.ndarray:
    """
    Apply a morphological closing operation (dilation followed by erosion) to fill small holes
    and connect nearby white regions in the binary mask.

    Args:
        mask: Binary mask (0 or 255) to be processed.
        kernel_size: Size of the structuring element used for closing.

    Returns:
        The mask after morphological closing.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

def remove_small_components(mask: np.ndarray, top_margin: int) -> np.ndarray:
    """
    Remove white components (noise) from the top part of the image.

    Args:
        mask: Binary mask (0 or 255) (after closing).
        top_margin: Number of pixels from the top; any component starting above this
                    line will be removed.

    Returns:
        The mask with small top components removed.
    """
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if y < top_margin:
            mask[labels == i] = 0
    return mask

def extract_top_contour(mask: np.ndarray) -> np.ndarray:
    """
    Extract the top contour of the white regions in the binary mask by keeping only the first
    white pixel in each column.

    Args:
        mask: Cleaned binary mask (0 or 255).

    Returns:
        A binary image where each column has at most one white pixel.
    """
    h, w = mask.shape
    contour = np.zeros_like(mask)
    for col in range(w):
        white = np.where(mask[:, col] == 255)[0]
        if white.size > 0:
            contour[white[0], col] = 255
    return contour

def dilate_contour(contour: np.ndarray,
                   kernel_size: Tuple[int,int]=(2,2),
                   iterations: int=1) -> np.ndarray:
    """
    Thicken the one- pixel-wide contour by applying dilation.

    Args:
        contour: Binary contour image (0 or 255) with single-pixel lines.
        kernel_size: Size of the rectangular structuring element.
        iterations: Number of dilation iterations.

    Returns:
        The dilated contour mask.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.dilate(contour, kernel, iterations=iterations)

def smooth_mask(dilated: np.ndarray,
                blur_ksize: Tuple[int,int]=(5,5)) -> np.ndarray:
    """
    Apply a Gaussian blur to the dilated contour mask.

    Args:
        dilated: Dilated binary contour mask.
        blur_ksize: Kernel size for Gaussian blur.

    Returns:
        A smooth mask with values in [0, 255].
    """
    blurred = cv2.GaussianBlur(dilated, blur_ksize, 0)
    blurred[dilated == 255] = 255
    return blurred

def original_intensity_mask(image: np.ndarray, smooth: np.ndarray) -> np.ndarray:
    """
    Preserve the original grayscale intensities.

    Args:
        image: Original 2D grayscale image.
        smooth: Smooth mask with values in [0, 255].

    Returns:
        Masked image where the contour regions preserve their original intensities.
    """
    norm = smooth.astype(np.float32) / 255.0
    return (image.astype(np.float32) * norm).astype(np.uint8)



def mask(image: np.ndarray,
          top_percent: float = 0.93,
          top_margin: int = 5,
          apply_closing_flag: bool = True) -> np.ndarray:
    """
    Complete pipeline that generates a masked ultrasound image that keeps only the contour of a certain object.

    Args:
        image: Input 2D grayscale image.
        top_percent: Fraction of pixels to threshold as white (default 0.93).
        top_margin: Pixel row margin to remove top noise components (default 5).
        apply_closing_flag: Whether to perform morphological closing (default True).

    Returns:
        A grayscale image where only the contour region retains its original intensities.
    """
    th = compute_threshold(image, top_percent)
    mask = threshold_mask(image, th)

    if apply_closing_flag:
        mask = do_closing(mask)

    mask = remove_small_components(mask, top_margin)
    contour = extract_top_contour(mask)
    dilated = dilate_contour(contour)
    smooth = smooth_mask(dilated)
    return original_intensity_mask(image, smooth)