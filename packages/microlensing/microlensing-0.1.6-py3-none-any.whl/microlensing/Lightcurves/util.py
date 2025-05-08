import numpy as np
from scipy.interpolate import RegularGridInterpolator

from microlensing.IPM.ipm import IPM


def pixel_to_point(pixel, center, half_length, num_pixels):
    '''
    convert a pixel coordinate into a point in the source plane
    parameters may be 1D or 2D values

    :param pixel: pixel coordinate or array of pixel coordinates
    :param center: center of the magnification map
    :param half_length: half_length of the magnification map
    :param num_pixels: number of pixels of the magnification map along the axes
    '''
    if not isinstance(pixel, np.ndarray):
        pixel = np.array(pixel)
    return pixel * 2 * half_length / num_pixels - half_length + center

def get_borders(ipm: IPM, kernel):
    '''
    return the inner border of the magnification map after removing a
    region the size of the provided kernel around the edge

    :param ipm: formally, an IPM instance that has ran and has a magnification
                map. in general, any object that has attributes magnifications,
                center, half_length, num_pixels, and pixel_scales, in (y1,y2) coordinates
    :param kernel: kernel of the source profile    
    :return: (y1_min, y1_max), (y2_min, y2_max)
    '''
    # borders of the valid region in pixel coordinates
    x = (np.shape(kernel)[1] / 2, ipm.num_pixels[0] - np.shape(kernel)[1] / 2)
    y = (np.shape(kernel)[0] / 2, ipm.num_pixels[1] - np.shape(kernel)[0] / 2)

    return pixel_to_point(np.transpose([x, y]), ipm.center, 
                          ipm.half_length, ipm.num_pixels).T

def random_position(ipm: IPM, kernel, num: int = 1):
    '''
    return a number of random valid positions in the magnification map

    :param ipm: formally, an IPM instance that has ran and has a magnification
                map. in general, any object that has attributes magnifications,
                center, half_length, num_pixels, and pixel_scales, in (y1,y2) coordinates
    :param kernel: kernel of the source profile
    :param num: number of random positions to return
    '''
    # borders of the valid region
    xlim, ylim = get_borders(ipm, kernel)

    rng = np.random.default_rng()
    x, y = rng.uniform(*xlim, num), rng.uniform(*ylim, num)

    return np.squeeze(np.transpose([x, y])) # to remove unnecessary dimensions if num=1

def valid_positions(positions, ipm: IPM, kernel):
    '''
    determine whether positions within the magnification map are valid
    to avoid edge effects for the given kernel

    :param positions: positions to check
    :param ipm: formally, an IPM instance that has ran and has a magnification
                map. in general, any object that has attributes magnifications,
                center, half_length, num_pixels, and pixel_scales, in (y1,y2) coordinates
    :param kernel: kernel of the source profile
    '''
    if np.ndim(kernel) != 2:
        raise ValueError("kernel must be a 2D array")
    
    if positions.shape[-1] != 2:
        raise ValueError("There are not 2 coordinates per position")
    
    # borders of the valid region
    xlim, ylim = get_borders(ipm, kernel)
    x, y = positions[...,0], positions[...,1]

    return (np.all(x > xlim[0]) and np.all(x < xlim[1])
            and np.all(y > ylim[0]) and np.all(y < ylim[1]))

def interpolated_map(magnifications, center, half_length, num_pixels):
    '''
    :param magnifications: magnification map
    :param center: center of the magnification map
    :param half_length: half_length of the magnification map
    :param num_pixels: number of pixels of the magnification map along the axes
    '''
    # add 0.5 to offset to center of pixels for interpolation
    x, y = np.arange(num_pixels[0]) + 0.5, np.arange(num_pixels[1]) + 0.5

    x = pixel_to_point(x, center[0], half_length[0], num_pixels[0])
    y = pixel_to_point(y, center[1], half_length[1], num_pixels[1])

    # reverse magnification map since (0,0) in pixel coordinates for 
    # python arrays is top left corner and we want it to be bottom left
    return RegularGridInterpolator((x,y), magnifications[::-1].T,
                                   bounds_error=False, fill_value=None)
