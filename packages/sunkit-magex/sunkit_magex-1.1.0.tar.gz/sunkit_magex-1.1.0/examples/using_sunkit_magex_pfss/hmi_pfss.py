"""
HMI PFSS solutions
==================

Calculating a PFSS solution from a HMI synoptic map.

This example shows how to calculate a PFSS solution from a HMI synoptic map.
There are a couple of important things that this example shows:

- HMI maps have non-standard metadata, so this needs to be fixed
- HMI synoptic maps are very big (1440 x 3600), so need to be downsampled
  in order to calculate the PFSS solution in a reasonable time.
"""
import os

import matplotlib.pyplot as plt

import astropy.units as u

import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a

from sunkit_magex import pfss

###############################################################################
# Set up the search.
#
# The synoptic maps are labelled by Carrington rotation number instead of time.

series = a.jsoc.Series('hmi.synoptic_mr_polfil_720s')
crot = a.jsoc.PrimeKey('CAR_ROT', 2210)

###############################################################################
# Do the search.
#
# If you use this code, please replace this email address
# with your own one, registered here:
# http://jsoc.stanford.edu/ajax/register_email.html

result = Fido.search(series, crot, a.jsoc.Notify(os.environ["JSOC_EMAIL"]))
files = Fido.fetch(result)

###############################################################################
# Read in a file. This will read in the first file downloaded to a sunpy Map
# object.

hmi_map = sunpy.map.Map(files[0])

###############################################################################
# Since this map is far to big to calculate a PFSS solution quickly, lets
# resample it down to a smaller size.

print('Old shape: ', hmi_map.data.shape)
hmi_map = hmi_map.resample([360, 180] * u.pix)
print('New shape: ', hmi_map.data.shape)

###############################################################################
# Now calculate the PFSS solution

nrho = 35
rss = 2.5
pfss_in = pfss.Input(hmi_map, nrho, rss)
pfss_out = pfss.pfss(pfss_in)

###############################################################################
# Using the Output object we can plot the source surface field, and the
# polarity inversion line.

ss_br = pfss_out.source_surface_br

fig = plt.figure()
ax = fig.add_subplot(projection=ss_br)

ss_br.plot(axes=ax)
# Plot the polarity inversion line
ax.plot_coord(pfss_out.source_surface_pils[0])
plt.colorbar()
ax.set_title('Source surface magnetic field')

plt.show()
