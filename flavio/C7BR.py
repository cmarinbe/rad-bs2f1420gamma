#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flavio
import flavio.plots as fpl
import matplotlib.pyplot as plt
import flavio.statistics.fits
from collections import OrderedDict

def wc_fct(C7pRe, C7pIm):
    return { 'C7p_bs': C7pRe + 1j * C7pIm, }
def fastfit_obs(name, obslist):
    return flavio.statistics.fits.FastFit(
                name = name,
                observables = obslist,
                fit_wc_function = wc_fct,
                input_scale = 4.8,
            )

fits = OrderedDict()
fits['1'] = ['BR(B+->K*gamma)']
fits['2'] = ['BR(B->Xsgamma)']
fits['3'] = ['BR(B0->K*gamma)']
fits['4'] = ['BR(Bs->phigamma)']

obs_fastfits={}
for k, v in fits.items():
    obs_fastfits[k] = fastfit_obs('C7-C7p fit '+ k, v)      

for k, v in fits.items():
    obs_fastfits[k].make_measurement(threads=4)

x_max = .16

for i, f in enumerate(fits):
    fpl.likelihood_contour(obs_fastfits[f].log_likelihood,
                                    -x_max, x_max, -x_max, x_max, col=i+1, label=flavio.Observable.get_instance(fits[f][0]).tex,
                                    interpolation_factor=3, threads=4, steps=30)

plt.xlabel(r'$\text{Re}(C_7^{\prime\,\text{NP}})$')
plt.ylabel(r'$\text{Im}(C_7^\prime)$')
plt.legend(loc=2, bbox_to_anchor=(1.05, 1))

plt.show()

