"""
Clear sky models huh

"""

import pandas as pd
import numpy as np

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


def solar_angles(df, lat, lon, alt=0):
    """
    Calculate solar angles (zenith, elevation, azimuthal) for a specified
    location and time.

    Parameter
    ---------
    df : pandas.DataFrame
        A DataFrame object from the pandas package, where the DataFrame.index
        are timestamps. Two-dimensional size-mutable, potentially heterogeneous tabular data structure with labeled axes
    lat : float
        Latitude [degrees].
    lon : float
        Longitude [degrees].
    alt : float
        Altitude above sea level [km].

    Returns
    -------
    angles : (n, 3) array
        Zenith, elevation, and azimuthal angles [degrees] for n timestamps.

    """

    ##I = df.year
    ##J = df.month
    ##K = df.day
    ##jd= K-32075+1461*(I+4800+(J-14)/12)/4+367*(J-2-(J-14)/12*12)/12-3*((I+4900+(J-14)/12)/100)/4


    jd = pd.Timestamp(df).to_julian_date()

    # offset (2451543.5)
    d_offset = pd.Timestamp('1999-12-31 00:00:00').to_julian_date()

    d = jd - d_offset


    # Keplerian elements for the sun (geocentric)
    w = 282.9404 + 4.70935E-5 * d                   # longitude of perihelion [degrees]
    a = 1.0                                         # mean distance [AU]
    e = 0.016709 - 1.151E-9 * d                     # eccentricity [-]
    M = np.mod(356.0470 + 0.9856002585 * d, 360.0)  # mean anomaly [degrees]
    L = w + M                                       # Sun's mean longitude [degrees]
    oblecl = 23.4393 - 3.563E-7 * d                 # Sun's obliquity of the eliptic [degrees]

    # Auxiliary angle [degrees]
    E = M + (180.0 / np.pi) * e * np.sin(np.deg2rad(M)) * (1.0 + e * np.cos(np.deg2rad(M)))

    # Rectangular coordinates in the plane of the ecliptic (x-axis toward perihelion)
    x = np.cos(np.deg2rad(E)) - e
    y = np.sin(np.deg2rad(E)) * np.sqrt(1 - (e ** 2))

    # Distance (r) and true anomaly (v)
    r = np.sqrt((x ** 2) + (y ** 2))
    v = np.rad2deg(np.arctan2(y, x))

    # Longitude of the sun
    lon_sun = v + w

    # Ecliptic rectangular coordinates
    xeclip = r * np.cos(np.deg2rad(lon_sun))
    yeclip = r * np.sin(np.deg2rad(lon_sun))
    zeclip = 0.0

    # Rotate coordinates to equatorial rectangular coordinates
    xequat = xeclip
    yequat = yeclip * np.cos(np.deg2rad(oblecl)) + zeclip * np.sin(np.deg2rad(oblecl))
    zequat = yeclip * np.sin(np.deg2rad(23.4406)) + zeclip * np.cos(np.deg2rad(oblecl))

    # Convert equatorial rectangular coordinates to right-ascension (RA) and declination
    r = np.sqrt(xequat ** 2 + yequat ** 2 + zequat ** 2) - (alt / 149598000.0)
    RA = np.rad2deg(np.arctan2(yequat, xequat))
    delta = np.rad2deg(np.arcsin(zequat / r))

    # Calculate local siderial time
    uth = df.hour + (df.minute / 60.0) + (df.second / 3600.0)
    gmst0 = np.mod(L + 180.0, 360.0) / 15.0
    sidtime = gmst0 + uth + (lon / 15.0)

    # Replace RA with hour-angle (HA)
    HA = sidtime * 15.0 - RA

    # Convert to rectangular coordinates
    x = np.cos(np.deg2rad(HA)) * np.cos(np.deg2rad(delta))
    y = np.sin(np.deg2rad(HA)) * np.cos(np.deg2rad(delta))
    z = np.sin(np.deg2rad(delta))

    # Rotate along an axis going East-West
    xhor = x * np.cos(np.deg2rad(90.0 - lat)) - z * np.sin(np.deg2rad(90.0 - lat))
    yhor = y
    zhor = x * np.sin(np.deg2rad(90.0 - lat)) + z * np.cos(np.deg2rad(90.0 - lat))

    # Find azimuthal and elevation angles
    azimuthal = np.rad2deg(np.arctan2(yhor, xhor)) + 180.0
    elevation = np.rad2deg(np.arcsin(zhor))

    zenith = 90.0 - elevation

    return np.column_stack((zenith, elevation, azimuthal))


def zenith_angle(df, lat, lon, alt=0):
    """Solar zenith angle."""
    return solar_angles(df, lat, lon, alt=alt)[:, 0]
    #returns first column of the output array (zenith, elev, azimuthal) as an array of zenith's. 

def elevation_angle(df, lat, lon, alt=0):
    """Solar elevation angle."""
    return solar_angles(df, lat, lon, alt=alt)[:, 1]
    #returns second column of the output array (zenith, elev, azimuthal) as an array of elevations. 

def azimuthal_angle(df, lat, lon, alt=0):
    """Solar azimuthal angle."""
    return solar_angles(df, lat, lon, alt=alt)[:, 2]
    #returns third column of the output array (zenith, elev, azimuthal) as an array of azimuthals. 