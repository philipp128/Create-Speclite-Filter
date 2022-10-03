import numpy as np
from astropy import units as u

import speclite.filters

def transform(filters, group_name, band_names, save_path):
    '''
    Speclite filters obtained from filter set.

    This function takes a set of filters and transforms them into 
    speclite objects.

    Params
    ------
    filters: str or 1-d array-like of str
        Set of filters. The elements correspond to the
        filenames of the filters. The first column of the file 
        should be the wavelength in Angstrom and the 
        second columns should be the response.
    group_name: str
        Names of the filter group.
    band_names: array-like
        Names of the filter bands. Same type and shape as filters
    
    Returns
    -------
    speclite_filters: speclite filters
        Filters as specite objects
    ''' 
    if type(filters) == str:
        filters = [filters]
        band_names = [band_names]
    

    for i, filter in enumerate(filters):
        f = np.loadtxt(filter)
        wavelength = f[:,0] * u.Angstrom
        response = f[:,1]
        
        # for speclite the response curve must start with 0 and end with 0
        if response[0] != 0:
            wavelength = np.insert(wavelength, 0, min(wavelength)-100*u.Angstrom)
            response = np.insert(response, 0, 0)
        if response[-1] != 0:
            wavelength = np.append(wavelength, max(wavelength)+100*u.Angstrom)
            response = np.append(response, 0)

        speclite_filter = speclite.filters.FilterResponse(
                        wavelength = wavelength, response = response, 
                        meta=dict(group_name=group_name, band_name=band_names[i]))
        speclite_filter.save(save_path)
        
