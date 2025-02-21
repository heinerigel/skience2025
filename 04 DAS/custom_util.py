import numpy as np
import xdas as xd

def apply_scaling(da):
    da = da * 116.0 / 8192.0 * 400.0 / 10.0 * 1e-9
    return da

def apply_mapping(da, segments_filename="good_segments.txt"):

    tmp = np.loadtxt("good_segments.txt")
    segment = {}
    segment['x1'] = tmp[:,0]
    segment['y1'] = tmp[:,1]
    segment['d1'] = tmp[:,2]
    segment['x2'] = tmp[:,3]
    segment['y2'] = tmp[:,4]
    segment['d2'] = tmp[:,5]


    #-- Each channel is associated with a distance along the fiber (based on metadata like channel spacing)
    channels_dd_original = da.coords['distance'].values

    icount = 0
    tie_indices = []
    tie_distances = []
    tie_lat = []
    tie_lon = []
    mapped_ranges = []

    #-- Now we loop through each segment, find the channel nearest to the reported start and end, and interpolate
    for i in range(len(segment['x1'])):
        i1 = np.argmin(np.abs(channels_dd_original - segment['d1'][i]))
        i2 = np.argmin(np.abs(channels_dd_original - segment['d2'][i]))
        nchan = i2-i1
        
        #-- Each start of a segment is a "tie", where the distance, lat, lon are locked in.
        tie_indices.append(icount)
        tie_distances.append(segment['d1'][i])
        tie_lat.append(segment['y1'][i])
        tie_lon.append(segment['x1'][i])
        icount += nchan

        #-- If there is a gap, we need to lock in the end of that segment as a new tie-point:
        if(i<len(segment['x1'])-1):
            if(segment['d2'][i] != segment['d1'][i+1]):
                tie_indices.append(icount)
                icount += 1
                tie_distances.append(segment['d2'][i])
                tie_lat.append(segment['y2'][i])
                tie_lon.append(segment['x2'][i])
        #-- At the very end, again need to lock in the end of that segment
        else:
            tie_indices.append(icount)
            tie_distances.append(segment['d2'][i])
            tie_lat.append(segment['y2'][i])
            tie_lon.append(segment['x2'][i])
        mapped_ranges.append([i1,i2])

    #-- Now for each segment we need to extract and collect all the actual DAS data in "da"
    for i in range(len(mapped_ranges)):

        #-- Figure out the indices. If there's a gap, we need to catch the final trace up to it.
        i0 = mapped_ranges[i][0]
        i1 = mapped_ranges[i][1]
        if(i<len(mapped_ranges)-1):
            if(mapped_ranges[i][1]!=mapped_ranges[i+1][0]):
                i1 += 1
        else:
            i1 += 1
        
        #-- Actually collect the da from each chunk
        if(i==0):
            da2 = da[:, i0:i1]
        else:
            da2 = xd.concatenate([da2, da[:, i0:i1]],dim = "distance")

    #-- Make new Coordinate containers for our distances, lat, lon
    distance_mapped = xd.Coordinate(
        {
            "tie_indices": tie_indices,
            "tie_values": tie_distances
        }
    )
    lat_mapped = xd.Coordinate(
        {
            "tie_indices": tie_indices,
            "tie_values": tie_lat
        }
    )
    lon_mapped = xd.Coordinate(
        {
            "tie_indices": tie_indices,
            "tie_values": tie_lon
        }
    )

    #-- Attach those coordinates to our data
    da2 = da2.assign_coords(distance=distance_mapped)
    da2 = da2.assign_coords(latitude=("distance", lat_mapped))
    da2 = da2.assign_coords(longitude=("distance", lon_mapped))
    return da2