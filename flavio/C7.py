#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flavio
import flavio.statistics.fits
import flavio.plots as fpl
import matplotlib.pyplot as plt
from collections import OrderedDict

observables = [
  'BR(B+->K*gamma)',
  'BR(B->Xsgamma)',
  'BR(B0->K*gamma)',
  'BR(Bs->phigamma)',
  'ADeltaGamma(Bs->phigamma)',
  'S_K*gamma',
  ('<ATIm>(B0->K*ee)', 0.002, 1.12),
  ('<P1>(B0->K*ee)', 0.002, 1.12),
]

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
fits['BR'] = ['BR(B+->K*gamma)', 'BR(B->Xsgamma)', 'BR(B0->K*gamma)', 'BR(Bs->phigamma)',]
fits['A'] = ['ADeltaGamma(Bs->phigamma)']
fits['P1'] = [('<P1>(B0->K*ee)', 0.002, 1.12)]
fits['S'] = ['S_K*gamma']
fits['ATIm'] = [('<ATIm>(B0->K*ee)', 0.002, 1.12)]

obs_fastfits={}
for k, v in fits.items():
    obs_fastfits[k] = fastfit_obs('C7-C7p fit '+ k, v)

global_fastfit = fastfit_obs('C7-C7p fit global', observables)    
    
labels = {
    'BR': 'branching ratios',
    'A': flavio.Observable.get_instance(fits['A'][0]).tex,
    'S': flavio.Observable.get_instance(fits['S'][0]).tex,
    'ATIm': flavio.Observable.get_instance(fits['ATIm'][0][0]).tex,
    'P1': flavio.Observable.get_instance(fits['P1'][0][0]).tex,
}    

for k, v in fits.items():
    obs_fastfits[k].make_measurement(threads=4)
global_fastfit.make_measurement(threads=4)    

x_max = 0.33

for i, f in enumerate(fits):
    fpl.likelihood_contour(obs_fastfits[f].log_likelihood,
                                    -x_max, x_max, -x_max, x_max, col=i+1, label=labels[f],
                                    interpolation_factor=3, threads=4, steps=30)

fpl.likelihood_contour(global_fastfit.log_likelihood,
                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2, 3), col=0,
                                interpolation_factor=10, threads=4, steps=30, label='global')

plt.xlabel(r'$\text{Re}(C_7^{\prime\,\text{NP}})$')
plt.ylabel(r'$\text{Im}(C_7^\prime)$')
plt.legend(loc=2, bbox_to_anchor=(1.05, 1))

plt.show()



