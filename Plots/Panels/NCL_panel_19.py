"""
NCL_panel_19.py
===============
This script illustrates the following concepts:
   - Paneling four subplots in a two by two grid using `gridspec`
   - Adjusting the positioning of the subplots using `hpace` and `wspace`
   - Using a blue-white-red color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/dev_1.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/dev_1_lg.png
"""

##############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil

##############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/sst8292a.nc"))

dates = [198212, 199008, 198705, 198411]

##############################################################################
# Helper function to create and format subplots

def add_axes(fig, grid_space):
    ax = fig.add_subplot(grid_space, projection=ccrs.PlateCarree(central_longitude=-160))
    ax.set_extent([100, 300, -60, 60], crs=ccrs.PlateCarree())

    # Usa geocat.viz.util convenience function to set axes parameters
    gvutil.set_axes_limits_and_ticks(ax,
                                     ylim=(-60, 60),
                                     xticks=np.arange(-80, 120, 30),
                                     yticks=np.arange(-60, 61, 30))

    # Use geocat.viz.util convenience function to make plots look like NCL
    # plots by using latitude, longitude tick labels
    gvutil.add_lat_lon_ticklabels(ax)
    # Remove the degree symbol from tick labels
    ax.yaxis.set_major_formatter(LatitudeFormatter(degree_symbol=''))
    ax.xaxis.set_major_formatter(LongitudeFormatter(degree_symbol=''))

    # Use geocat.viz.util convenience function to add minor and major tick lines
    gvutil.add_major_minor_ticks(ax, labelsize=8)

    # Make sure that tick marks are only on the left and bottom sides of figure
    ax.tick_params('both', which='both', top=False, right=False)

    ax.coastlines(linewidths=0.5)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    return ax

##############################################################################
# Plot with default spacing:

fig = plt.figure(figsize=(10,8))

# Create gridspec to hold four subplots
grid = fig.add_gridspec(ncols=2, nrows=2)

# Add the axes
ax1 = add_axes(fig, grid[0, 0])
ax2 = add_axes(fig, grid[0, 1])
ax3 = add_axes(fig, grid[1, 0])
ax4 = add_axes(fig, grid[1, 1])
plt.show()


