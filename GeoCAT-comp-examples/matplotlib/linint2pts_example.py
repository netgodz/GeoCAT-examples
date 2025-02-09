"""
linint2pts_example.py
=====================

This script illustrates the following concepts:
   - Usage of geocat-comp's `linint2pts` function
   - Bilinear interpolation from a rectilinear grid to an unstructured grid or locations
   - Usage of geocat-datafiles for accessing NetCDF files
   - Usage of geocat-viz plotting convenience functions

See following GitHub repositories to see further information about the function and to access data:
    - For `linint2pts` function: https://github.com/NCAR/geocat-comp
    - For "sst.nc" data file: https://github.com/NCAR/geocat-datafiles/tree/main/netcdf_files

Dependencies:
    - geocat.comp
    - geocat.datafiles (Not necessary but for conveniently accessing the NetCDF data file)
    - geocat.viz (Not necessary but for plotting convenience)
    - numpy
    - xarray
    - cartopy
    - matplotlib
    - mpl_toolkits
"""

###############################################################################
# Import packages:

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid

import geocat.viz.util as gvutil
import geocat.datafiles as gdf
from geocat.comp import linint2pts

###############################################################################
# Read in data:

# Open a netCDF data file (Sea surface temperature) using xarray default
# engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/sst.nc'))

sst = ds.TEMP[0, 0, :, :].chunk()
lat = ds.LAT[:]
lon = ds.LON[:]

###############################################################################
# GeoCAT-comp function call:

# Provide (output) interpolation locations. This script uses 3000 arbitrary
# locations world-wide in order to demonstrate an extensive comparison of the
# linint2pts outputs to the original grid throughout the globe. The function
# can even be used for a single location though.
newlat = np.random.uniform(low=min(lat), high=max(lat), size=(3000,))
newlon = np.random.uniform(low=min(lon), high=max(lon), size=(3000,))

# Call `linint2pts` from `geocat-comp`
newsst = linint2pts(sst, newlon, newlat, False)

###############################################################################
# Plot:

# Generate figure and set its size (width, height) in inches
fig = plt.figure(figsize=(10, 8))

# Generate Axes grid using a Cartopy projection
projection = ccrs.PlateCarree()
axes_class = (GeoAxes, dict(map_projection=projection))
axgr = AxesGrid(fig,
                111,
                axes_class=axes_class,
                nrows_ncols=(2, 1),
                axes_pad=0.7,
                cbar_location='right',
                cbar_mode='single',
                cbar_pad=0.5,
                cbar_size='3%',
                label_mode='')

# Create a dictionary for common plotting options for both subplots
common_options = dict(vmin=-30, vmax=30, cmap=cm.jet)

# Plot original grid and linint2pts interpolations as two subplots
# within the figure
for i, ax in enumerate(axgr):

    # Plot original grid and linint2pts interpolations within the subplots
    if (i == 0):
        p = sst.plot.contourf(ax=ax,
                              **common_options,
                              transform=projection,
                              levels=16,
                              extend='neither',
                              add_colorbar=False,
                              add_labels=False)
        ax.set_title('Sea Surface Temperature - Original Grid',
                     fontsize=14,
                     fontweight='bold',
                     y=1.04)
    else:
        ax.scatter(newlon, newlat, c=newsst, **common_options, s=25)
        ax.set_title(
            'linint2pts - Bilinear interpolation for 3000 random locations',
            fontsize=14,
            fontweight='bold',
            y=1.04)

    # Add coastlines to the subplots
    ax.coastlines()

    # Use geocat.viz.util convenience function to add minor and major tick
    # lines
    gvutil.add_major_minor_ticks(ax)

    # Use geocat.viz.util convenience function to set axes limits & tick
    # values without calling several matplotlib functions
    gvutil.set_axes_limits_and_ticks(ax,
                                     ylim=(-60, 60),
                                     xticks=np.linspace(-180, 180, 13),
                                     yticks=np.linspace(-60, 60, 5))

    # Use geocat.viz.util convenience function to make plots look like NCL
    # plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax, zero_direction_label=False)

# Add color bar and label details (title, size, etc.)
cax = axgr.cbar_axes[0]
cax.colorbar(p)
axis = cax.axis[cax.orientation]
axis.label.set_text(r'Temperature ($^{\circ} C$)')
axis.label.set_size(16)
axis.major_ticklabels.set_size(10)

plt.show()
