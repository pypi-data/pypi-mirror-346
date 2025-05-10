import numpy as np
import scipy.signal
import math as m

def convert_to_grayscale(image):
    """
    Converts a PIL image to a grayscale NumPy array.

    Args:
        image (PIL.Image.Image): Input image in PIL.Image format.

    Returns:
        np.ndarray: Grayscale image as a 2D NumPy array.
    """

    return np.array(image.convert("L"))



def detect_cm_marks(gray_array):
    """
    Detects centimeter marks in the grayscale image along rows and columns.

    Args:
        gray_array (np.ndarray): Grayscale image array.

    Returns:
        Tuple[float, List[int], List[int]]: 
            - Estimated distance in pixels between cm marks (float).
            - List of detected row indices (List[int]).
            - List of detected column indices (List[int]).
    """

    def find(line):
        marks, prev = [], False
        for i, val in enumerate(line):
            curr = val > 10
            dist = True
            if marks: dist = i - marks[-1] > 10
            if curr and not prev and dist:
                marks.append(i) 
            prev = curr
        return marks
    
    rows = find(gray_array[:,2])
    cols = find(gray_array[2])
    d = ((rows[-1] - rows[1]) + (cols[-1] - cols[1])) / (len(rows) + len(cols) - 4)

    return d, rows, cols



def clean_image(gray_array):
    """
    Cleans the grayscale image by cropping and filtering pixel values.

    Args:
        gray_array (np.ndarray): Grayscale image array.

    Returns:
        Tuple[np.ndarray, int]: 
            - Processed image as a float array with noise filtered.
            - Index of the first row retained after cropping.
    """

    idx = np.where(np.sum(gray_array, axis=1) < 500)[0][0]
    img = gray_array[idx:, 6:].astype(float)
    img[(img > 200) | (img < 5)] = 0
    img[:100,:100], img[:100,-100:] = 0, 0

    return img, idx



def calculate_geometry(temp, d, alpha):
    """
    Calculates geometric parameters from the ultrasound image.

    Args:
        temp (np.ndarray): Cleaned image array.
        d (float): Pixel-to-centimeter ratio.
        alpha (float): Half angle of the ultrasound beam in radians.

    Returns:
        Tuple[float, int, float, float, int]: 
            - Depth of the offset in pixels.
            - Height in pixels of the ultrasound window.
            - Offset in centimeters.
            - Height in centimeters of the ultrasound window.
            - First row index of the window.
    """

    row = np.where(np.sum(temp, axis = 1) > 200)[0][0]
    peaks = scipy.signal.find_peaks(temp[row], distance=50)[0]
    cln = peaks[abs(peaks) <= len(temp[0]) * 4 / 5]
    d_cm = abs(cln[0] - cln[1]) / (2 * d)
    offset_cm = d_cm / m.sin(alpha)
    r = np.where(temp[:, int(cln[0] + abs(cln[0] - cln[1]) / 2)] > 0)[0]

    return offset_cm * d, r[-1] - r[0], offset_cm, (r[-1] - r[0]) / d, r[0]


def compute_coordinate_grid(offset_cm, r_cm, d, temp, offset_px, first, alpha_deg, res):
    """
    Computes the coordinate grid for the ultrasound image transformation.

    Args:
        offset_cm (float): Offset in centimeters.
        r_cm (float): Range in centimeters.
        d (float): Pixel-to-centimeter ratio.
        temp (np.ndarray): Processed grayscale image.
        offset_px (float): Offset in pixels.
        first (int): Index of the first pixel row used.
        alpha_deg (float): Half angle of ultrasound beam in degrees.
        res (float): Image resolution scaling factor.

    Returns:
        Tuple[np.ndarray, np.ndarray]: 
            - X coordinates in the transformed space.
            - Y coordinates in the transformed space.
    """

    rows = np.arange(int(offset_cm*res), int(offset_cm*res + r_cm*res))[:, None]
    cols = np.linspace(-alpha_deg, alpha_deg, len(rows))
    Th = cols * m.pi / 180
    X, Y = np.sin(Th) * rows, np.cos(Th) * rows

    return X / res * d + temp.shape[1]/2, Y / res * d - (offset_px - first)



def interpolate_image(X, Y, temp):
    """
    Applies bilinear interpolation to map intensity values from input coordinates.

    Args:
        X (np.ndarray): X coordinate grid.
        Y (np.ndarray): Y coordinate grid.
        temp (np.ndarray): Processed grayscale image.

    Returns:
        np.ndarray: Interpolated intensity values.
    """

    X = np.clip(X, 0, temp.shape[0]-2)
    Y = np.clip(Y, 0, temp.shape[1]-2)

    Xl = np.floor(X).astype(int)
    Xr = Xl + 1
    Yt = np.floor(Y).astype(int)
    Yb = Yt + 1

    dx = X - Xl
    dy = Y - Yt

    intensity = (
        (1 - dx) * (1 - dy) * temp[Yt, Xl] +
        (dx * (1 - dy)) * temp[Yt, Xr] +
        (1 - dx) * dy * temp[Yb, Xl] +
        (dx * dy) * temp[Yb, Xr]
    )

    return np.clip(intensity, 0, 255)


def transform_image(img: 'PIL.Image.Image', alpha_deg: float, res: float):    
    """
    Transforms an ultrasound image into a rectified coordinate system.

    Args:
        img (PIL.Image.Image): Input image to process.
        alpha_deg (float): Half angle of the ultrasound beam in degrees.
        res (float): Image resolution scaling factor.

    Returns:
        Tuple[np.ndarray, float, float]: 
            - Transformed image as a 2D array.
            - Depth of the ultrasound window in pixels.
            - Offset from the top in centimeters.
    """
        
    gray = convert_to_grayscale(img)
    d, rows, cols = detect_cm_marks(gray)
    alpha = alpha_deg/180*m.pi
    temp, gray_idx = clean_image(gray)
    offset_px, r_px, offset_cm, r_cm, first = calculate_geometry(temp, d, alpha)

    X, Y = compute_coordinate_grid(offset_cm, r_cm, d, temp, offset_px, first, alpha_deg, res)
    intensity = interpolate_image(X, Y, temp)

    depth = r_px / d

    return intensity, depth, offset_cm














if __name__ == "__main__":
    pass



