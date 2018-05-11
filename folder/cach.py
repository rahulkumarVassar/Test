import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from pysheds.grid import Grid
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from PIL import Image

# -------------------------------- #C:/Users/Rahul/Documents/Geany/files/cach2/n30w100_dir/n30w100_dir
# <<< Instatiate a grid from a DEM raster >>> #C:/Users/Rahul/Documents/Geany/files/cach2/n30w100_con_grid/n30w100_con/n30w100_con

grid = Grid.from_raster('C:/Users/Rahul/Documents/Geany/files/Cat_DEM/SRTM_90m_AP_srikakulam_5km.tif', data_name='dem')
fig, ax = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(1)
plt.imshow(grid.dem, extent=grid.extent, cmap='cubehelix', zorder=1)
plt.colorbar(label='Elevation (m)')
plt.grid(zorder=0)
plt.title('Digital elevation map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('C:/Users/Rahul/Documents/Geany/files/cach2/conditioned_dem.png', bbox_inches='tight')
#im1=Image.open('C:/Users/Rahul/Documents/Geany/files/cach2/conditioned_dem.png')
#im1.show()

# -------------------------------- #
# <<< Read a flow direction grid from a raster >>> #

#grid.read_raster('C:/Users/Rahul/Documents/Geany/files/cach2/n30w100_dir/n30w100_dir', data_name='dir')
grid.flowdir(data='dem', out_name='dir',dirmap=(64,  128,  1,   2,    4,   8,    16,  32))
print("\ngrid_dir:\n",grid.dir,"\tgrid_size:",grid.dir.size)

# -------------------------------- #
# <<< Specify flow direction values >>> #

        # N    NE    E    SE    S    SW    W    NW
dirmap = (64,  128,  1,   2,    4,   8,    16,  32)
fig = plt.figure(figsize=(8,6))
fig.patch.set_alpha(1)
plt.imshow(grid.dir, extent=grid.extent, cmap='viridis', zorder=2)
boundaries = ([0] + sorted(list(dirmap)))
plt.colorbar(boundaries = boundaries,values=sorted(dirmap))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Flow direction grid')
plt.grid(zorder=-1)
plt.tight_layout()
plt.savefig('C:/Users/Rahul/Documents/Geany/files/cach2/flow_direction.png', bbox_inches='tight')
#im2=Image.open('C:/Users/Rahul/Documents/Geany/files/cach2/flow_direction.png')
#im2.show()

# -------------------------------- #
# <<< Delineate catchment >>> #

# Specify pour point
#x, y = -97.294167, 32.73750
x, y = 83.712,18.721

# Delineate the catchment
grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',recursionlimit=15000, xytype='label', nodata_out=0)

# Clip the bounding box to the catchment
grid.clip_to('catch')

# Get a view of the catchment
catch = grid.view('catch', nodata=np.nan)

# Plot the catchment
fig, ax = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(1)
plt.grid('on', zorder=0)
im = ax.imshow(catch, extent=grid.extent, zorder=1, cmap='viridis')
plt.colorbar(im, ax=ax, boundaries=boundaries, values=sorted(dirmap), label='Flow Direction')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Delineated Catchment')
plt.savefig('C:/Users/Rahul/Documents/Geany/files/cach2/catchment.png', bbox_inches='tight')
#im3=Image.open('C:/Users/Rahul/Documents/Geany/files/cach2/catchment.png')
#im3.show()

# -------------------------------- #
# <<< Get flow accumulation >>> #

grid.accumulation(data='catch', dirmap=dirmap, out_name='acc')
fig, ax = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(1)
plt.grid('on', zorder=1)
acc_img = np.where(grid.mask, grid.acc + 1, np.nan)
im = ax.imshow(acc_img, extent=grid.extent, zorder=2,cmap='cubehelix',norm=colors.LogNorm(1, grid.acc.max()))
plt.colorbar(im, ax=ax, label='Upstream Cells')
plt.title('Flow Accumulation')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('C:/Users/Rahul/Documents/Geany/files/cach2/flow_accumulation.png', bbox_inches='tight')
#im4=Image.open('C:/Users/Rahul/Documents/Geany/files/cach2/flow_accumulation.png')
#im4.show()

# -------------------------------- #
# <<< Get distances to upstream cells >>> #

grid.flow_distance(data='catch', x=x, y=y, dirmap=dirmap, out_name='dist',xytype='label', nodata_out=np.nan)
fig, ax = plt.subplots(figsize=(8,6))
fig.patch.set_alpha(1)
plt.grid('on', zorder=0)
im = ax.imshow(grid.dist, extent=grid.extent, zorder=2,cmap='cubehelix_r')
plt.colorbar(im, ax=ax, label='Distance to outlet (cells)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Flow Distance')
plt.savefig('C:/Users/Rahul/Documents/Geany/files/cach2/flow_distance.png', bbox_inches='tight')
#im5=Image.open('C:/Users/Rahul/Documents/Geany/files/cach2/flow_distance.png')
#im5.show()


# -------------------------------- #
# <<< Extract river network >>> # 

branch = grid.extract_river_network(fdir='catch', acc='acc',threshold=50, dirmap=dirmap)
#grid.view(branch)


