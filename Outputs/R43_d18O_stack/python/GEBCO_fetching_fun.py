#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:44:37 2020

@author: zhou
"""

import xarray as xr
import numpy as np

def fetch_GEBCO(lon_res, lat_res):
    ds = xr.open_dataset('./GEBCO/GEBCO_2014_6x6min_Global.nc')
    # interpolat (downgrading)
    new_lon = np.linspace(-180, 180, lon_res)  # 900
    new_lat = np.linspace(-90, 90, lat_res)  # 450
    dsi = ds.interp(lat=new_lat, lon=new_lon)
    return dsi

def fetch_MAR_bathymetry():
    """
    return Eastern North Atlantic bathymetry - Denmark Strait side

    Returns
    -------
    heights : numpy.Array
        DESCRIPTION.
    lats : numpy.Array
        DESCRIPTION.

    """
    dsi = fetch_GEBCO(900,450)
    
    # vectorized indexing
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjVuPPYyf3pAhUISTABHWAnCrYQygQwBnoECAcQBw&url=https%3A%2F%2Fncar-hackathons.github.io%2Fscientific-computing%2Fxarray%2F03_label_indexing.html%23vectorized-indexing&usg=AOvVaw0EsAu0_7W70fyE7usVaYHV
    lat_list = [-6.8,3.7,19.9,63.9,76]
    lon_list = [-28.1,-43.6,-54.8,-33.4,-0.2]
    
    lat_list_zip = list(zip(lat_list[:-1], lat_list[1:]))
    lon_list_zip = list(zip(lon_list[:-1], lon_list[1:]))
    
    MAR = []
    
    for lat_pair, lon_pair in zip(lat_list_zip, lon_list_zip):
        ind_x = xr.DataArray(np.arange(lat_pair[0],lat_pair[1],(lat_pair[1]-lat_pair[0])/100), dims='points')
        ind_y = xr.DataArray(np.arange(lon_pair[0], lon_pair[1], (lon_pair[1]-lon_pair[0])/100), dims='points')
        MAR.append(dsi.sel(lat=ind_x,lon=ind_y,method='nearest'))
    
    heights = np.concatenate([dataset['Height'] for dataset in MAR])
    lats = np.concatenate([dataset['lat'] for dataset in MAR])
    return (heights, lats)

def fetch_WNA_bathymetry():
    """
    return Western North Atlantic bathymetry - Labrador Sea side

    Returns
    -------
    heights : numpy.Array
        DESCRIPTION.
    lats : numpy.Array
        DESCRIPTION.

    """
    dsi = fetch_GEBCO(900,450)
    
    # vectorized indexing
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjVuPPYyf3pAhUISTABHWAnCrYQygQwBnoECAcQBw&url=https%3A%2F%2Fncar-hackathons.github.io%2Fscientific-computing%2Fxarray%2F03_label_indexing.html%23vectorized-indexing&usg=AOvVaw0EsAu0_7W70fyE7usVaYHV
    lat_list = [-7.4, 18.6, 47.5, 70]
    lon_list = [-29.3, -54.5, -38, -61.9]
    
    lat_list_zip = list(zip(lat_list[:-1], lat_list[1:]))
    lon_list_zip = list(zip(lon_list[:-1], lon_list[1:]))
    
    MAR = []
    
    for lat_pair, lon_pair in zip(lat_list_zip, lon_list_zip):
        # If lat, lon mismatch error meesage, 
        # Increase (#) in lat_pair[1]-lat_pair[0])/(#)
        ind_x = xr.DataArray(np.arange(lat_pair[0],lat_pair[1],(lat_pair[1]-lat_pair[0])/100), dims='points')
        ind_y = xr.DataArray(np.arange(lon_pair[0], lon_pair[1], (lon_pair[1]-lon_pair[0])/100), dims='points')
        MAR.append(dsi.sel(lat=ind_x,lon=ind_y,method='nearest'))
    
    heights = np.concatenate([dataset['Height'] for dataset in MAR])
    lats = np.concatenate([dataset['lat'] for dataset in MAR])
    return (heights, lats)

def fetch_ENA_bathymetry():
    """
    return Eastern North Atlantic bathymetry - Denmark Strait side

    Returns
    -------
    heights : numpy.Array
        DESCRIPTION.
    lats : numpy.Array
        DESCRIPTION.

    """
    dsi = fetch_GEBCO(900,450)
    
    # vectorized indexing
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjVuPPYyf3pAhUISTABHWAnCrYQygQwBnoECAcQBw&url=https%3A%2F%2Fncar-hackathons.github.io%2Fscientific-computing%2Fxarray%2F03_label_indexing.html%23vectorized-indexing&usg=AOvVaw0EsAu0_7W70fyE7usVaYHV
    lat_list = [-5.3, 18.6, 44.7, 56.8, 70]
    lon_list = [-3.3, -28.7, -17.5, -24, -1]
    
    lat_list_zip = list(zip(lat_list[:-1], lat_list[1:]))
    lon_list_zip = list(zip(lon_list[:-1], lon_list[1:]))
    
    MAR = []
    
    for lat_pair, lon_pair in zip(lat_list_zip, lon_list_zip):
        # If lat, lon mismatch error meesage, 
        # Increase (#) in lat_pair[1]-lat_pair[0])/(#)
        ind_x = xr.DataArray(np.arange(lat_pair[0],lat_pair[1],(lat_pair[1]-lat_pair[0])/100), dims='points')
        ind_y = xr.DataArray(np.arange(lon_pair[0], lon_pair[1], (lon_pair[1]-lon_pair[0])/100), dims='points')
        MAR.append(dsi.sel(lat=ind_x,lon=ind_y,method='nearest'))
    
    heights = np.concatenate([dataset['Height'] for dataset in MAR])
    lats = np.concatenate([dataset['lat'] for dataset in MAR])
    return (heights, lats)