#Functions to work with Spectral Energy Distribution arrays
#==========================================================

import numpy as np

from ..LazaUtils.get import get_index


#==========================================================
def change_units(sed,wl_unit,f_unit):
    """
    ---------------------------------------------
    INSTRUCTIONS
    Converts AA-ergscma seds into whatever unit you want, for each axis
    ---------------------------------------------
    ARGS:
    sed: Nx2 or Nx3 array with wavelength in AA in the first column and flux density in ergscma in the second column and, optionally, flux error in the third column^
    wl_unit:    output wavelength unit. Can be AA or meter-related (mm,um,nm,etc)
    f_unit: output flux unit. Can be ergscma or jansky related (mjy.ujy,njy,etc)
    ---------------------------------------------
    """
    wl=sed[:,0]
    f=sed[:,1]
    wl_ind,wl_unit=get_index(wl_unit)
    f_ind,f_unit=get_index(f_unit)
    c=2.99792458e+8 #speed of light in m/s
    if wl_unit!='AA' and wl_unit[-1]!='m' and f_unit!='ergscma' and f_unit[-2:]!='jy':
        raise ValueError('Wavelength units must eb either AA or m related, and flux units must be either ergscma or jy related!')
    else:
        if f_unit[-2:]=='jy':
            f=f/(1e-23*f_ind)*((wl)**2/(c*1e10))
        if sed.shape[1]>2:
            e=sed[:,2]
            if f_unit[-2:]=='jy':
                e=e/(1e-23*f_ind)*((wl)**2/(c*1e10))
        else:
            e=ones(len(f))*-99e99
        if wl_unit[-1]=='m':
            wl=wl*(1e-10/wl_ind)
    sed=np.stack((wl,f,e),axis=1)
    print(wl_ind,wl_unit,f_ind,f_unit)
    return sed

#==========================================================

def smooth_sed(sed,bins):
    """
    ---------------------------------------------
    INSTRUCTIONS:
    Smooths (i.e., rebins) a given SED
    ---------------------------------------------
    ARGS:
    sed:    Nx2 or Nx3 array, containing the wavelength and the flux and associated error of the SED
    bins:   rebinning vaulue. Must be an integer
    ---------------------------------------------
    """
    wl,f,e=[],[],[]
    lim=np.floor(len(sed[:,0])/bins)
    for i in range(int(lim-1)):
        wl.append(sed[int(bins*i+np.floor(bins/2)),0])
        f.append(np.nansum(sed[bins*i:bins*(i+1),1])/bins)
        if sed.shape[1]>2:
            e.append(np.sqrt(np.nansum(sed[bins*i:bins*(i+1),2]**2))/bins)
        else:
            e.append(-99e99)
    bin_sed=np.stack((wl,f,e),axis=1)
    return bin_sed

#==========================================================

def remove_bad_values(arr,col,ratio=1e4):
    """
    ---------------------------------------------
    INSTRUCTIONS:
    Removes the rows from an array if a column of an array contains an absolute value larger than ratio*median(abs). This criteria is completely arbitary yet useful for the working data
    ---------------------------------------------
    ARGS:
    arr:    input array, must have at least 2 columns
    col:    column index from which apply the criteria
    ---------------------------------------------
    KWARGS:
    ratio:  ratio between values and median(abs). If a value is above this ratio, that value is removed
    ---------------------------------------------
    """
    ab_arr=abs(arr[:,col])
    ab_med=np.nanmedian(ab_arr)
    new_arr=arr[ab_arr<ab_med*ratio,:]
    return new_arr
