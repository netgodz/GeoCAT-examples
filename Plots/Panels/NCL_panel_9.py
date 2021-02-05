"""
NCL_panel_9.py
==============
This script illustrates the following concepts:
   - Paneling an XY and polar plot on the same figure
   - Using a blue-white-red color map
   - Using indexed color to set contour fill colors
   - Filling the areas of an XY curve above and below a reference line
   - Drawing a Y reference line in an XY plot
   - Turning off the map lat/lon grid lines
See following URLs to see the reproduced NCL plot & script:
   - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/panel_9.ncl
   - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/panel_9_lg.png
"""

##############################################################################
# Import packages:
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
import geocat.viz.util as gvutil
from geocat.viz import cmaps as gvcmaps

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/nao.obs.nc"),
                     decode_times=False) 
deppat = ds.nao_djf
xyarr = ds.nao_pc_djf

# Fix the artifact of not-shown-data around -0 and 360 degree longitudes
deppat = gvutil.xr_add_cyclic_longitudes(deppat, 'lon')

###############################################################################
# Plot

# Format axes
fig = plt.figure(figsize=(10, 12))

# Create grid with two rows and one column
# Use `height_ratios` to adjust the relative height of the rows
grid = gridspec.GridSpec(nrows=2, 
                         ncols=1,
                         height_ratios=[0.75, 0.25],
                         figure=fig)

# Specify the projection
proj = ccrs.NorthPolarStereo()

# Add polar plot to figure
ax1 = plt.subplot(grid[0], projection=proj)
ax1.coastlines(linewidths=0.5)
gvutil.set_map_boundary(ax1, [-180, 180], [30, 90], south_pad=1)

# Add XY plot to figure
ax2 = plt.subplot(grid[1])
gvutil.set_axes_limits_and_ticks(ax=ax2,
                                 xlim=(ds.time[0], ds.time[-1]),
                                 ylim=(-4, 3))
gvutil.add_major_minor_ticks(ax=ax2,
                             x_minor_per_major=4,
                             y_minor_per_major=5)
# Plot contours on map
cmap = gvcmaps.BlWhRe  # select colormap
deppat.plot.contourf(ax=ax1,
                     transform=ccrs.PlateCarree(),
                     cmap=cmap,
                     levels=19)

# Add mean temperature over time data to XY plot
ax2.plot(xyarr.time, xyarr, linewidth=1, color='black')

plt.show()
