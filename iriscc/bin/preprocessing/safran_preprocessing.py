import sys
sys.path.append('.')

import xarray as xr
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from iriscc.settings import SAFRAN_RAW_DIR

def plot_map(lon_cible,
             lat_cible,
             var,
             title,
             save_dir):
    plt.figure(figsize=(8, 5))
    map = Basemap(
                llcrnrlon=lon_cible.min(), 
                llcrnrlat=lat_cible.min(), 
                urcrnrlon=lon_cible.max(), 
                urcrnrlat=lat_cible.max(),
                resolution='h')
    map.drawcoastlines()
    map.drawcountries()
    lon_grid, lat_grid = np.meshgrid(lon_cible, lat_cible)

    contourf = map.contourf(lon_grid, lat_grid, var, 10, cmap = 'viridis')
    cbar = plt.colorbar(contourf, label = '°C', fraction = 0.06)
    cbar.ax.tick_params(labelsize=12)

    plt.title(title, fontsize =16)
    plt.xticks(np.linspace(lon_cible.min(), lon_cible.max(), 5), fontsize=12) 
    plt.yticks(np.linspace(lat_cible.min(), lat_cible.max(), 5), fontsize=12)
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel("Latitude", fontsize=12)
    plt.tight_layout()
    plt.savefig(save_dir)

if __name__=='__main__':


    file = xr.open_dataset(SAFRAN_RAW_DIR / 'SAFRAN_2020080107_2021080106.nc')
    lat = file['LAT'].values
    lon = file['LON'].values
    Tair = file['Tair'].values[0] - 273.15 # first hour

    lat_min, lat_max = lat.min(), lat.max()
    lon_min, lon_max = lon.min(), lon.max()

    lat_cible = np.arange(lat_min, lat_max, 0.072)
    lon_cible = np.arange(lon_min, lon_max, 0.072)

    lon_grid, lat_grid = np.meshgrid(lon_cible, lat_cible)
    grid_points = np.column_stack((lon_grid.ravel(), lat_grid.ravel()))

    # Construire un arbre pour les données existantes
    data_points = np.column_stack((lon, lat))
    tree = cKDTree(data_points)

    # Trouver les plus proches voisins pour chaque point de la grille cible
    distances, indices = tree.query(grid_points)

    # Initialisation de la grille cible avec -1
    Tair_cible = -1 * np.ones(len(grid_points))

    # Copier les températures des points proches dans la grille cible
    Tair_cible = Tair[indices]
    Tair_cible[distances > 0.072 * 1.5] = -1  # Mettre -1 pour les points trop éloignés

    # Reshape la grille pour correspondre à (lat_cible, lon_cible)
    Tair_cible = Tair_cible.reshape(len(lat_cible), len(lon_cible))


    print(np.shape(Tair_cible))
    print(np.shape(lat_grid))
    print(np.shape(lon_grid))

    plot_map(lon_cible,
             lat_cible,
             Tair_cible,
             f'Temperature SAFRAN {file.time.values[0]}',
             'test.png')


