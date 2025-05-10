import numpy as np
from typing import Tuple



def transform_spherical_to_cartesian(R: np.ndarray, THETA: np.ndarray):
    """
    Converts spherical coordinates (R, THETA) to Cartesian (X, Z).

    Args:
        R (np.ndarray): Radial distances.
        THETA (np.ndarray): Polar angles.

    Returns:
        Tuple[np.ndarray, np.ndarray]: X and Z Cartesian coordinates.
    """
    Z = np.cos(THETA) * R
    X = np.sin(THETA) * R
    return X, Z

def transform_cartesian_to_spherical(X: np.ndarray, Z: np.ndarray):
    """
    Converts Cartesian coordinates (X, Z) to spherical coordinates (R, THETA).

    Args:
        X (np.ndarray): X coordinates.
        Z (np.ndarray): Z coordinates.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Radial distances R and polar angles THETA.
    """
    R = np.sqrt(X**2 + Z**2)
    THETA = np.zeros(R.shape)
    THETA[R > 0] = np.arcsin(X[R > 0] / R[R > 0])
    return R, THETA

def generate_cartesian_volume(depth, thetas, offset, resolution):
    """
    Creates a Cartesian grid and corresponding spherical coordinates within a conic frustum.

    Returns:
        Tuple containing the image shape, filtered R, THETA arrays and valid indices.
    """
    frame_width = 400
    frame_depth = 400
    frame_THETA = np.linspace(thetas[0], thetas[1], frame_width)
    frame_R = np.linspace(offset, depth + offset, frame_depth)

    R, THETA = np.meshgrid(frame_R, frame_THETA, indexing='ij')
    X, Z = transform_spherical_to_cartesian(R, THETA)

    x_min, x_max = np.min(X), np.max(X)
    z_max = np.max(Z)

    x_len = int(np.ceil((x_max - x_min) / resolution + 1))
    z_len = int(np.ceil(z_max / resolution + 1))

    X = np.linspace(x_min, x_max, x_len)
    X = np.tile(X, (z_len, 1)).T
    Z = np.linspace(0, z_max, z_len)
    Z = np.tile(Z, (x_len, 1))

    R, THETA = transform_cartesian_to_spherical(X, Z)
    cone_mask = (THETA < thetas[0]) | (THETA > thetas[1]) | (R > depth + offset)

    return X.shape, R[~cone_mask], THETA[~cone_mask], np.where(~cone_mask)

def find_nearest_indices(image_R, image_THETA, frame_R, frame_THETA):
    """
    Finds the nearest neighbor indices and interpolation weights.
    
    """
    dR = np.mean(np.diff(frame_R))
    dTHETA = np.mean(np.diff(frame_THETA))

    THETA_l_ind = np.clip(np.floor((image_THETA - frame_THETA[0]) / dTHETA).astype(int), 0, len(frame_THETA) - 2)
    THETA_r_ind = THETA_l_ind + 1

    R_l_ind = np.clip(np.floor((image_R - frame_R[0]) / dR).astype(int), 0, len(frame_R) - 2)
    R_r_ind = R_l_ind + 1

    THETA_l_val = frame_THETA[THETA_l_ind]
    THETA_r_val = frame_THETA[THETA_r_ind]
    R_l_val = frame_R[R_l_ind]
    R_r_val = frame_R[R_r_ind]

    left_Theta = image_THETA - THETA_l_val
    right_Theta = THETA_r_val - image_THETA
    R_m = -(2 * image_R * (np.cos(right_Theta) - np.cos(left_Theta))) / \
          (np.power(2 * np.sin((THETA_r_val - THETA_l_val) / 2), 2) * (np.sin(right_Theta) - np.sin(left_Theta)) /
           (np.sin(right_Theta) + np.sin(left_Theta)))
    R_m[np.cos(right_Theta) == np.cos(left_Theta)] = image_R[np.cos(right_Theta) == np.cos(left_Theta)] / np.cos(dTHETA / 2)

    w1 = (R_r_val - R_m) / (R_r_val - R_l_val)
    w2 = 1 - w1
    w3 = np.sin(right_Theta) / (np.sin(right_Theta) + np.sin(left_Theta))
    w4 = 1 - w3

    return THETA_l_ind, THETA_r_ind, R_l_ind, R_r_ind, w1, w2, w3, w4

def bilinear_interpolation(frame: np.ndarray, indices, weights, shape, cone_mask_indices):
    """
    Performs bilinear interpolation on the image.

    Args:
        frame (np.ndarray): The input frame.
        indices (tuple): Index arrays for R and THETA.
        weights (tuple): Weight arrays.
        shape (tuple): Shape of the output image.
        cone_mask_indices (tuple): Indices for valid cone region.

    Returns:
        np.ndarray: Interpolated image.
    """
    THETA_l_ind, THETA_r_ind, R_l_ind, R_r_ind = indices
    w1, w2, w3, w4 = weights

    A = frame[THETA_l_ind, R_l_ind]
    B = frame[THETA_r_ind, R_l_ind]
    C = frame[THETA_r_ind, R_l_ind]
    D = frame[THETA_r_ind, R_r_ind]

    interpolated_frame = np.zeros(shape)
    to_fill = w1 * (w3 * A + w4 * B) + w2 * (w3 * C + w4 * D)
    interpolated_frame[cone_mask_indices] = to_fill
    return interpolated_frame



def transform_back(frame, depth, alpha, offset_frame, offset=0, resolution=0.01):
    """
    Transforms back the masked image to the original coordinate system.
    This is the main function that calls the other functions to perform the interpolation.

    Args:
        frame (np.ndarray): The input frame.
        depth (float): Depth of the frustum.
        thetas (Tuple[float, float]): The range of theta values.
        alpha (float): Half angle of the ultrasound device in radians.
        offset (float): Offset value between the top of the frame and the US source.
        offset_frame (float): Offset value for the frame.
        resolution (float): Resolution value for upscaling or downscaling.

    Returns:
        np.ndarray: Interpolated frame.
    """
    thetas = (-alpha, alpha)

    frame = frame.T
    frame_width, frame_depth = frame.shape

    offset_row = int(frame_depth / depth * offset_frame)
    padded_frame = np.zeros((frame_width, offset_row + frame_depth))
    padded_frame[:, offset_row:] = frame[:, :]

    frame = padded_frame
    frame_depth = frame.shape[1] 

    frame_TETHA = np.linspace(thetas[0], thetas[1], frame_width)
    freame_R = np.linspace(offset, depth + offset, frame_depth)

    shape, image_R, image_THETA, cone_mask_indices = generate_cartesian_volume(depth, thetas, offset, resolution)
    indices_weights = find_nearest_indices(image_R, image_THETA, freame_R, frame_TETHA)
    indices = indices_weights[:4]
    weights = indices_weights[4:]

    interpolated_frame = bilinear_interpolation(frame, indices, weights, shape, cone_mask_indices)

    return interpolated_frame.T

