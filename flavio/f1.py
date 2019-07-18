#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flavio
import flavio.statistics.fits
import flavio.plots as fpl
import matplotlib.pyplot as plt
import bfgamma
from flavio.physics.bdecays import bvgamma
from collections import OrderedDict

# Here we set parameters for the new decay Bs -> f1 gamma
mp=flavio.classes.Parameter('m_f1')
flavio.default_parameters.set_constraint('m_f1', 1.420)
flavio.physics.bdecays.common.meson_quark[('Bs','f1')]='bs'
flavio.physics.bdecays.common.meson_ff[('Bs','f1')]='Bs->phi'

# You can set constraints on T1(0)
flavio.default_parameters.set_constraint('Bs->phi BSZ a0_T1', 0.299 +- 0.01)

wc = flavio.WilsonCoefficients()
wc.set_initial({'C7p_bs': 0.25}, 4.8)

# Defining (new and already existing) observables

A = ('<ATIm>(B0->K*ee)', 0.002, 1.12)
P = ('<P1>(B0->K*ee)', 0.002, 1.12)


BR = 'BR(Bs->f1gamma)'
flavio.classes.Observable(BR)
flavio.classes.Observable(BR).tex=r'$\overline{\text{BR}}(B_s\to f_1\gamma)$'
flavio.classes.Prediction(BR, bfgamma.BVgamma_function(bfgamma.BR_timeint, 'Bs', 'f1'))

Ad = 'ADeltaGamma(Bs->f1gamma)'
flavio.classes.Observable(Ad)
flavio.classes.Observable(Ad).tex=r'$A_{\Delta\Gamma}(B_s\to f_1\gamma)$'
flavio.classes.Prediction(Ad, bfgamma.BVgamma_function(bfgamma.A_DeltaGamma, 'Bs', 'f1'))

S = 'S_f1gamma'
flavio.classes.Observable(S)
flavio.classes.Observable(S).tex=r'$S_{f_1\gamma}$'
flavio.classes.Prediction(S, bfgamma.BVgamma_function(bfgamma.S, 'Bs', 'f1'))

Acp = 'ACP(Bs->f1gamma)'
flavio.classes.Observable(Acp)
flavio.classes.Observable(Acp).tex=r'$A_{CP}(B_s\to f_1\gamma)$'
flavio.classes.Prediction(Acp, bfgamma.BVgamma_function(bfgamma.ACP, 'Bs', 'f1'))


BRphi='BR(Bs->phigamma)'
flavio.classes.Prediction(BRphi, bvgamma.BVgamma_function(bvgamma.BR_timeint, 'Bs', 'phi'))

Adphi = 'ADeltaGamma(Bs->phigamma)'
flavio.classes.Prediction(Adphi, bvgamma.BVgamma_function(bvgamma.A_DeltaGamma, 'Bs', 'phi'))

Sphi = 'S_phigamma'
flavio.classes.Prediction(Sphi, bvgamma.BVgamma_function(bvgamma.S, 'Bs', 'phi'))

Acpphi = 'ACP(Bs->phigamma)'
flavio.classes.Prediction(Acpphi, bvgamma.BVgamma_function(bvgamma.ACP, 'Bs', 'phi'))

# Reading measures for f1 obs. (you can modify the file meas.yml)
flavio.measurements.read_file('meas.yml')

def wc_fct(C7pRe, C7pIm):
    return { 'C7p_bs': C7pRe + 1j * C7pIm, }
def fastfit_obs(name, obslist):
    return flavio.statistics.fits.FastFit(
                name = name,
                observables = obslist,
                fit_wc_function = wc_fct,
                input_scale = 4.8
            )

# Dictionnary for individual fits. Set the ones you don't want in commentaries
fits = OrderedDict()
fits['BR'] = [BR]
"""
fits['A'] = [A]
fits['P'] = [P]
"""
fits['Acp'] = [Acp]
fits['Ad'] = [Ad]
fits['S'] = [S]
"""
fits['BRphi'] = [BRphi]

fits['Acpphi'] = [Acpphi]
fits['Adphi'] = [Adphi]
fits['Sphi'] = [Sphi]
"""
labels = {
    'BR': flavio.Observable.get_instance(BR).tex,
    'Acp': flavio.Observable.get_instance(Acp).tex,
    'Ad': flavio.Observable.get_instance(Ad).tex,
    'S': flavio.Observable.get_instance(S).tex,
    'BRphi': flavio.Observable.get_instance(BRphi).tex,
    'Acpphi': flavio.Observable.get_instance(Acpphi).tex,
    'Adphi': flavio.Observable.get_instance(Adphi).tex,
    'Sphi': flavio.Observable.get_instance(Sphi).tex,
    'A': flavio.Observable.get_instance(A[0]).tex,
    'P': flavio.Observable.get_instance(P[0]).tex
}

obs_fastfits={}
for k, v in fits.items():
    obs_fastfits[k] = fastfit_obs('C7-C7p fit '+ k, v)
  
for k, v in fits.items():
    obs_fastfits[k].make_measurement(threads=4)

# Set in the list the observables you want for the global fit. Usually same as individual fits but if it is not the case you can change the label line 130.
global_fastfit = fastfit_obs('C7-C7p fit global', [Acp, Ad, S, BR])

global_fastfit.make_measurement(threads=4)

# Scale
x_max = 1

# Plotting the fits. You can change the confidence levels with n_sigma=(...)

for i, f in enumerate(fits):
    fpl.likelihood_contour(obs_fastfits[f].log_likelihood,
                                    -x_max, x_max, -x_max, x_max, col=i+1,
                                    interpolation_factor=3, threads=4, steps=30, label=labels[f])

fpl.likelihood_contour(global_fastfit.log_likelihood,
                                -x_max, x_max, -x_max, x_max, n_sigma=(1, 2), col=0,
                                interpolation_factor=10, threads=4, steps=30, label='global')

# You can set the title
plt.title('')
plt.xlabel(r'$\text{Re}(C_7^{\prime\,\text{NP}})$')
plt.ylabel(r'$\text{Im}(C_7^\prime)$')
plt.legend()

plt.show()
