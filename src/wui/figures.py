"""Publication figures with county-specific display masks and explicit denominators."""
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds, Window
from affine import Affine


def hazard_overview(path, counties, class_counts):
    labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    colors = ['#2c7bb6', '#abd9e9', '#ffffbf', '#fdae61', '#d7191c']
    cmap = ListedColormap(colors)
    cmap.set_bad((1, 1, 1, 0))
    norm = BoundaryNorm(np.arange(0.5, 6), 5)
    fig = plt.figure(figsize=(12, 8), layout='constrained')
    grid = fig.add_gridspec(2, 3, height_ratios=[1.6, 1])
    with rasterio.open(path) as src:
        counties = counties.to_crs(src.crs)
        for column, name in enumerate(['Salt Lake', 'Utah', 'Washington']):
            county = counties[counties['NAME'].str.replace(' County', '', regex=False).str.lower() == name.lower()]
            if len(county) != 1:
                raise ValueError(f'Expected one county polygon for {name}.')
            bounds = county.total_bounds
            window = from_bounds(*bounds, transform=src.transform)
            window = window.intersection(Window(0, 0, src.width, src.height))
            scale = min(1.0, 650 / max(window.width, window.height))
            height, width = max(1,round(window.height*scale)), max(1,round(window.width*scale))
            preview = src.read(1, window=window, out_shape=(height,width),
                               masked=True, resampling=Resampling.nearest)
            transform = src.window_transform(window) * Affine.scale(window.width/width, window.height/height)
            inside = geometry_mask(county.geometry, out_shape=preview.shape, transform=transform, invert=True)
            preview = np.ma.array(preview.data, mask=np.ma.getmaskarray(preview) | ~inside)
            left, top = transform * (0,0)
            right, bottom = transform * (width,height)
            ax = fig.add_subplot(grid[0,column])
            county.plot(ax=ax,color='#ededed',edgecolor='none',zorder=0)
            ax.imshow(preview,cmap=cmap,norm=norm,extent=[left,right,bottom,top],interpolation='nearest',zorder=1)
            county.boundary.plot(ax=ax,color='#253746',linewidth=0.6,zorder=2)
            ax.set_title(name+' County',fontsize=12)
            ax.set_axis_off()
        area_per_cell = abs(src.transform.a * src.transform.e) / 1e6
    ax = fig.add_subplot(grid[1,:])
    bars = ax.bar(labels, np.asarray(class_counts)*area_per_cell, color=colors, edgecolor='#253746')
    ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)
    ax.set_ylim(0, max(np.asarray(class_counts)*area_per_cell)*1.18)
    ax.set_ylabel('Modeled burnable area (km²)')
    ax.set_title('Study-wide class areas; fixed score intervals',fontsize=11)
    ax.legend(handles=[Patch(facecolor='#ededed',label='Excluded or missing data in county panels')],
              loc='upper right',fontsize=8)
    fig.suptitle('Relative wildfire hazard\nCounty panels use individual extents; map scales differ',fontsize=14)
    return fig
