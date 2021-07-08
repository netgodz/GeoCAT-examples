"""
NCL_lb_5.py
===========
This script illustrates the following concepts:
   - Customizing a labelbar for a contour plot
   - Turning off the perimeter around a labelbar
   - Making the labelbar be horizontal
   - Setting the fontsize of labelbar labels
   - Changing the levels of the labelbar labels
   - Changing the width and height of a labelbar
   - Changing the width and height of a plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/lb_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/lb_5_lg.png
"""

###############################################################################
# Import packages:

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import util as gvutil

###############################################################################
# Read in data:

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/cone.nc"))
u = ds.u.isel(time=4)

###############################################################################
# Plot:

# Generate figure (set its size (width, height) in inches)
plt.figure(figsize=(10, 8))

# Generate with Cartopy projection
ax = plt.axes(projection=ccrs.PlateCarree())

# Set contour levels
levels = np.arange(0, 11, 1)

# Plot contour lines
lines = u.plot.contour(ax=ax, levels=levels, linewidths=0.5, add_labels=False)

# Draw contour labels and use Matplotlib FancyBboxPatch object to set bounding boxes for the labels
# Use clabel to set labelbar label fontsize
# Use FancyBboxPatch object by calling set_bbox to customize aspect ratio, background color and padding of label bounding boxes
ax.clabel(lines, np.array([0]), colors='black', fmt="%.0f", fontsize=18)
[
    txt.set_bbox(
        dict(mutation_aspect=0.8, facecolor='white', edgecolor='none', pad=2))
    for txt in lines.labelTexts
]

# Plot filled contour
colors = u.plot.contourf(ax=ax,
                         cmap='viridis_r',
                         levels=levels,
                         transform=ccrs.PlateCarree(),
                         add_colorbar=False,
                         add_labels=False)

# Add colorbar
cbar = plt.colorbar(colors,
                    ax=ax,
                    orientation='horizontal',
                    shrink=0.65,
                    pad=0.13,
                    extendrect=True,
                    extendfrac='auto',
                    aspect=11,
                    drawedges=True,
                    ticks=levels[:-1:2])

# Set colorbar label size
cbar.ax.xaxis.set_tick_params(length=0, labelsize=24, pad=12)

# Use geocat.viz.util convenience function to set axes limits & tick values without calling several matplotlib functions
gvutil.set_axes_limits_and_ticks(ax,
                                 xlim=(0, 49),
                                 ylim=(0, 29),
                                 xticks=np.linspace(0, 40, 5),
                                 yticks=np.linspace(0, 25, 6))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=5, y_minor_per_major=5)

# Use geocat.viz.util convenience function to add titles to left and right of the plot axis.
gvutil.set_titles_and_labels(ax,
                             maintitle='Cone amplitude',
                             maintitlefontsize=32)

# Set both major and minor ticks to point inwards
ax.tick_params(which='both', direction='in')

# Set different tick font sizes and padding for X and Y axis
ax.tick_params(axis='x', labelsize=24, pad=18)
ax.tick_params(axis='y', labelsize=16, pad=12)

# Set major and minor tick length
ax.tick_params(which='major', length=16)
ax.tick_params(which='minor', length=10)

# Show plot
plt.tight_layout()
plt.show()
