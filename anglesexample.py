def haurwitz(zenith):
    """
    Clear sky GHI predicted by the Haurwitz model.

    The Haurwitz model GHI uses only the zenith angle to determine the clear
    sky GHI, but performs reasonably well (i.e. not as good as Ineichen, but
    better than other zenith-only clear sky models).

    Parameters
    ----------
    zenith : array
        Solar zenith angle in degrees.

    Returns
    -------
    clearsky_ghi : array
        Clear sky GHI in W/m^2.

    """

    # GHI = 1098 * cos(z) * exp(-0.057 / cos(z))
    clearsky_ghi = 1098.0 * np.cos(np.radians(zenith)) * np.exp(-0.057 / np.cos(np.radians(zenith)))

    # remove negative values
    clearsky_ghi[clearsky_ghi < 0] = 0

    return clearsky_ghi

print("""Clear sky GHI predicted by the Haurwitz model.

    The Haurwitz model GHI uses only the zenith angle to determine the clear
    sky GHI, but performs reasonably well (i.e. not as good as Ineichen, but
    better than other zenith-only clear sky models).

    Parameters
    ----------
    zenith : array
        Solar zenith angle in degrees.

    Returns
    -------
    clearsky_ghi : array
        Clear sky GHI in W/m^2.""")