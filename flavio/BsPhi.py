#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flavio
import flavio.statistics.fits
import flavio.plots as fpl
import matplotlib.pyplot as plt
from collections import OrderedDict

BR1 = 'BR(Bs->phigamma)'
A = ('<ATIm>(B0->K*ee)', 0.002, 1.12)
P = ('<P1>(B0->K*ee)', 0.002, 1.12)

def wc_fct(C7pRe, C7pIm):
    return { 'C7p_bs': C7pRe + 1j * C7pIm, }
def fastfit_obs(name, obslist):
    return flavio.statistics.fits.FastFit(
                name = name,
                observables = obslist,
                fit_wc_function = wc_fct,
                input_scale = 4.8
            )
    
flavio.default_parameters.set_constraint('Bs->phi BSZ a0_T1',0.299 +- 0.002) # Here you can change the constraint on T1(0)

fits = OrderedDict()
fits['BR1'] = [BR1]
fits['A'] = [A]
fits['P'] = [P]

obs_fastfits={}
for k, v in fits.items():
    obs_fastfits[k] = fastfit_obs('C7-C7p fit '+ k, v)
    
for k, v in fits.items():
    obs_fastfits[k].make_measurement(threads=4)

global_fastfit = fastfit_obs('C7-C7p fit global', [BR1, A, P])

global_fastfit.make_measurement(threads=4)

labels = {
    'BR1': flavio.Observable.get_instance(fits['BR1'][0]).tex,
    'A': flavio.Observable.get_instance(fits['A'][0][0]).tex,
    'P': flavio.Observable.get_instance(fits['P'][0][0]).tex
}  

x_max = .4

for i, f in enumerate(fits):
    fpl.likelihood_contour(obs_fastfits[f].log_likelihood,
                                    -x_max, x_max, -x_max, x_max, col=i+1,
                                    interpolation_factor=3, threads=4, steps=30, label=labels[f])

fpl.likelihood_contour(global_fastfit.log_likelihood,
                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2), col=0,
                                interpolation_factor=10, threads=4, steps=30, label='global')

plt.title('')
plt.xlabel(r'$\text{Re}(C_7^{\prime\,\text{NP}})$')
plt.ylabel(r'$\text{Im}(C_7^\prime)$')
plt.legend()

plt.show()







