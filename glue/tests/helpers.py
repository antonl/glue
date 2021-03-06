# Define decorators that can be used for pytest tests

from __future__ import absolute_import, division, print_function

from distutils.version import LooseVersion

import pytest


def make_skipper(module, label=None, version=None):
    label = label or module
    try:
        mod = __import__(module)
        if version:
            assert LooseVersion(mod.__version__) >= LooseVersion(version)
        installed = True
    except (ImportError, AssertionError):
        installed = False
    return installed, pytest.mark.skipif(str(not installed), reason='Requires %s' % label)


ASTROPY_INSTALLED, requires_astropy = make_skipper('astropy',
                                                   label='Astropy')

ASTROPY_GE_03_INSTALLED, requires_astropy_ge_03 = make_skipper('astropy',
                                                               label='Astropy >= 0.3',
                                                               version='0.3')

ASTROPY_GE_04_INSTALLED, requires_astropy_ge_04 = make_skipper('astropy',
                                                               label='Astropy >= 0.4',
                                                               version='0.4')

ASTRODENDRO_INSTALLED, requires_astrodendro = make_skipper('astrodendro')

SCIPY_INSTALLED, requires_scipy = make_skipper('scipy',
                                               label='SciPy')

PIL_INSTALLED, requires_pil = make_skipper('pil', label='PIL')

SKIMAGE_INSTALLED, requires_skimage = make_skipper('skimage',
                                                   label='scikit-image')

XLRD_INSTALLED, requires_xlrd = make_skipper('xlrd')

PLOTLY_INSTALLED, requires_plotly = make_skipper('plotly')

IPYTHON_GE_012_INSTALLED, requires_ipython_ge_012 = make_skipper('IPython',
                                                                 label='IPython >= 0.12',
                                                                 version='0.12')


requires_pil_or_skimage = pytest.mark.skipif(str(not SKIMAGE_INSTALLED and not PIL_INSTALLED),
                                             reason='Requires PIL or scikit-image')

GINGA_INSTALLED, requires_ginga = make_skipper('ginga')

H5PY_INSTALLED, requires_h5py = make_skipper('h5py')
