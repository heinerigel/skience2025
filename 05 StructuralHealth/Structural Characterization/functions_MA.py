import numpy
def roof_edges2D(mult = 1, Lat = 0, Lon = 0):
    offsetLon = 681437.8 -Lon
    offsetLat = 248919.2 -Lat

    NLon = (681443.103 - offsetLon)*mult
    NLat = (248954.576 - offsetLat)*mult
    ELon = (681462.783 - offsetLon)*mult
    ELat = (248942.503 - offsetLat)*mult
    E_1 = (681429.922 - offsetLon)*mult
    N_1 = (248934.161 - offsetLat)*mult
    E_2 = (681431.376 - offsetLon)*mult
    N_2 = (248912.610 - offsetLat)*mult
    WLon = (681426.233 - offsetLon)*mult
    WLat = (248895.830 - offsetLat)*mult
    SLon = (681447.497 - offsetLon)*mult
    SLat = (248889.417 - offsetLat)*mult
    E_5 = (681460.536 - offsetLon)*mult
    N_5 = (248909.601 - offsetLat)*mult
    E_6 = (681459.040 - offsetLon)*mult
    N_6 = (248927.087 - offsetLat)*mult
    edges = numpy.array([[NLon, NLat],[E_1,N_1],[E_2,N_2],[WLon,WLat],[SLon,SLat],[E_5,N_5],[E_6,N_6],[ELon,ELat]])
    return edges

def roof_edges3D(mult=1, Lon=0, Lat=0, up=0):
    offsetLon = 681437.8 - Lon
    offsetLat = 248919.2 - Lat

    NLon = (681443.103 - offsetLon) * mult
    NLat = (248954.576 - offsetLat) * mult
    ELon = (681462.783 - offsetLon) * mult
    ELat = (248942.503 - offsetLat) * mult
    E_1 = (681429.922 - offsetLon) * mult
    N_1 = (248934.161 - offsetLat) * mult
    E_2 = (681431.376 - offsetLon) * mult
    N_2 = (248912.610 - offsetLat) * mult
    WLon = (681426.233 - offsetLon) * mult
    WLat = (248895.830 - offsetLat) * mult
    SLon = (681447.497 - offsetLon) * mult
    SLat = (248889.417 - offsetLat) * mult
    E_5 = (681460.536 - offsetLon) * mult
    N_5 = (248909.601 - offsetLat) * mult
    E_6 = (681459.040 - offsetLon) * mult
    N_6 = (248927.087 - offsetLat) * mult

    Lon1 = 681437.8 - offsetLon  # check again from registration!!
    Lat1 = 248919.2 - offsetLat

    ER = (124.37) * mult + up
    E23 = (78.7 - 0.32) * mult
    E6 = (21.78 - 0.32) * mult
    E0 = (0) * mult
    BE0 = (0) * mult
    edges_gfloor = [list(zip([NLon, E_1, E_2, WLon, SLon, E_5, E_6, ELon], [NLat, N_1, N_2, WLat, SLat, N_5, N_6, ELat],
                             [0, 0, 0, 0, 0, 0, 0, 0], ))]
    edges_roof = [list(zip([NLon, E_1, E_2, WLon, SLon, E_5, E_6, ELon], [NLat, N_1, N_2, WLat, SLat, N_5, N_6, ELat],
                           [ER, ER, ER, ER, ER, ER, ER, ER], ))]
    return edges_gfloor, edges_roof, ER, E23, E6, E0, BE0, ELon, ELat, Lon1, Lat1

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''
    import numpy as np
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5 * max([x_range, y_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])

def H_array2D(mult=1, Lat=0, Lon=0):
    offsetLon = 681437.8 - Lon
    offsetLat = 248919.2 - Lat

    NLon = (681443.103 - offsetLon) * mult
    NLat = (248954.576 - offsetLat) * mult
    ELon = (681462.783 - offsetLon) * mult
    ELat = (248942.503 - offsetLat) * mult
    WLon = (681426.233 - offsetLon) * mult
    WLat = (248895.830 - offsetLat) * mult
    SLon = (681447.497 - offsetLon) * mult
    SLat = (248889.417 - offsetLat) * mult
    Lon1 = 0 * mult
    Lat1 = 0 * mult
    edges = numpy.array([[Lon1, Lat1], [NLon, NLat], [ELon, ELat], [SLon, SLat], [WLon, WLat]])
    return edges