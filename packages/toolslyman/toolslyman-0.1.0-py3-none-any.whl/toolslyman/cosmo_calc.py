# cosmology.py
from astropy import cosmology
from . import cosmo  # Import the global cosmo variable from __init__.py

def set_cosmology(name='Planck', **kwargs):
    global cosmo  # Declare cosmo as global to update the module-level variable

    # Dictionary of predefined cosmologies in astropy
    astropy_defined_cosmo = {
        'wmap1': cosmology.WMAP1,
        'wmap3': cosmology.WMAP3,
        'wmap5': cosmology.WMAP5,
        'wmap7': cosmology.WMAP7,
        'wmap9': cosmology.WMAP9,
        'planck13': cosmology.Planck13,
        'planck15': cosmology.Planck15,
        'planck18': cosmology.Planck18,
    }

    # Check if the requested cosmology is predefined in astropy
    if name.lower() in astropy_defined_cosmo:
        cosmo = astropy_defined_cosmo[name.lower()]
    else:
        # Define a custom FlatLambdaCDM cosmology
        H0 = kwargs.get('H0', 100 * kwargs.get('h0', kwargs.get('h', 0.67)))
        Om0 = kwargs.get('Om0', 0.31)
        Ob0 = kwargs.get('Ob0', 0.049)
        Tcmb0 = kwargs.get('Tcmb0', 2.725)
        cosmo = cosmology.FlatLambdaCDM(H0=H0, Om0=Om0, Ob0=Ob0, Tcmb0=Tcmb0, name=name)

    return cosmo