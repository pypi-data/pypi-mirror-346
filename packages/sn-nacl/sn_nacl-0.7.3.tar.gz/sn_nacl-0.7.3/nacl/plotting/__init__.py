"""
"""

import pathlib
import logging

_band_ordering = {'u': 0, 'U': 0, 'g': 1, 'B': 2, 'r': 3, 'r2': 3,
                  'R': 4, 'i': 5, 'i2': 5, 'I': 6, 'z': 7, 'Y': 8}

def get_band_order(band):
    b = band.split('::')[-1]
    return _band_ordering.get(b, 100)

def order_bands(bands):
    l = bands.sort(key=get_band_order)
    return l

def save_figure(fig, path, output_dir=None, pattern=None, ext='.png', **kwargs):
    """
    """
    bbox = kwargs.get('bbox_inches', 'tight')
    if isinstance(path, (str, pathlib.Path)):
        path = pathlib.Path(path)
    elif isinstance(output_dir, (str, pathlib.Path)) and isinstance(pattern, str) and isinstance(ext, str):
        path = pathlib.Path(output_dir).joinpath(pattern + ext)
    else:
        return
    if not path.parent.is_dir():
        path.parent.mkdir(exist_ok=True, parents=True)
    
    fig.savefig(path, bbox_inches=bbox)

from . import tds
from . import lightcurves
from . import spectra
from . import model
from . import snake
from . import snpars
