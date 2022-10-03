import numpy as np
from astropy import units as u
import speclite.filters
import os

def test_tramsform():
    import transform
    save_path = '../example_filters/'
    
    # test single input filter as string and correct return
    filter =  save_path + 'Paranal_VISTA.Y.dat'
    y_filter = np.loadtxt(filter)
    y_filter_lam = y_filter[:,0] * u.Angstrom
    y_filter_response = y_filter[:,1]

    y_filter_lam = np.insert(y_filter_lam, 0, min(y_filter_lam)-100*u.Angstrom)
    y_filter_response = np.insert(y_filter_response, 0, 0)

    y_filter_lam = np.append(y_filter_lam, max(y_filter_lam)+100*u.Angstrom)
    y_filter_response = np.append(y_filter_response, 0)

    transform.transform(filter, 'Vista', 'Y', save_path)

    speclite_filter = speclite.filters.load_filter(save_path + 'Vista-Y.ecsv')
    np.testing.assert_array_equal(speclite_filter.wavelength, y_filter_lam.value)
    np.testing.assert_array_equal(speclite_filter.response, y_filter_response)

    # test array of filters
    filters =  [save_path + 'Paranal_VISTA.J.dat', 
                save_path + 'Paranal_VISTA.H.dat', 
                save_path + 'Paranal_VISTA.KS.dat']
    transform.transform(filters, 'Vista', ['J', 'H', 'Ks'], save_path)

    speclite.filters.load_filters(save_path+'Vista-J.ecsv',
                                      save_path+'Vista-H.ecsv',
                                      save_path+'Vista-Ks.ecsv')

    os.remove(save_path+'Vista-Y.ecsv') 
    os.remove(save_path+'Vista-J.ecsv')
    os.remove(save_path+'Vista-H.ecsv')
    os.remove(save_path+'Vista-Ks.ecsv')
    

