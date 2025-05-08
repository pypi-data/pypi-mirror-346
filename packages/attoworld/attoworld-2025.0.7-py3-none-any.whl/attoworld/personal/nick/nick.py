import numpy as np

def fwhm(x: np.ndarray, y: np.ndarray, height: float = 0.5) -> float:
    """
    Gives the full-width at half-maximum of data in a numpy array pair.

    :param x: The x-values (e.g. the scale of the vector; has the same units as the return value)
    :type x: np.ndarray

    :param y: The y-values (to which half-maximum refers)
    :type y: np.ndarray

    :param height: Instead of half-max, can optionally return height*max (e.g. default 0.5)
    :type height: float

    :return: The full-width at half-max (units of x)
    :rtype: float
    """
    heightLevel = np.max(y) * height
    indexMax = np.argmax(y)
    y = np.roll(y, - indexMax + int(np.shape(y)[0]/2),axis=0)
    indexMax = np.argmax(y)
    xLower = np.interp(heightLevel, y[:indexMax], x[:indexMax])
    xUpper = np.interp(heightLevel, np.flip(y[indexMax:]), np.flip(x[indexMax:]))
    return xUpper - xLower
