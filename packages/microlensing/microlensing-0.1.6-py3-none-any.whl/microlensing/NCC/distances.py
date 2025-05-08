import numpy as np
from scipy.ndimage import distance_transform_edt, rotate

from .ncc import NCC


def expanding_source(ncc: NCC):
    '''
    :param ncc: formally, an NCC instance that has ran and has a number of
                caustic crossings map. In general, any object that has
                attributes num_caustic_crossings, center, half_length,
                num_pixels, and pixel_scales, in (y1,y2) coordinates
    '''
    # pixels must be square for distance calculations
    assert ncc.pixel_scales[0] == ncc.pixel_scales[1]

    d_caustic = np.zeros(ncc.num_caustic_crossings.shape)

    for i in range(np.min(ncc.num_caustic_crossings), 
                   np.max(ncc.num_caustic_crossings) + 1):
        mask = (ncc.num_caustic_crossings==i)
        distances = distance_transform_edt(mask)
        d_caustic[mask] = distances[mask]
    d_caustic = d_caustic * ncc.pixel_scales[0]

    return d_caustic

def moving_source(ncc: NCC, angle: float = 90):
    '''
    :param ncc: formally, an NCC instance that has ran and has a number of
                caustic crossings map. In general, any object that has
                attributes num_caustic_crossings, center, half_length,
                num_pixels, and pixel_scales, in (y1,y2) coordinates
    :param angle: angle the source travels at with respect to the y1 axis
    '''
    # pixels must be square for distance calculations
    assert ncc.pixel_scales[0] == ncc.pixel_scales[1]

    def closest_distance_per_row(a):
        '''
        calculate the distance to the nearest different valued pixel, 
        traveling left along the row. borders count as different pixel values.
        we note that distances have a minimum of 0.5, as the center of a pixel
        is at least 0.5 from its border. for example,
        [1,2,2,1,1,2,2,2] returns [0.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 2.5]
        '''
        distances = np.ones(a.shape, dtype=int)
        mask = (a[:, 1:] != a[:, :-1])
        mask = np.insert(mask, 0, True, axis=1)
        for i, _ in enumerate(a):
            idx = np.flatnonzero(mask[i])
            if idx.size > 0:
                distances[i, idx[1:]] = idx[:-1] - idx[1:] + 1

        return distances.cumsum(1) - 0.5

    # add 180 to angle since we calculate distances left along a row, 
    # but an angle of 0 is to the right
    # negate the angle, as array is rotated opposite relative to direction of travel
    d_caustic = closest_distance_per_row(rotate(ncc.num_caustic_crossings, 
                                                -(angle + 180), reshape=True, order=0))
    d_caustic = rotate(d_caustic, angle + 180, reshape=True, order=0)
    d_caustic = d_caustic * ncc.pixel_scales[0] # scale pixel distances to physical

    # remove borders from rotations
    dy1 = (d_caustic.shape[1] - ncc.num_pixels_y1) // 2
    dy2 = (d_caustic.shape[0] - ncc.num_pixels_y2) // 2
    d_caustic = d_caustic[dy2:dy2 + ncc.num_pixels_y2,
                          dy1:dy1 + ncc.num_pixels_y1]

    return d_caustic
