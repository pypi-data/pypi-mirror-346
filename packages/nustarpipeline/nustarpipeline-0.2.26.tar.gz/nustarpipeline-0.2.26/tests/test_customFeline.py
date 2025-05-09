import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from scipy.stats import norm
import shutil

from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord
from importlib import reload
from astropy.io import fits as pf
from nustarpipeline import process, utils, plotting
import pyxmmsas as pysas
import hratio
from scipy import interpolate
import json
from datetime import datetime
import logging
from time import gmtime, strftime    
import os, sys

#Parameters
continuum_comment = "  "
cyclotron_line = [[], [], []]
distance = [3.2, 4.4]
dump_second_harmonic = True
show_initial_energy_guess = True
e1_flex = 10.0
e2_flex = 20.0
forced_gaussian_amplitudes = []
forced_gaussian_centroids = []
forced_gaussian_sigmas = []
method_calc_rms = "counts"
min_sn_matrix = float(sys.argv[3])
n_high_bins_to_exclude = -1
nbins = int(sys.argv[2])
noFe = 'custom'
read_values = True
reference_main = "  "
reference_main_bib = " "
reference_urls = ["  "]
source = sys.argv[1]
threshold_p_value = 0.05
recompute_matrixes = False
run_nustar_tasks = False
rerun_nustar_pipeline = False
poly_deg : int = [3]
obsid='90602328002'
hm_steps : int = 600



reload(utils)

in_folder = 'data_tests/'

PF_file = in_folder+'pf_snr_010_nbins_032_nexcl_-1_counts.dat'

PF = np.loadtxt(PF_file, skiprows = 1)


ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac = PF[:,0], PF[:,1], PF[:,2], PF[:,3]

ind_selected = np.where((ee_pulsed < 9.0) & (ee_pulsed > 4.0))[0]


y_lim = [ np.min(pulsed_frac[ind_selected] -dpulsed_frac[ind_selected])-0.1,
          np.max(pulsed_frac[ind_selected] +dpulsed_frac[ind_selected])+0.1]

e1_flex = 60.0

noFe = 'custom'
custom_center = [[6.34, 6.2, 6.5]]
custom_sigma = [[0.06,0.025,0.4]]
stem = 'Vela_test_custom_'
pulsed_fit_dict = utils.elaborate_pulsed_fraction(ee_pulsed[ind_selected], 
                                        dee_pulsed[ind_selected], 
                                        pulsed_frac[ind_selected], 
                                        dpulsed_frac[ind_selected],
                                        debug_plots=True,
                                        stem=stem, 
                                        poly_deg = poly_deg, title=source + ' '+ obsid, save_plot=True,
                                        e1=e1_flex, e2=e2_flex, 
                                        forced_gaussian_centroids=forced_gaussian_centroids, 
                                        forced_gaussian_sigmas=forced_gaussian_sigmas,
                                        forced_gaussian_amplitudes=forced_gaussian_amplitudes, noFe = noFe,
					custom_Fe_center = custom_center, custom_Fe_sigma = custom_sigma,
                                        y_lim=y_lim, threshold_p_value = threshold_p_value)

para_hash='001'

mcmc_low, corner_low = utils.explore_fit_mcmc(pulsed_fit_dict['pulsed_fit_low'], pars=[], 
                                              hm_steps=hm_steps, 
                                              hm_walkers=50, hm_jump=int(hm_steps/10), 
                                              plot_corner=True, print_file=True, high_part=False,
                                              stem=stem, read=False, para_hash=para_hash)




noFe = False
stem = 'Vela_test_Fe_'
pulsed_fit_dict2 = utils.elaborate_pulsed_fraction(ee_pulsed[ind_selected],
                                        dee_pulsed[ind_selected],
                                        pulsed_frac[ind_selected],
                                        dpulsed_frac[ind_selected],
                                        debug_plots=True,
                                        stem=stem,
                                        poly_deg = poly_deg, title=source + ' '+ obsid, save_plot=True,
                                        e1=e1_flex, e2=e2_flex,
                                        forced_gaussian_centroids=forced_gaussian_centroids,
                                        forced_gaussian_sigmas=forced_gaussian_sigmas,
                                        forced_gaussian_amplitudes=forced_gaussian_amplitudes, noFe = noFe,
                                        y_lim=y_lim, threshold_p_value = threshold_p_value)

para_hash = '002'

mcmc_low2, corner_low2 = utils.explore_fit_mcmc(pulsed_fit_dict2['pulsed_fit_low'], pars=[], 
                                              hm_steps=hm_steps, 
                                              hm_walkers=50, hm_jump=int(hm_steps/10), 
                                              plot_corner=True, print_file=True, high_part=False,
                                              stem=stem, read=False, para_hash=para_hash)



noFe = True

stem = 'Vela_test_noFe'
pulsed_fit_dict3 = utils.elaborate_pulsed_fraction(ee_pulsed[ind_selected],
                                        dee_pulsed[ind_selected],
                                        pulsed_frac[ind_selected],
                                        dpulsed_frac[ind_selected],
                                        debug_plots=True,
                                        stem=stem,
                                        poly_deg = poly_deg, title=source + ' '+ obsid, save_plot=True,
                                        e1=e1_flex, e2=e2_flex,
                                        forced_gaussian_centroids=forced_gaussian_centroids,
                                        forced_gaussian_sigmas=forced_gaussian_sigmas,
                                        forced_gaussian_amplitudes=forced_gaussian_amplitudes, noFe = noFe,
                                        y_lim=y_lim, threshold_p_value = threshold_p_value)

para_hash='003'


mcmc_low3, corner_low3 = utils.explore_fit_mcmc(pulsed_fit_dict3['pulsed_fit_low'], pars=[], 
                                              hm_steps=hm_steps, 
                                              hm_walkers=50, hm_jump=int(hm_steps/10), 
                                              plot_corner=True, print_file=True, high_part=False,
                                              stem=stem, read=False, para_hash=para_hash) 
