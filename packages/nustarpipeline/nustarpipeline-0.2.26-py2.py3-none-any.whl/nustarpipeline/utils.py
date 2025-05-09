import logging
from numpy import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import re
from scipy.stats.mstats import trimmed_mean, trimmed_std
from subprocess import Popen, PIPE, STDOUT
from scipy.stats import norm

from .data_manipulation import *
from .plotting import *

# file_handler = logging.FileHandler(filename='nustar_utils_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
# stdout_handler = logging.StreamHandler(sys.stdout)
# handlers = [stdout_handler, file_handler]
#
# logging.basicConfig(level=logging.DEBUG, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}

shell_cmd = 'timingsuite <timing_cmd.txt'

logger = logging.getLogger('')

default_trimmed_limit = 0.05
default_trimmed_correction = 1.2669


def get_trimmed_correction(alpha=(default_trimmed_limit, default_trimmed_limit)):
    
    if alpha[0] == default_trimmed_limit and alpha[1] == default_trimmed_limit:
        return default_trimmed_correction
    
    a = norm.ppf(alpha[0])
    b = norm.ppf(1 - alpha[1])

    Z = norm.cdf(b) - norm.cdf(a)
    phi_a = norm.pdf(a)
    phi_b = norm.pdf(b)

    mean_trimmed = (phi_a - phi_b) / Z
    variance_trimmed = 1 + (a * phi_a - b * phi_b) / Z - mean_trimmed**2

    return 1. / np.sqrt(variance_trimmed)


def corrected_trimmed_std(x, axis=0, limits=(default_trimmed_limit, 
                                             default_trimmed_limit), 
                          relative=True):
    """
    Calculate the trimmed standard deviation of a dataset, correcting for the bias introduced by trimming.
    The correction is based on the assumption that the data follows a normal distribution.

    Parameters:
        x (array-like): Input data.
        alpha (float): Proportion of data to trim from each end. Default is 0.05.

    Returns:
        float: Corrected trimmed standard deviation.
    """
    if len(x) < 2:
        return np.nan
    
    if limits[0] <= 0 or limits[1] <= 0:
        std = np.std(x, axis=axis)
        correction_factor = 1.0
    else:
        # Calculate the trimmed mean and standard deviation
        std = trimmed_std(x, limits=limits, axis=axis, relative=relative)

        # Calculate the correction factor
        correction_factor = get_trimmed_correction(limits)

    # Apply the correction
    return std * correction_factor


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info(line.decode()[0:-1])


def run(cmd=shell_cmd):
    logger.info("------------------------------------------------------------------------------------------------\n")
    logger.info("**** running %s ****\n" % cmd)
    #out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
    process = Popen('export DYLD_LIBRARY_PATH=$HEADAS/lib;'+cmd, stdout=PIPE, 
                    stderr=STDOUT, shell=True)
    with process.stdout:
        log_subprocess_output(process.stdout)
    out = process.wait()  # 0 means success

    logger.info("------------------------------------------------------------------------------------------------\n")

    logger.info("Command '%s' finished with exit value %d" % (cmd, out))

    return out


def get_obsids(src):
    from astroquery.heasarc import Heasarc
    from astropy.io import ascii
    heasarc = Heasarc()
    payload = heasarc._args_to_payload(mission='numaster', entry=src, radius='10 arcmin')
    table = heasarc.query_async(payload)

    table_body = table.content.decode().split('END')[-1].strip().split('\n')
    table_body_clean = [cc for cc in table_body if 'SCIENCE' in cc and 'archived' in cc]
    logger.info("************************************")
    logger.info(src)
    logger.info("************************************")
    logger.info(table_body_clean)
    logger.info("************************************")

    try:
        data = ascii.read(table_body_clean, format='fixed_width_no_header', delimiter=' ')
        logger.info(data['col5'])
        output = [str(x) for x in data['col5'].data]
    except Exception as ee:
        logger.warning('No OBSIDS :: ' + str(ee))
        output = []

    return output


def make_basic_fit():
    ff = open('files-auto.xcm', 'w')
    ff.write('stati cstat\n')
    ff.write('data 1:1 FPMA_sr_rbn.pi\n')
    ff.write('data 2:2 FPMB_sr_rbn.pi\n')
    ff.write('ignore bad\n')
    ff.write('ignore *:**-3.0,70.0-**\n')
    ff.write('abun wilm\nmodel tbabs*high*peg')
    ff.write('\n\n\n\n\n3\n70\n1\n\n\n\n\n3\n70\n1,.1\n\n')
    ff.write('query yes\n')
    ff.write('freeze 2,3\nfit\n\n')
    ff.write('tha 2,3\nfit\n\n')
    ff.write('rm -f mod_base.xcm\nsave mod mod_base.xcm\n')
    ff.write('setpl ene\ncpd basic-plot.gif/GIF\nplot ld del\n')
    ff.write('quit\n\n')
    ff.close()

    ff = open('files-iterative.xcm', 'w')
    ff.write('stati cstat\n')
    ff.write('data 1:1 FPMA_sr_rbn.pi\n')
    ff.write('data 2:2 FPMB_sr_rbn.pi\n')
    ff.write('ignore bad\n')
    ff.write('ignore *:**-3.0,70.0-**\n')
    ff.write('@mod_base.xcm\n')
    ff.write('query yes\n')
    ff.write('setpl ene\ncpd /XW\npl ld del\n')
    ff.close()

    status = run('xspec - files-auto.xcm')
    from IPython.display import Image
    from IPython.display import display
    _ = display(Image(filename='basic-plot.gif_2', format="gif"))
    return status


def plot_periodogram():
    with open('ef_pipe_periodogram_f.qdp') as ff:
        qdp_lines = ff.readlines()
    with open('tmp.qdp', 'w') as ff:
        ff.write(qdp_lines[0])
        ff.write('cpd tmp.gif/GIF\n')
        ff.write('scr white\n')
        ff.write('ma 17 on\n')
        ff.write('time off\n')
        ff.write('lab f\n')
        for ll in qdp_lines[2:]:

            ff.write(ll)
        ff.write('\n')

    run("qdp tmp.qdp")
    from IPython.display import Image
    from IPython.display import display
    _ = display(Image(filename='tmp.gif', format="gif"))
    return


efold_cmd = '''14
1
list_evt.txt
%f
%f
ef_pipe
n
%d

%f
%f
1
0
'''

efold_orbit_cmd = '''14
1
list_evt.txt
%f
%f
ef_pipe
y
%s
%d

%f
%f
1
0
'''


def get_efold_frequency(nu_min, nu_max, min_en=3., max_en=20., n_bins=32, 
                        unit='A',
                        orbitfile=None,
                        actual_search=True):
    """It finds the spin frequency using epoch folding

    Args:
        nu_min (float): the minimum search frequency
        nu_max (float): the maximum search frequency
        min_en (float, optional): the minimum energy of events to be used. Defaults to 3 keV.
        max_en (float, optional):  the maximum energy of events to be used.. Defaults to 20 keV.
        n_bins (int, optional): number of pulse bins to use. Defaults to 32.
        unit (str, optional): the NuSTAR unit to use. Defaults to 'A'.
        orbitfile (str, optional): The orbit file for correction. Defaults to None.
        actual_search (bool, optional): If true it will run the epoch folding,
                                        if false it will read the output of aprevious search stored in the file ef_pipe_res.dat.
                                        Defaults to True.

    Raises:
        FileExistsError: FileExistsError in case the orbit file is given but not found

    Returns:
        float: the most probable spin frequency
    """

    if actual_search:
        with open('list_evt.txt', 'w') as ff:
            ff.write('source%s.evt' % unit)

        with open('timing_cmd.txt', 'w') as ff:
            if orbitfile is None:
                ff.write(efold_cmd % (min_en, max_en, n_bins, nu_min, nu_max))
            else:
                if not os.path.isfile(orbitfile):
                    raise FileExistsError('File %s does not exist' % orbitfile)

                ff.write(efold_orbit_cmd % (min_en, max_en, orbitfile, n_bins, 
                                            nu_min, nu_max))

        run()

    plot_periodogram()

    x = np.loadtxt('ef_pipe_res.dat', dtype=np.double)

    return x[2]


ls_command = '''13
%s
%s
%s
1
n
2
2
4
lc_ls_%s
n
'''


def get_nu_search_limits(filename, freq_search_interval=0.2,
                         plot_filename=None, min_frequency=1e-4,
                         max_frequency=10., orbitfile=None):
    """It uses the Lomb-Scargle periodogram to find a range of spin
        frequencies to explore
        to find a reliable periodicity

    Args:
        filename (_type_): name of the light curve in fits format to load
        freq_search_interval (float, optional): it will provide a search interval from (1-/+freq_search_interval) of the peak. Defaults to 0.2.
        plot_filename (str, optional): the name of output plot file. Defaults to None to avoid plotting.
        min_frequency (float, optional): it will search peaks only above this frequency (to avoid red-noise). Defaults to 1e-4
        max_frequency (float, optional): it will search peaks only below this frequency (to avoid red-noise). Defaults to 10

    Returns:
        nu_start, nu_stop: minimum and maximum frequencies to search
    """

    if orbitfile is None:
        binary_flag = 'n'
        str_orbitfile = 'none.dat'
    else:
        binary_flag = 'y'
        str_orbitfile = orbitfile

    with open('timing_cmd.txt', 'w') as ff:
        ff.write(ls_command % (filename, binary_flag, str_orbitfile, "auto"))

    run()

    frequencies, power = np.loadtxt('lc_ls_auto.qdp', unpack=True, skiprows=6)

    mask = (frequencies >= min_frequency) & (frequencies <= max_frequency)
    if np.sum(mask) == 0:
        logger.warning('Cannot find frequencies within the interval in LS perodogram')
        return min_frequency, max_frequency
    max_freq = frequencies[mask][np.argmax(power[mask])]
    nu_start = max_freq * (1.-freq_search_interval)
    nu_stop = max_freq * (1.+freq_search_interval)
    logger.info("We suggest to explore from %f to %f Hz" %(nu_start, nu_stop))

    if plot_filename is not None:
        plt.figure()
        plt.loglog(frequencies, power)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Power (Lomb-Scargle)')
        plt.axvspan(nu_start, nu_stop, alpha=0.5, color='cyan')
        plt.savefig(plot_filename)

    return nu_start, nu_stop


enphase_cmd = '''17
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
%19.12e
n
%f
%f
%f
0
0
0
1000000000
'''

enphase_cmd_binfile = '''17
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
%19.12e
y
%s
0
0
0
0
1000000000
'''

enphase_cmd_orbit = '''17
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
%19.12e
n
%f
%f
%f
0
0
0
1000000000
'''

enphase_cmd_orbit_binfile = '''17
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
%19.12e
y
%s
0
0
0
0
1000000000
'''


xselect_gti_filter = '''dummy

read eve %s
./
yes
filter time file %s
extract events
save events %s
yes


quit
no

'''


def make_enphase(freq,  min_en=3., max_en=70., en_step=0.5, n_bins=32,
                 orbitfile=None, nudot=0, t_ref=0, user_gti=None,
                 nudodot=0):

    '''
    Wrapper on timingsuite to produce Energy - Phase matrixes for source and background for both FPM units.
    :param freq: spin frequency
    :param min_en: minimum energy (default is 3 keV)
    :param max_en: mximum energy (default is 70 keV)
    :param en_step: energy step (default is 0.5 keV)
    :param n_bins: number of phase bins (default is 32)
    :param orbitfile: orbitfile for orbital correction (timingsuite) if None
    :param nudot: spinn requency derivative (default is 0)
    :param t_ref: reference time for folding (if <= 0, it adds to the first time)
    ;param user_gti : user GTI file (defaults to None to avoid extraction)
    ;nudotdot (int, optional): frequency second derivative. Defaults to 0.
    :return: it writes the fits files sourceA_ENPHASE.fits sourceB_ENPHASE.fits
                        backgroundA_ENPHASE.fits backgroundB_ENPHASE.fits
    '''

    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                if user_gti is not None:
                    with open('gti_select_cmd.txt', 'w') as f2:
                        f2.write(xselect_gti_filter %('%s%s.evt' % (tt, unit), user_gti, '%s%s_filtered.evt' % (tt, unit) ))
                    run('rm -f %s%s_filtered.evt' % (tt, unit))
                    run('xselect < gti_select_cmd.txt')
                    ff.write('%s%s_filtered.evt' % (tt, unit) )
                else:
                    ff.write('%s%s.evt' % (tt, unit))

            if orbitfile is None:
                with open('timing_cmd.txt', 'w') as ff:
                    if type(en_step) is float:
                        ff.write(enphase_cmd % ('%s%s_ENPHASE.fits' % (tt, unit),
                                                n_bins, t_ref, freq, nudot, nudodot,
                                                en_step, min_en, max_en) )
                    else:
                        if not os.path.isfile(en_step):
                            raise FileExistsError('File %s does not exist' % en_step)
                        ff.write(enphase_cmd_binfile % ('%s%s_ENPHASE.fits' % (tt, unit),
                                                        n_bins, t_ref, freq, nudot,
                                                        nudodot, en_step))
            else:
                if not os.path.isfile(orbitfile):
                    raise FileExistsError('File %s does not exist' % orbitfile)

                with open('timing_cmd.txt', 'w') as ff:
                    if type(en_step) is float:
                        ff.write(enphase_cmd_orbit % ('%s%s_ENPHASE.fits' % (tt, unit), orbitfile,
                                                      n_bins, t_ref, freq, nudot,
                                                      nudotdot, en_step, min_en, max_en) )
                    else:
                        if not os.path.isfile(en_step):
                            raise FileExistsError('File %s does not exist' % en_step)
                        ff.write(enphase_cmd_orbit_binfile % ('%s%s_ENPHASE.fits' % (tt, unit),
                        orbitfile, n_bins, t_ref, freq, nudot, nudodot, en_step))

            run()
            shutil.copy('%s%s_ENPHASE.fits' % (tt, unit), '%s%s_ENPHASE_%03d.fits' % (tt, unit, n_bins))


def pad_matrices_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max, pp2, dpp2, tolerance=1e-2):
    '''
    :param x1_min:
    :param x1_max:
    :param pp1:
    :param dpp1:
    :param x2_min:
    :param x2_max:
    :param pp2:
    :param dpp2:
    :param tolerance:
    :return:
    '''
    if len(x1_min) == len(x2_min):
        diff = np.sum(x1_min - x2_min)
        if np.abs(diff) > tolerance:
            logger.warning("vector lower edges have same size but likely different values")
        return x1_min, x1_max, pp1, dpp1, x2_min, x2_max, pp2, dpp2

    if len(x1_min) < len(x2_min):
        new_x1_min, new_x1_max, new_pp1, new_dpp1 = pad_matrix_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max)
        return new_x1_min, new_x1_max, new_pp1, new_dpp1, x2_min, x2_max, pp2, dpp2

    if len(x1_min) > len(x2_min):
        new_x2_min, new_x2_max, new_pp2, new_dpp2 = pad_matrix_with_zeros(x2_min, x2_max, pp2, dpp2, x1_min, x1_max)
        return x1_min, x1_max, pp1, dpp1, new_x2_min, new_x2_max, new_pp2, new_dpp2


def pad_matrix_with_zeros(x1_min, x1_max, pp1, dpp1, x2_min, x2_max):
    '''
    returns matrix padded with zeros to fill the gaps
    :param x1_min:
    :param x1_max:
    :param pp1:
    :param dpp1:
    :param x2_min:
    :param x2_max:
    :return:
    '''

    new_x1_min = []
    new_x1_max = []
    new_pp1 = []
    new_dpp1 = []
    n_bins = pp1.shape[1]
    for y, z in zip(x2_min, x2_max):
        found = False
        for i in range(len(x1_min)):
            if x1_min[i] == y:
                new_x1_min.append(x1_min[i])
                new_x1_max.append(x1_max[i])
                new_pp1.append(pp1[i, :])
                new_dpp1.append(dpp1[i, :])
                found = True

        if not found:
            new_x1_min.append(y)
            new_x1_max.append(z)
            new_pp1.append(np.zeros(n_bins))
            new_dpp1.append(np.zeros(n_bins))

    if len(x2_min) != len(new_x1_min):
        raise RuntimeError('Padding matrix with zeros gave wrong sizes !!')

    return np.array(new_x1_min), np.array(new_x1_max), np.array(new_pp1), np.array(new_dpp1)


def read_one_matrix(kind, unit, background_difference_limit=-1, nbins=None, use_counts=False, subtract_background=True):
    '''
    Read matrix from one NuSTAR unit and optionally subtract the background.
    Note that if background_difference_limit>0, the output source and background matrices might have different shapes

    :param kind: 'E' for Energy-Phase, 'T' for Time-Phase
    :param unit: 'A' or 'B' for FPM unit
    :param background_difference_limit:
            =0 does not subtract the background
            <0 subtracts the background after padding background matrix with zeros
            >0  if sizes of source and background matrices differs by more than this value, it will skip subtraction
    :param use_counts: if correcting for the exposure
    :return: x_min lower edge of time or energy bins
             x_min upper edge of time or energy bins,
             pp matrix
             dpp matrix of uncertainties
             pp_b background matrix
             dpp_b matrix of background uncertainties

    '''
    import astropy.io.fits as pf

    if not (unit == 'A' or unit == 'B'):
        raise UserWarning('The unit must be A or B, you have %s ' % unit)

    if kind == 'E':
        fname_src = 'source%s_ENPHASE' % unit
        fname_bck = 'background%s_ENPHASE' % unit
        key1 = 'E_MIN'
        key2 = 'E_MAX'
    elif kind == 'T':
        key1 = 'T_START'
        key2 = 'T_STOP'
        fname_src = 'source%s_TPHASE' % unit
        fname_bck = 'background%s_TPHASE' % unit
    else:
        raise UserWarning('The kind of matrix can be E or T, you gave %s' % kind)

    if nbins is not None:
        fname_src += '_%03d' % nbins
        fname_bck += '_%03d' % nbins

    fname_src += '.fits'
    fname_bck += '.fits'

    logger.info('Reading %s and %s' % (fname_src, fname_bck))

    ff = pf.open(fname_src, 'readonly')
    t_minA = ff[1].data[key1]
    t_maxA = ff[1].data[key2]
    ptA = ff[1].data['MATRIX']
    dptA = ff[1].data['ERROR']
    if 'Exposure' in ff[1].data.names:
        exposureA = ff[1].data['Exposure']
    else:
        exposureA = np.ones(ptA.shape)
    ff.close()

    ff = pf.open(fname_bck, 'readonly')
    t_minAb = ff[1].data[key1]
    t_maxAb = ff[1].data[key2]
    ptbA = ff[1].data['MATRIX']
    dptbA = ff[1].data['ERROR']
    if 'Exposure' in ff[1].data.names:
        exposure_bA = ff[1].data['Exposure']
    else:
        exposure_bA = np.ones(ptbA.shape)
    ff.close()

    if use_counts:
        ptA *= exposureA
        dptA *= exposureA
        ptbA *= exposure_bA
        dptbA *= exposure_bA

    if background_difference_limit < 0:
        t_minA, t_maxA, ptA, dptA, t_minAb, t_maxAb, ptbA, dptbA = \
            pad_matrices_with_zeros(t_minA, t_maxA, ptA, dptA, t_minAb, t_maxAb, ptbA, dptbA)
        #print("Padding in reading one matrix ", ptA.shape, ptbA.shape)
        #print(t_minA.shape, t_minAb.shape)
        if subtract_background:
            ptA -= ptbA
            dptA = np.sqrt(dptbA ** 2 + dptA ** 2)
            logger.info('Subtracted the background, possibly padded with zeros')
        else:
            logger.info("Not subtracting the background")
    elif background_difference_limit > 0:
        if np.abs(len(t_minA) - len(t_minAb)) < background_difference_limit and subtract_background:
            indA, indAb = get_ind_combine(t_minA, t_minAb)
            t_minA = t_minA[indA]
            t_maxA = t_maxA[indA]

            ptA = ptA[indA, :] - ptbA[indAb, :]
            dptA = np.sqrt(dptA[indA, :] ** 2 + dptbA[indAb, :] ** 2)
            logger.info('Subtracted the background')
        else:
            logger.info('We do not subtract the background: difference in matrix dimension is %d and subtract_backgroun is %b' %
                        (np.abs(len(t_minA) - len(t_minAb)), subtract_background))

    return t_minA, t_maxA, ptA, dptA, ptbA, dptbA


def read_and_sum_matrixes(kind, background_difference_limit=-1,
                          use_counts=False, subtract_background=True,
                          nbins=None):
    '''
    Reads and sum matrixes fromt he two NuSTAR units by reading the files
    sourceA_ENPHASE.fits
    sourceA_TPHASE.fits
    sourceB_ENPHASE.fits
    sourceB_TPHASE.fits
    backgroundA_ENPHASE.fits
    backgroundA_TPHASE.fits
    backgroundB_ENPHASE.fits
    backgroundB_TPHASE.fits
    It assumes they are present in obs_lc.

    if nbins is specified it will try to read the files (here the example is for nbins=32)
    backgroundA_ENPHASE_032.fits
    backgroundA_TPHASE_032.fits
    backgroundB_ENPHASE_032.fits
    backgroundB_TPHASE_032.fits
    sourceA_ENPHASE_032.fits
    sourceA_TPHASE_032.fits
    sourceB_ENPHASE_032.fits
    sourceB_TPHASE_032.fits

    (Note that if background_difference_limit>0, the method is not tested as the output source and background matrixes might have different shape)

    :param kind: 'E' for ENERGY-Phase, 'T'  for 'TIME-Phase
    :param background_difference_limit: if >0 removes at most this number of rows to match background and source matrixes
                                        if <=0 it pads the smalle matrix with zeros (default -1)
    :param subtract background: boolean to subtract the background (default true)
    :param nbins Specify the number of phase bins of the matrix to read (it should be present) if None it takes the
    :return:
    x_min array of minimum times or energies
    x_max array of maximum times or energies
    pp matrix
    dpp matrix uncertainties
    pp_b backound matrix
    dpp_b background matrix uncertainties
    '''
    t_minA, t_maxA, ptA, dptA, ptbA, dptbA = read_one_matrix(kind, 'A',
                                                             background_difference_limit=background_difference_limit,
                                                             use_counts=use_counts,
                                                             subtract_background=subtract_background,
                                                             nbins=nbins)
    t_minB, t_maxB, ptB, dptB, ptbB, dptbB = read_one_matrix(kind, 'B',
                                                             background_difference_limit=background_difference_limit,
                                                             use_counts=use_counts,
                                                             subtract_background=subtract_background,
                                                             nbins=nbins)

    if background_difference_limit > 0:
        indA, indB = get_ind_combine(t_minA, t_minB)
        t_min = t_minA[indA]
        t_max = t_maxA[indA]
        pp = ptA[indA, :] + ptB[indB, :]
        dpp = np.sqrt(dptA[indA, :] ** 2 + dptB[indB, :] ** 2)
        pp_b = ptbA[indA, :] + ptbB[indB, :]
        dpp_b = np.sqrt(dptbA[indA, :] ** 2 + dptbB[indB, :] ** 2)

    else:
        # print(ptA.shape, ptB.shape, ptbA.shape,  ptbB.shape)
        t_min, t_max, ptA, dptA, _, _, ptB, dptB = \
            pad_matrices_with_zeros(t_minA, t_maxA, ptA, dptA, t_minB,
                                    t_maxB, ptB, dptB)
        # print(ptA.shape, ptB.shape, ptbA.shape,  ptbB.shape)
        # print(t_minA.shape, t_minB.shape, t_maxA.shape,  t_maxB.shape)
        _, _, ptbA, dptbA, _, _, ptbB, dptbB = \
            pad_matrices_with_zeros(t_minA, t_maxA, ptbA, dptbA, t_minB,
                                    t_maxB, ptbB, dptbB)
        # print(ptA.shape, ptB.shape, ptbA.shape,  ptbB.shape)
        # print(t_minA.shape, t_minB.shape, t_maxA.shape,  t_maxB.shape)
        pp = ptA + ptB
        dpp = np.sqrt(dptA ** 2 + dptB ** 2)
        pp_b = ptbA + ptbB
        dpp_b = np.sqrt(dptbA ** 2 + dptbB ** 2)

    logger.info('Matrix for unit A has size %d x %d ' % (ptA.shape[0], ptA.shape[1]))
    logger.info('Matrix for unit B has size %d x %d ' % (ptB.shape[0], ptB.shape[1]))
    logger.info('Background Matrix for unit A has size %d x %d ' % (ptbA.shape[0], ptbA.shape[1]))
    logger.info('Background Matrix for unit B has size %d x %d ' % (ptbB.shape[0], ptbB.shape[1]))
    logger.info('The combined matrix has size %d x %d' % (pp.shape[0], pp.shape[1]))

    return t_min, t_max, pp, dpp, pp_b, dpp_b


def get_ind_combine_engine(x1, x2):
    '''
    Util function to find index of common values in x1 and x2
    :param x1:
    :param x2:
    :return:
    '''
    ind1 = []
    ind2 = []
    n_removed = 0
    for i in range(len(x1)):
        not_found = True
        for j in range(max((i - n_removed), 0), len(x2)):
            if x1[i] == x2[j]:
                ind1.append(i)
                ind2.append(j)
                not_found = False
                logger.debug("Found %d %d" % (i, j))
                break
        if not_found:
            logger.debug("Remove %d" % i)
            n_removed += 1
    return ind1, ind2


def get_ind_combine(t_minA, t_minB):
    '''
    it calls get_ind_combine_engine after sorting for length
    :param t_minA:
    :param t_minB:
    :return:
    '''
    if len(t_minA) == len(t_minB):
        return np.arange(len(t_minA)), np.arange(len(t_minB))
    elif len(t_minA) < len(t_minB):
        return get_ind_combine_engine(t_minA, t_minB)
    else:
        indA, indB = get_ind_combine_engine(t_minB, t_minA)
        return indB, indA


tphase_cmd = '''12
list_evt.txt
none
%s
n
%d
%19.12e
%19.12e
%19.12e
%19.12e
n
%f
0
0
%f
%f
'''

tphase_cmd_orbit = '''12
list_evt.txt
none
%s
y
%s
%d
%19.12e
%19.12e
%19.12e
%19.12e
n
%f
0
0
%f
%f
'''


def make_tphase(freq,  min_en=3., max_en=70., t_step=1000, n_bins=32,
                orbitfile=None, nudot=0, t_ref=0, user_gti=None, nudotdot=0.):
    """It builds the time-phase matrix

    Args:
        freq (float): folding frequency in Hertz
        min_en (float, optional): minimum energy to accumulate the matrix. Defaults to 3..
        max_en (float, optional): maximum energy to accumulate the matrix. Defaults to 70..
        t_step (int, optional): time step. Defaults to 1000.
        n_bins (int, optional): number of bins of the pulse profile. Defaults to 32.
        orbitfile (string, optional): name of the orbit correction file. Defaults to None.
        nudot (int, optional): frequency derivative. Defaults to 0.
        t_ref (int, optional): folding reference time (<=0 it takes the first time). Defaults to 0 to take the first time.
        user_gti (str, optional): file name for user GTI, default None skips the GTI selection
        nudotdot (int, optional): frequency second derivative. Defaults to 0.

    Raises:
        It writes the time phase matrixes in fits format
    """
    for tt in ['source', 'background']:
        for unit in ['A', 'B']:
            with open('list_evt.txt', 'w') as ff:
                if user_gti is not None:
                    with open('gti_select_cmd.txt', 'w') as f2:
                        f2.write(xselect_gti_filter % ('%s%s.evt' % (tt, unit),
                                                       user_gti,
                                                       '%s%s_filtered.evt' % (tt, unit)))
                    run('rm -f %s%s_filtered.evt' % (tt, unit))
                    run('xselect < gti_select_cmd.txt')
                    ff.write('%s%s_filtered.evt' % (tt, unit))
                else:
                    ff.write('%s%s.evt' % (tt, unit))

            with open('timing_cmd.txt', 'w') as ff:
                if orbitfile is None:
                    ff.write(tphase_cmd % ('%s%s_TPHASE.fits' % (tt, unit),
                                           n_bins, t_ref, freq, nudot,
                                           nudotdot, t_step, min_en, max_en))
                else:
                    if not os.path.isfile(orbitfile):
                        raise FileExistsError('File %s does not exist' % orbitfile)
                    ff.write(tphase_cmd_orbit % ('%s%s_TPHASE.fits' % (tt, unit), orbitfile,
                                                 n_bins, t_ref, freq, nudot, nudotdot,
                                                 t_step, min_en, max_en))
                    # print(tphase_cmd_orbit % ('%s%s_TPHASE.fits' % (tt, unit), orbitfile,
                    #                        n_bins, t_ref, freq, nudot, t_step, min_en, max_en))

            run()
            shutil.copy('%s%s_TPHASE.fits' % (tt, unit),
                        '%s%s_TPHASE_%03d.fits' % (tt, unit, n_bins))


def rebin_matrix(e_min_matrix, e_max_matrix, pp_input_matrix, dpp_input_matrix,
                 min_s_n=50, only_pulsed=False, use_counts=False,
                 background_matrix=None,
                 flip=False):
    '''
    :param e_min_matrix: array with minimum energy of each bin
    :param e_max_matrix: array with maximum energy of each bin
    :param pp_input_matrix: 2-d array with pulse profiles
    :param dpp_input_matrix: 2-d array with pulse profile uncertainties
    :param min_s_n: minimum S/N for rebin
    :param only_pulsed:  it subtracts the average value before rebinning
    ;param background_matrix a couple (background, background_uncertainty)
    :param flip : boolean ; if True rebin matrix from the last channel
    :return:
    new_e_mins rebinned array with minimum energy of each bin
    new_e_maxs rebinned array with maximum energy of each bin
    new_pulses rebinned 2-d array with pulse profiles
    dnew_pulses rebinned 2-d array with pulse profile uncertainties
    (new_background rebinned 2-d array with background pulse profiles
    dnew_background rebinned 2-d array with background pulse profiles uncertainties) - returned only if background is not None !
    '''
    e_min = copy.deepcopy(e_min_matrix)
    e_max = copy.deepcopy(e_max_matrix)
    pp_input = copy.deepcopy(pp_input_matrix)
    dpp_input = copy.deepcopy(dpp_input_matrix)

    if flip:
        logger.info('Rebinning starts from highest energy/time channel')
        e_min = np.flip(e_min)
        e_max = np.flip(e_max)
        pp_input = np.flip(pp_input)
        dpp_input = np.flip(dpp_input)

    new_pulses = []
    dnew_pulses = []
    new_e_mins = []
    new_e_maxs = []
    i1 = 0
    rebinned_index = 0

    pp = copy.deepcopy(pp_input)
    dpp = copy.deepcopy(dpp_input)

    if background_matrix is not None:
        background = [[],[]]
        background[0] = copy.deepcopy(background_matrix[0])
        background[1] = copy.deepcopy(background_matrix[1])
        if flip:
            backk = np.flip(background[0])
            dbackk = np.flip(background[1])
            pp_b = copy.deepcopy(backk)
            dpp_b = copy.deepcopy(dbackk)
        else:
            pp_b = copy.deepcopy(background[0])
            dpp_b = copy.deepcopy(background[1])

        new_pulses_b = []
        dnew_pulses_b = []

    while i1 < len(e_min) - 1:
        p1 = copy.copy(pp[i1, :])
        dp1 = copy.copy(dpp[i1, :])
        if background_matrix is not None:
            p1_b = copy.copy(pp_b[i1, :])
            dp1_b = copy.copy(dpp_b[i1, :])
        logger.debug('%d' % i1)
        for i2 in range(i1 + 1, len(e_min)):

            ind = dp1 > 0
            if only_pulsed:
                s_n = np.sum(np.abs(p1[ind] - np.mean(p1[ind]))) / np.sqrt(np.sum(dp1[ind] ** 2))
            else:
                s_n = np.sum(np.abs(p1[ind])) / np.sqrt(np.sum(dp1[ind] ** 2))

            logger.debug(s_n)
            #print(np.sum(np.abs(p1)), np.sqrt(np.sum(dp1 ** 2)), s_n)
            if s_n >= min_s_n or i2 == len(e_min) - 1:
                if use_counts:
                    new_pulses.append(p1)
                    dnew_pulses.append(dp1)
                else:
                    new_pulses.append(p1/float(i2-i1))
                    dnew_pulses.append(dp1/float(i2-i1))
                if background_matrix is not None:
                    if use_counts:
                        new_pulses_b.append(p1_b)
                        dnew_pulses_b.append(dp1_b)
                    else:
                        new_pulses_b.append(p1_b/float(i2-i1))
                        dnew_pulses_b.append(dp1_b/float(i2-i1))
                if flip:
                    new_e_mins.append(e_min[i2 - 1])
                    new_e_maxs.append(e_max[i1])
                else:
                    new_e_mins.append(e_min[i1])
                    new_e_maxs.append(e_max[i2 - 1])
                logger.debug("Boom %f %d %d " % (s_n, i1, i2))
                # print("Boom", s_n, i1, i2)
                # print(np.mean(p1)/float(i2-i1), np.mean(dp1)/float(i2-i1))
                i1 = i2
                logger.debug('Rebinned index : %d' % rebinned_index)
                # print('Rebinned index : %d' % rebinned_index)
                rebinned_index += 1
                break
            else:
                logger.debug("i2 %d" % i2)

                p1 += pp[i2, :]
                dp1 = np.sqrt(dp1 ** 2 + dpp[i2, :] ** 2)
                if background_matrix is not None:
                    p1_b += pp_b[i2, :]
                    dp1_b = np.sqrt(dp1_b ** 2 + dpp_b[i2, :] ** 2)

                # print("i2", i2)
                # print(np.count_nonzero(p1), np.count_nonzero(pp[i2, :]))
                #It may happen that 1 background photon (negative rate) makes a bin to zero
                # if np.count_nonzero(p1) < old_nonzero:
                #     print(p1)
                #     print(pp[i2, :])
                #old_nonzero = np.count_nonzero(p1)

    logger.info('We rebinned from %d to %d bins at a minimum S/N of %.1f' % (len(e_min), len(new_e_mins), min_s_n))
    # not sure this is a good practice
    if background_matrix is None:
        if flip:
            return np.flip(np.array(new_e_mins)), np.flip(np.array(new_e_maxs)), np.flip(np.array(new_pulses)), np.flip(
                np.array(dnew_pulses))
        else:
            return np.array(new_e_mins), np.array(new_e_maxs), np.array(new_pulses), np.array(dnew_pulses)
    else:
        if flip:
            return np.flip(np.array(new_e_mins)), np.flip(np.array(new_e_maxs)),\
                np.flip(np.array(new_pulses)), np.flip(np.array(dnew_pulses)), \
                    np.flip(np.array(new_pulses_b)), np.flip(np.array(dnew_pulses_b))
        else:
            return np.array(new_e_mins), np.array(new_e_maxs), np.array(new_pulses),\
                np.array(dnew_pulses), np.array(new_pulses_b), np.array(dnew_pulses_b)


def pulsed_fraction_area(c, dc, background=None, background_error=None):
    """It computes the pulsed fraction with the Area method (ref. )
    remember PF is a factor  of about 1.4 the other PFs

    Args:
        c (numpy array): the pulse profile
        dc (numpy array): the pulse profile uncertainty [used for error computation]

    Returns:
       numpy float: the pulsed fraction!
    """
    logger.debug('remember PF is a factor  of about 1.4 the other PFs')
    a0 = 0
    if background is not None and background_error is not None:
        a0 = subtract_background(a0, background, background_error)
    return np.sum((c - a0) - (np.min(c - a0))) / np.sum(c-a0)


def compute_a_b_sigma_a_sigma_b(counts, counts_err, K):
    """auxiliary function for Pf method by Archibald 2014 (and others)

    Args:
        counts (numpy array): the pulse profile
        counts_err (numpy array): the pulse profile uncertainties
        K (int): number of harmonics

    Returns:
        a, b, sigma_a, sigma_b (numpy arrays): these vectors
    """
    N = np.size(counts)
    A = np.zeros(K)
    B = np.zeros(K)
    a = np.zeros(K)
    b = np.zeros(K)
    sigma2_a = np.zeros(K)
    sigma2_b = np.zeros(K)

    for k in range(K):

        argsinus = (2 * np.pi * (k + 1) * np.arange(1, N+1, dtype=float)) / N

        L = counts * np.cos(argsinus)

        M = counts * np.sin(argsinus)

        P = counts_err ** 2 * np.cos(argsinus) ** 2
        O = counts_err ** 2 * np.sin(argsinus) ** 2
        #
        A[k] = np.sum(L)

        B[k] = np.sum(M)

        SIGMA_A = np.sum(P)
        SIGMA_B = np.sum(O)
        #
        a[k] = A[k] / N

        b[k] = B[k] / N
        sigma2_a[k] = SIGMA_A / N**2
        sigma2_b[k] = SIGMA_B / N**2

    return a, b, sigma2_a, sigma2_b


def pulse_fraction_from_data_rms(counts, counts_err, n_harm=-1,
                                 background=None,
                                 background_error=None,
                                 plot=False, label='', verbose=False,
                                 statistics='cstat', level=0.1):

    """pulsed fractio computation
        following Archibald et al (2014) that uses de Jager et al. (1986)
    Args:
        counts (_type_): pulse profile
        counts_err (_type_): pulse profile uncertainty
        n_harm (int, optional): number of used harmonics. If <=0, it determines the optimal number. default -1
        :param level: minimum confidence level to stop number of harmonics (default 0.1, lower values give less harmonics)
        :param n_harm: maximum number of harmonics to use (default -1 takes the size of pulse profile)
        :param plot: plot the pulse profile
        :param label: to save the plot with name "rms_`label`.pdf", if label=='' it does not save the plot
        ;parma verbose (bool): if true it returns both pulsed_frac, n_harm, if false just the pulsed_frac
        ;param background the vector of the background
        ;param backgroun_error the uncertainty vector of the background
        statistics (str, optional) : the method to compute the optimal number of harmonics (chi2, cstat, archibald) de cstat, see the function get_n_harm

    Returns:
        numppy double: pulsed fraction
    """
    from matplotlib import cm

    a0 = np.mean(counts)
    N = np.size(counts)

    if n_harm <= 0:
        K = get_n_harm(counts, counts_err, n_harm_min=2, n_harm_max=-1,
                       statistics=statistics, level=level)
    elif n_harm > N/2:
        K = int(N/2)
    else:
        K = n_harm

    a, b, sigma2_a, sigma2_b = compute_a_b_sigma_a_sigma_b(counts, counts_err, K)

    somma = a[0:K] ** 2 + b[0:K] ** 2
    # print(somma)
    differenza = sigma2_a[0:K] + sigma2_b[0:K]
    bla = somma - differenza

    # print('diff: ',differenza)
    logger.debug('Pre background average %f' % a0)
    if background is not None and background_error is not None:
        a0 = subtract_background(a0, background, background_error)
    logger.debug('Post background average %f' % a0)

    summed_bla = np.sum(bla)

    if summed_bla < 0:
        logger.warning('Poissononian correction in pulse_fraction_from_data_rms gives a negative value, resetting it to zero ')
        summed_bla = 0
    PF_rms = np.sqrt(2 * summed_bla) / a0

    col = cm.viridis(np.linspace(0, 1, int(500)))
    if plot:
        import matplotlib.pyplot as plt
        f = np.linspace(0, 1, int(N))

        plt.errorbar(f, counts, yerr=counts_err, fmt='.',color=col[K])
        plt.plot(f, counts, linestyle='--', color=col[K])
        # plt.text(0.4,120,str(K)+'  harmonics',color = col[K])
        plt.xlabel('Phase')
        plt.ylabel('Counts')
        # plt.legend()
        if label != '':
            plt.savefig('rms_%s.pdf' % label)

    if verbose:
        return PF_rms, K
    else:
        return PF_rms


def subtract_background(a0, background, background_error):
    """subtracts background from the average

    Args:
        a0 (float): input average
        background (numpy array): vector of background values
        background_error (numpy array): vector of background values uncertainties

    Raises:
        Exception: if the subtracted continuun level is zero should we raise an exception ?

    Returns:
        a0 (loat): background subtracted average
    """
    ind = background_error > 0
    if np.sum(ind)>0:
        background_level = np.sum(background[ind]/background_error[ind]**2) / np.sum(1./background_error[ind]**2)
        logger.debug('Background level %f' % background_level)
        a0_out = a0 - background_level
        if a0 == 0:
            a0_out = background_level
            logger.debug('continuum level is zero')
            #raise Exception
    else:
        a0_out = a0
        logger.warning('Zero background level')
    return a0_out


def get_phases(pp, dpp, ind_selected=None, ee_pulsed=None, dee_pulsed=None,
               plot=True,
               margin=0.5, debug=False, distance_factor=2,
               output_figure_file=None,
               output_file=None, read=False):
    """gets the phases with uncertainties of all pulses in a matrix

    Args:
        pp (numopy array): a time- or energy-phase matrix
        dpp (numopy array): a time- or energy-phase uncertainty matrix
        ind_selected (numpy array, optional): a selection index, Defaults to None -> keeps all
        ee_pulsed (numpy array, optional): the axis vector (energy). Defaults to None.
        dee_pulsed (numpy array, optional): the axis vector uncertainty (energy). Defaults to None.
        plot (bool, optional): if making the plot. Defaults to True.
        margin (float, optional): parameter to align_phases. Defaults to 0.5.
        debug (bool, optional): if show debug. Defaults to False.
        distance_factor (int, optional): parameer to align matrix. Defaults to 2.
        output_figure_file (str, optional): file name to save the figure. Defaults to None.
        output_file (string, optional): a file to putput the phases. Defaults to None.
        read (bool, optional): if try to read the results from output_file. Defaults to False.

    Returns:
       np.array(As) amplitudes of fundamental
       np.array(dAs) amplitude- of-fundamental uncertainties
       np.array(phi0) phases of fundamental
       np.array(dphases) phase-of-fundamental uncertainties
       np.array(A2s) amplitudes of harmonic
       np.array(dA2s) amplitude-of-harmonic uncertainties
       np.array(phi0_2) phases of harmonic
       np.array(dphases2) phase-of-harmonic uncertainties
    """    

    if output_file is not None and read is True:
        if os.path.isfile(output_file):
            ee_pulsed, dee_pulsed, \
                As, dAs, phases, dphases, \
                A2s, dA2s, phases2, dphases2 = np.loadtxt(output_file,
                                                          unpack=True,
                                                          skiprows=1)
            return As, dAs, phases, dphases, A2s, dA2s, phases2, dphases2
        else:
            logger.warning(f'{output_file} is not a file, recomputing phases')

    if ind_selected is None:
        ind_selected = range(pp.shape[0])

    phases = []
    dphases = []
    phases2 = []
    dphases2 = []

    As = []
    dAs = []
    A2s = []
    dA2s = []
    
    for i in ind_selected:
        y = pp[i,:]
        dy = dpp[i,:]
        A, phi = get_fourier_coeff(y)
        dA, dphi = get_fourier_coeff_error(y, dy)
        phases.append(phi[0])
        dphases.append(dphi[0])
        phases2.append(phi[1])
        dphases2.append(dphi[1])
        As.append(A[0])
        dAs.append(dA[0])
        A2s.append(A[1])
        dA2s.append(dA[1])

    phi0 = align_phases(np.array(phases),
                        margin=margin, debug=debug,
                        distance_factor=distance_factor)
    phi0_2 = align_phases(np.array(phases2),
                          margin=margin, debug=debug,
                          distance_factor=distance_factor)

    if output_file is not None:
        with open(output_file, 'w') as out:
            out.write('e de A1 dA1 phi1 pdhi1 A2 dA2 phi2 dphi2\n')
            for j, i in enumerate(ind_selected):
                out.write('%e %e %e %e %e %e %e %e %e %e\n' % (ee_pulsed[i],
                                                               dee_pulsed[i],
                                                               As[j], dAs[j],
                                                               phi0[j],
                                                               dphases[j],
                                                               A2s[j], dA2s[j],
                                                               phi0_2[j],
                                                               dphases2[j]))

    if plot and ee_pulsed is not None and dee_pulsed is not None:
        color = iter(plt.cm.viridis(np.linspace(0, 1, 5)))
        fig, ax = plt.subplots(2,2, sharex=True, figsize=(8, 6))
        ax[0][0].errorbar(ee_pulsed[ind_selected], phi0,
                          xerr=dee_pulsed[ind_selected],
                          yerr=dphases, linestyle='',
                          marker='.',color=next(color))
        ax[0][0].set_ylabel('$\phi_1$')
        ax[1][0].errorbar(ee_pulsed[ind_selected], As,
                          xerr=dee_pulsed[ind_selected],
                          yerr=dAs, linestyle='',
                          marker='.', color=next(color))
        ax[1][0].set_ylabel('$A_1$')
        ax[0][1].errorbar(ee_pulsed[ind_selected], phi0_2,
                          xerr=dee_pulsed[ind_selected],
                          yerr=dphases2, linestyle='',
                          marker='.',color=next(color))
        ax[0][1].set_ylabel('$\phi_2$')
        ax[1][1].errorbar(ee_pulsed[ind_selected], A2s,
                          xerr=dee_pulsed[ind_selected],
                          yerr=dA2s, linestyle='',
                          marker='.',color=next(color))
        ax[1][1].set_ylabel('$A_2$')

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=0.4, hspace=None)
        for aa in ax[1][:]:
            aa.set_xlabel('Energy [keV]')
            aa.set_xscale('log')
        if output_figure_file is not None:
            plt.savefig(output_figure_file)

    return np.array(As), np.array(dAs), np.array(phi0), np.array(dphases), \
        np.array(A2s), np.array(dA2s), np.array(phi0_2), np.array(dphases2)


def get_pulsed_fraction(e_min, e_max, pp, dpp, method_calc_rms='explicit_rms',
                        output_file=None, read_pf=False,
                        pp_back=None, dpp_back=None, n_harms=1,
                        verbose=False, level=5e-2,
                        use_poisson=True, statistics='cstat',
                        plot=False, **kwargs):
    """ this functions is made to be a wrapper of different
    methods to compute the pulsed fraction at each selected energy bin

    Args:
        e_min (_type_): _description_
        e_max (_type_): _description_
        pp (_type_): _description_
        dpp (_type_): _description_
        method_calc_rms (str, optional): _description_. Defaults to 'adaptive'.
        output_file (_type_, optional): _description_. Defaults to None.
        read_pf (bool, optional): _description_. Defaults to False.

    Returns:

        output files:
               1. the fit result
               2. the fit results to be plotted in a file
               3. Figure in pdf

    """

    if output_file is not None and read_pf is True:
        if os.path.isfile(output_file):
            ee_pulsed, dee_pulsed, pulsed_frac, \
                dpulsed_frac = np.loadtxt(output_file, unpack=True, skiprows=1)
            return ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac
        else:
            logger.warning(f'{output_file} is not present, r' +\
                           'ecomputing the pulsed fraction')

    ee_pulsed = (e_max+e_min)/2.
    dee_pulsed = (e_max-e_min)/2.
    pulsed_frac = np.zeros(len(e_min))
    dpulsed_frac = np.zeros(len(e_min))

    n_harm = np.zeros(len(e_min))
    dn_harm_min = np.zeros(len(e_min))
    dn_harm_max = np.zeros(len(e_min))

    for i in range(0, len(e_min)):
        x = pp[i, :]
        dx = dpp[i, :]
        if pp_back is not None:
            x_b = pp_back[i, :]
            dx_b = dpp_back[i, :]
        else:
            x_b = None
            dx_b = None
        if method_calc_rms == 'minmax':
            # Min/MAX
            pulsed_frac[i], dpulsed_frac[i] = \
                pulse_fraction_from_data_min_max(x, dx, background=x_b,
                                                 background_error=dx_b)
        elif method_calc_rms == 'explicit_rms':
        #RMS with fixed n_harm
            if not verbose:
                pulsed_frac[i] = pulse_fraction_from_data_rms(x,
                                                              dx,
                                                              n_harm=n_harms,
                                                              background=x_b,
                                                              background_error=dx_b,
                                                              statistics=statistics)
                dpulsed_frac[i] = get_error_from_simul(x, dx,
                                                       pulse_fraction_from_data_rms,
                                                       n_simul=1000,
                                                       n_harm=n_harms,
                                                       background=x_b,
                                                       background_error=dx_b,
                                                       use_poisson=use_poisson,
                                                       statistics=statistics,
                                                       **kwargs)
            else:
                pulsed_frac[i], n_harm[i] = pulse_fraction_from_data_rms(x,dx, n_harm=n_harms, background=x_b,
                                                                    background_error=dx_b, statistics=statistics)
                dpulsed_frac[i], dn_harm_min[i], dn_harm_max[i] = get_error_from_simul(x,dx, pulse_fraction_from_data_rms,  n_simul=1000,
                                                                n_harm=n_harms, background=x_b,
                                                                    background_error=dx_b,
                                                                    use_poisson=use_poisson, statistics=statistics, **kwargs)
        elif method_calc_rms == 'adaptive':

            if not verbose:
                pulsed_frac[i] = fft_pulsed_fraction(x, dx, level=level, n_harm_min=2, n_harm_max=n_harms,
                                                            plot=plot,
                                                            verbose=verbose, background=x_b,
                                                                    background_error=dx_b, statistics=statistics, **kwargs)

                dpulsed_frac[i] = get_error_from_simul(x,dx, fft_pulsed_fraction, level=level,
                                                            n_harm_min=2, n_harm_max=-1,
                                                                verbose=verbose,  n_simul=1000, plot=plot,
                                                                use_poisson=use_poisson, background=x_b,
                                                                    background_error=dx_b, statistics=statistics, **kwargs)
            else:
                pulsed_frac[i], n_harm[i] = fft_pulsed_fraction(x, dx, level=level, n_harm_min=2, n_harm_max=-1,
                                                            plot=plot,
                                                            verbose=verbose, background=x_b,
                                                                    background_error=dx_b, statistics=statistics)

                dpulsed_frac[i], dn_harm_min[i], dn_harm_max[i] = get_error_from_simul(x,dx, fft_pulsed_fraction, level=level,
                                                            n_harm_min=2, n_harm_max=-1,
                                                                verbose=verbose,  n_simul=1000, plot=plot,
                                                                use_poisson=use_poisson, background=x_b,
                                                                    background_error=dx_b, statistics=statistics, **kwargs)

        elif method_calc_rms == 'area':
            pulsed_frac[i] = pulsed_fraction_area(x,dx, background=x_b,
                                                                background_error=dx_b)
            dpulsed_frac[i] = get_error_from_simul(x,dx,pulsed_fraction_area, background=x_b,
                                                                background_error=dx_b, **kwargs)
        elif method_calc_rms == 'counts':
            pulsed_frac[i] = pf_rms_counts(x,dx, background=x_b,
                                                                background_error=dx_b )
            dpulsed_frac[i] = get_error_from_simul(x,dx, pf_rms_counts, n_simul=1000,
                                                            use_poisson=use_poisson, background=x_b,
                                                                background_error=dx_b, **kwargs)
        else:
            raise RuntimeError('No method is defined')

        out_str = '%d (%.1f %.1f) keV %.3f %.3f' %(i, e_min[i], e_max[i],pulsed_frac[i], dpulsed_frac[i])

        if verbose:
            out_str+=' %d %d %d' %(n_harm[i], dn_harm_min[i], dn_harm_max[i])
            #
        logger.info(out_str)

    if output_file is not None:
        with open(output_file, 'w') as ff:
            ff.write("Energy Energy_error PF PF_error\n")
            for i in range(0, len(e_min)):
                ff.write("%.2f %.2f %.4f %.4f\n" % (ee_pulsed[i], dee_pulsed[i],
                            pulsed_frac[i], dpulsed_frac[i]))
    return ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac

def elaborate_pulsed_fraction(ee_pulsed, dee_pulsed, pulsed_frac, dpulsed_frac, debug_plots=True, e1=10, e2=20, ylabel = 'PF',
                              stem='', poly_deg=[3, 3], title='', save_plot=True, e_threshold=0.3,
                              division_derivative_order=2, max_n_high_lines = 2, forced_gaussian_centroids = [],
                              forced_gaussian_amplitudes = [],
                              forced_gaussian_sigmas = [],
                              y_lim=[0,1],
                              noFe=False,
                              custom_Fe_center = None,
                              custom_Fe_sigma = None,
                              threshold_p_value=5e-2,
                              ax1=None, ax2=None,
                              **kwargs):
    """This function implements performs a fit of the pulsed fraction spectrum.
    It first interpolates the pulsed fraction with a spline to find extremes of the function.
    Then it performs a fit with a polynomial plus gaussians.
    The general idea is to split the pulsed fraction into two regions, based on the flex of the function.
    Then to fit the lower energy checking for a gaussian feature in correspondence of the iron line complex.
    Then we look for minima of the PF in the highest part and insert gussians to model features associated with
    cyclotron resonant scattering features.
    If there are too may minima, we reduce them.
    Logic is included to comply with few points.

    Args:
        ee_pulsed (numpy array): energy
        dee_pulsed (numpy array): energy error
        pulsed_frac (numpy array): pulsed fraction
        dpulsed_frac (numpy array): pulsed fraction uncertainty
        debug_plots (bool, optional): plot the derivative and the fits. Defaults to True.
        e1 (int, optional): lower energy to search the flex in this interval. Defaults to 10.
        e2 (int, optional): lower energy to search the flex in this interval. Defaults to 20.
        ylabel (str) : label of the y axis. Default 'PF', first, second for amplitude of 1st and 2nd hamonics, respectively
        Note that if you put e1>=e2, we will use only one interval.
        stem (str, optional): a string in fron of output plot names. Defaults to ''.
        poly_deg (int or list of int, optional): degree of the polynomial. Defaults to 3. If <0, it inreases the value until a p-value of
                                                at least threshold_p_value is reached
        title (str, optional): title of the plots. Defaults to ''.
        save_plot (bool, optional): if plots should be saved Defaults to True.
        e_threshold (float, optional): if energies of PF minima differ in relative terms less than this values, they are reduced.
                                       ex.: if the algorithm finds minima at 32 and 35 keV, it retains only 32.
                                       This is used also as a range for the centroid search from (1-e_treshold)*e_centroid to
                                       (1+e_treshold)*e_centroid Defaults to 0.3.
        division_derivative_order (int, optional): order of the derivative to search for the division, if 2 it searches a flex. Defaults to 2.
        max_n_high_lines (int, optional): do not use more gaussians thn this. Defaults to 2.
        forced_gaussian_centroids (list, optional): you can force the initial centroid energies with this parameter. Defaults to [].
        forced_gaussian_amplitudes (list, optional): you can force the initial amplitudes with this parameter, if the length of the list
                                                    is different from the one of forced_gaussian_centroids, it is unused. Defaults to [].
        forced_gaussian_sigmas (list, optional): you can force the initial sigmas with this parameter, if the length of the list
                                                 is different from the one of forced_gaussian_centroids, it is unused. Defaults to [].
        y_lim : limits for the plotting. Defaults to [0,1]
        noFe (False, True, 'custom'):
            defaults = False: Considers Gaussian feature with standard values for Iron line
                                E = 6.5 p/m 1, sigma = 0.2 (rangin from 0.0 to 2.0)
            True: exclude the 6.4 keV Gaussian feature
            'custom': A customized value for the Fe line can be added
                    (custom_Fe_center = [[value, min,max]], custom_Fe_center = [[value, min,max]]
        threshold_p_value : defaults to 1e-4 it is the threshold p-value above which the polynomial degree is acceptable
    Returns:
        a dictionary of results
        two fitting objects for the two ranges (the output of utils.fit_pulsed_frac). if only one is used, the second is None.
     """
    from scipy import interpolate


    if type(poly_deg) is not list:
        poly_deg = [poly_deg]

    smoothing = interpolate.UnivariateSpline(ee_pulsed, pulsed_frac, w=1./dpulsed_frac, k=3)
    fake_en = np.linspace(ee_pulsed[0], ee_pulsed[-1], 1000)
    smoothed_pulsed_frac_deriv=smoothing.derivative(1)(fake_en)
    smoothed_pulsed_frac_deriv_2=smoothing.derivative(2)(fake_en)

    def get_zeros(energy,deriv,deriv_2,selection):
        positive = deriv[selection] > 0
        ind_extreme = np.where(np.bitwise_xor(positive[1:], positive[:-1]))
        #print(energy[selection][ind_extreme])
        if deriv_2 is not None:
            ind_zeros = deriv_2[selection][ind_extreme] > 0
            return energy[selection][ind_extreme][ind_zeros]
        else:
            ind_zeros = ind_extreme
            return energy[selection][ind_zeros]

    def get_minimum(energy, deriv, selection):
        ind_min = np.argmin(deriv[selection])
        return energy[selection][ind_min]

    if debug_plots:
        fig,axes = plt.subplots(1,2,sharex=True)
        axes[0].errorbar(ee_pulsed,pulsed_frac, xerr=dee_pulsed, yerr=dpulsed_frac, linestyle='')
        axes[0].set_xlabel('Energy [keV]')
        axes[0].set_ylabel('Pulsed Fraction')
        axes[0].plot(fake_en, smoothing(fake_en))

        pulsed_frac_deriv=np.gradient(pulsed_frac, ee_pulsed)
        axes[1].plot(ee_pulsed, (pulsed_frac_deriv))
        axes[1].plot(fake_en, smoothed_pulsed_frac_deriv)
        axes[1].set_xlabel('Energy [keV]')
        axes[1].set_ylabel('Pulsed Fraction Derivative')

    ind_range1 = (fake_en >= e1) & (fake_en <=e2)
    make_double_fit = True
    if np.sum(ind_range1) <= 0:
        make_double_fit = False

    if type(noFe) == str and noFe == 'custom':
        if custom_Fe_center is None or custom_Fe_sigma is None:
            raise ValueError('If you customize the Iron line, add custom_center = [[value,min,max]] and '
                             'custom_sigma = [[value,min,max]] as arguments for the function')
        else:
            center = custom_Fe_center
            sigma = custom_Fe_sigma
            amplitude = [[0., -1., 1.]]
            n_gauss = 1
    elif noFe is True:
        center = []
        sigma = []
        amplitude = []
        n_gauss = 0
    else:
        center = [[6.5, 5.5, 7.5]]
        sigma = [[0.2, 0.0, 2.0]]
        amplitude = [[0., -1., 1.]]
        n_gauss = 1


    e_turn = 0

    #We start building the outputdictionary
    output_dict = {}


    if make_double_fit:
        if division_derivative_order == 2:
            e_turn = get_zeros(fake_en, smoothed_pulsed_frac_deriv_2, None, ind_range1)
        else:
            e_turn = get_zeros(fake_en, smoothed_pulsed_frac_deriv, smoothed_pulsed_frac_deriv_2, ind_range1)

        if len(e_turn) == 0:
            logger.info('Using the minimum derivative instead of zero in dividing regimes')
            e_turn = get_minimum(fake_en, smoothed_pulsed_frac_deriv, ind_range1)
        else:
            logger.info('Getting a zero of derivative to divide regimes')
            e_turn = e_turn[0]

        logger.info("We separate PF fit at %f keV" % e_turn)

        if debug_plots:
            axes[0].axvline(e_turn, 0, 1, color='cyan')
            axes[1].axvline(e_turn, 0, 1, color='cyan')

        ind_low = ee_pulsed <= e_turn
        ind_high = ee_pulsed > e_turn
        logger.info('We use %d points in the low-energy' % np.sum(ind_low))

    else:
        #all values
        ind_low = ee_pulsed > 0
        #no value
        ind_high = ee_pulsed < 0

        if len(forced_gaussian_centroids) > 0 and str(forced_gaussian_centroids[0]) != '':
            center += [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in forced_gaussian_centroids]
            if len(forced_gaussian_sigmas) == len(forced_gaussian_centroids) and str(forced_gaussian_sigmas[0]) != '':
                sigma += [[ee,0,2*ee] for ee in forced_gaussian_sigmas ]
            else:
                sigma = [[1+0*ee,0,5] for ee in forced_gaussian_centroids]

            if len(forced_gaussian_amplitudes) == len(forced_gaussian_centroids) and str(forced_gaussian_amplitudes[0]) != '':
                amplitude += [[ee,-4*np.abs(ee),2*np.abs(ee)] for ee in forced_gaussian_amplitudes ]
            else:
                amplitude = [[0*ee,-2,2] for ee in forced_gaussian_centroids ]
            n_gauss = len(center)



    pulsed_fit_low, deg_poly_low = fit_pulsed_frac(ee_pulsed[ind_low],dee_pulsed[ind_low],
                                        pulsed_frac[ind_low], dpulsed_frac[ind_low], n_gauss=n_gauss,
                                       center=center,
                                        sigma=sigma,
                                        amplitude=amplitude, ylabel = ylabel,
                                       degree_pol=poly_deg[0], plot_final=True, stem=stem+'low', y_lim=y_lim,
                                       threshold_p_value=threshold_p_value)

    output_dict.update({'pulsed_fit_low': pulsed_fit_low,
                        'deg_poly_low': deg_poly_low})

    if make_double_fit:

        e_cyc = get_zeros(fake_en, smoothed_pulsed_frac_deriv, smoothed_pulsed_frac_deriv_2, fake_en>e_turn)

        if len(e_cyc)>1:
            logger.info("Checking for too close Gaussians in %d elements" % len(e_cyc))
            diff_e_cyc= ( 1- e_cyc[0:-1]/e_cyc[1:] )
            ind_stay = diff_e_cyc > e_threshold
    #         print(e_cyc)
    #         print(diff_e_cyc)
    #         print(ind_stay)
            e_cyc = [e_cyc[0]] + [ee for ee in e_cyc[1:][ind_stay]]
            logger.info("Kept %d gaussians" % len(e_cyc))

        n_gauss = len(e_cyc)
        if n_gauss > 0 and max_n_high_lines > 0 and len(forced_gaussian_centroids) == 0:
            center = [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in e_cyc[0:max_n_high_lines]]
            sigma=[[1+0*ee,0,3] for ee in e_cyc]
            amplitude=[[0*ee,-2,2] for ee in e_cyc ]
        elif len(forced_gaussian_centroids) > 0:
            center = [ [ee, (1-e_threshold)*ee, (1+e_threshold)*ee] for ee in forced_gaussian_centroids]

            if len(forced_gaussian_sigmas) == len(forced_gaussian_centroids):
                sigma = [[ee,0,2*ee] for ee in forced_gaussian_sigmas ]
            else:
                sigma = [[1+0*ee,0,3] for ee in forced_gaussian_centroids]

            if len(forced_gaussian_amplitudes) == len(forced_gaussian_centroids):
                amplitude = [[ee,-2*ee,4*ee] for ee in forced_gaussian_amplitudes ]
            else:
                amplitude = [[0*ee,-2,2] for ee in forced_gaussian_centroids ]
            n_gauss = len(forced_gaussian_centroids)
        else:
            center = []
            sigma = []
            amplitude = []
            n_gauss = 0

        #print(center,sigma,amplitude)
        logger.info('We use %d points in the high-energy' % np.sum(ind_high))
        high_poly_deg = poly_deg[-1]

        if np.sum(ind_high) <= high_poly_deg + n_gauss * 3:
            logger.info("Reducing polynomial order")
            while (np.sum(ind_high) <= high_poly_deg + n_gauss * 3) and high_poly_deg >0:

                high_poly_deg -= 1

            if (np.sum(ind_high) <= high_poly_deg + n_gauss * 3):
                n_gauss = 0
                center = []
                sigma = []
                amplitude = []
                high_poly_deg=1

        logger.info('We fit an order %d polynomial in the high-energy section' % high_poly_deg)
        logger.info('We fit %d gaussians in the high-energy section' % n_gauss)

        pulsed_fit_high, deg_poly_high = fit_pulsed_frac(ee_pulsed[ind_high],dee_pulsed[ind_high],
                                            pulsed_frac[ind_high], dpulsed_frac[ind_high], n_gauss=n_gauss,
                                        center=center,
                                            sigma=sigma,
                                            amplitude=amplitude,
                                        degree_pol=high_poly_deg, plot_final=True, stem=stem+'high',
                                        y_lim=y_lim,ylabel = ylabel, threshold_p_value=threshold_p_value)
    else:
        pulsed_fit_high = None
        deg_poly_high = 0

    output_dict.update({'pulsed_fit_high': pulsed_fit_high,
                        'deg_poly_high': deg_poly_high,
                       'e_turn' : e_turn})



    global_fig = plot_pf(ee_pulsed, dee_pulsed,
            pulsed_frac, dpulsed_frac,
            e_turn, pulsed_fit_low, pulsed_fit_high,
            noFe,
            forced_gaussian_centroids,
            ylabel=ylabel, y_lim=y_lim,
            title=title, ax1=ax1, ax2=ax2)

    if save_plot:
        global_fig.savefig(stem+'pulsed_fitted.pdf')



    return output_dict


def fit_pulsed_frac(en, den, pf, dpf, stem=None, degree_pol=4, n_gauss=0, center=[],
                    sigma=[], amplitude=[],
                    plot_final=True, ylabel = 'PF', print_results=True, y_lim=[0,1.1], x_lim=[3,70], threshold_p_value=1e-4):
    '''
    this function will fit an input energy range of the pulse profile.
    the fitting function will be a simple polynomial + gaussian
    the aim is to retrieve basic gaussian parameters to be compared
    to those obtained in spectral analysis around Ecycl.
     output files: 1. the fit result
                   2. the fit results to be plotted in a file
                   3. Figure in pdf
    :param en: input energy
    :param den: input energy uncertainty
    :param pf: pulsed fraction
    :param dpf: pulsed fractio uncertainty
    :param stem: output prefix
    :param degree_pol: degree of the polynomial to fit. If <0, it inreases the value until a p-value of
                                                at least threshold_p_value is reached
    :param n_gauss: number of gaussian lines
    :param center: array of centers of gaussians [[initial_value, min, max]]
    :param sigma: array of sigmas of gaussians [[initial_value, min, max]]
    :param amplitude: array of amplitude of gaussians [[initial_value, min, max]],
                        use negative values for absorption-like
    :param plot_final: if make a final plot
    :param ylabel: ylabel for the plot (defaults to 'PF')
    :param print_results: if results should be printed out in file
    ;param threshold_p_value: defaults to 1e-4 is the threshold p-value to stop increasing the number of polynomials
    :return:
    lmfit object, degree of polynomial
    '''
    from matplotlib.pyplot import cm
    from lmfit.models import PolynomialModel, GaussianModel
    from scipy.stats import chi2

    if len(center) != n_gauss or len(sigma) != n_gauss or len (amplitude) != n_gauss:
        logger.error("You provided %d centers, %d sigmas, and %d amplitudes for %d gaussians" % (len(center),
                            len(sigma), len(amplitude), n_gauss))
        return

    col = cm.viridis(np.linspace(0, 1, 6))

    if stem is not None:
        outputfile = open(stem + '_fit_pf.out', 'w')
    else:
        stem = ''
        outputfile = open('fit_pf.out', 'w')

    if degree_pol > 0:
        threshold_p_value = 1e-100
        running_degree_pol = degree_pol
    else:
        running_degree_pol = 1

    p_value = 0
    old_p_value=0

    while p_value <= threshold_p_value and np.fabs(p_value - old_p_value) <  threshold_p_value/4 :
        poly_mod = PolynomialModel(prefix='poly_', degree=running_degree_pol)
        pars = poly_mod.guess(pf, x=en, degree=running_degree_pol)
        mod = poly_mod

        for N in range(1, n_gauss+1):
            logger.debug("%d" % N)
            logger.debug("%g" % center[N - 1][0])
            gauss = GaussianModel(prefix='g' + str(N) + '_')
            pars.update(gauss.make_params())
            pars['g' + str(N) + '_center'].set(value=center[N - 1][0], min=center[N - 1][1], max=center[N - 1][2])
            pars['g' + str(N) + '_sigma'].set(sigma[N - 1][0], min=sigma[N - 1][1], max=sigma[N - 1][2])
            pars['g' + str(N) + '_amplitude'].set(amplitude[N - 1][0], min=amplitude[N - 1][1],
                                                max=amplitude[N - 1][2])
            mod = mod + gauss



        #initialfit = mod.eval(pars, x=en)

        out = mod.fit(pf, pars, x=en, weights = 1./dpf)
        old_p_value = p_value
        p_value = 1 - chi2.cdf(x=out.chisqr, df = out.nfree)
        logger.info('poly_deg %d chi2 %f dof %d p-value %g p-value difference %g' % \
                     (running_degree_pol , out.chisqr, out.nfree, p_value, np.fabs(p_value - old_p_value)))
        running_degree_pol += 1
        if running_degree_pol > 7 or (out.ndata - out.nfree) <= 1:
            logger.info('Reached maximum polynomial degree')
            break

    bb = (pf - out.best_fit) / dpf

    comps = out.eval_components(x=en)
    logger.info(comps)

    if not plot_final:
        fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.8))
        axes[0].errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[0])
        axes[0].plot(en, out.best_fit, '-', label='best fit', color=col[2])
        axes[0].legend(loc='upper left')
        axes[0].set_xlabel('E [keV]')
        axes[0].set_ylabel(ylabel)
        axes[0].set_ylim(y_lim)
        axes[0].set_xlim(x_lim)


        axes[1].errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[0])
        for N in range(1, n_gauss+1):
            axes[1].plot(en, comps['g%d_' % N], '--', label='Gaussian %d' % N, color=col[3])
            axes[1].axvline(center[N - 1][0], 0, 1, linestyle='--', color='cyan')
        axes[1].plot(en, comps['poly_'], '--', label='Polynomial component', color=col[4])
        axes[1].legend(loc='upper left')
        axes[1].set_xlabel('E [keV]')
        axes[1].set_ylabel(ylabel)
        axes[1].set_ylim(y_lim)
        axes[1].set_xlim(x_lim)

        plt.savefig(stem + 'fit_results.pdf')

    #Is it of any use maybe to remove?
    if print_results:
        datafile = open(stem + 'model_components_fit.dat', 'w')
        datafile.write('# fit results \n')
        datafile.write('# E[0]       dE[1]       pf_bestfit[2]          poly[3]            gauss1...N [4]...[N+4] \n')
        for j in range(len(pf)):
            datafile.write(str(round(en[j], 5)).ljust(10) + str(round(den[j], 2)).ljust(10) +
                           str(round(out.best_fit[j], 5)).ljust(15) + str(round(comps['poly_'][j], 5)).ljust(15) + '\t')
            for S in range(1, n_gauss+1):
                datafile.write(str(round(comps['g' + str(S) + '_'][j], 8)).ljust(25) + '\t')
            datafile.write('\n')

        datafile.close()

    if plot_final:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6.0), sharex=True, gridspec_kw={'height_ratios': [3, 1],
                                                                              'hspace': 0.0}
                                       )
        ax1.errorbar(en, pf, xerr=den, yerr=dpf, fmt='.', color=col[4], label='data')
        ax1.plot(en, out.best_fit, '-', label='best fit', color=col[0])
        ax1.plot(en, comps['poly_'], '--', label='Polynomial', color=col[1])
        ax1.legend(loc='upper left')
        ax1.set_xscale('log')
        ax2.set_xlabel('E (keV)')
        ax1.set_ylabel(ylabel)
        ax1.set_ylim(y_lim)
        ax1.set_xlim(x_lim)
        for N in range(1, n_gauss+1):
            ax1.axvline(center[N - 1][0], 0, 1, linestyle='--', color='cyan')

        ax2.set_ylabel('Residuals')
        #ax1.set_ylim(-0.1, 1)
        ax2.errorbar(en, bb, xerr=den, yerr=1., fmt='.', color=col[2])
        ax2.axhline(y=0, color='k', linestyle='--')
        plt.savefig(stem + 'pulsed_fitted.pdf')

    logger.info(str(out.fit_report()))
    outputfile.write(out.fit_report())
    outputfile.close()

    with open(stem+'.json', 'w') as jf:
        out.params.dump(jf, cls=NpEncoder)

    return out, running_degree_pol-1 #(it is increase in the while after setting the degree)


def explore_fit_mcmc(model_fitted, pars=[], hm_steps=7000, hm_walkers=2000, hm_jump=500, plot_corner=True, print_file=True,
                     stem='', high_part=True, latex_dict = mcmc_latex_dict, title='', read=True, para_hash=''):
    '''
    this function explore the posterior parameter space obtained with a previous fit
    using mcmc
    outputs: - corner plot
             - Maximum Likelihood Estimation
             - Error @ 1,2,3 sigma


    Parameters
    ----------
    model_fitted :  lmfit.model.ModelResult
        output of the fit procedure obtained with
        the function 'fit_pulsed_frac'
    pars :  lmfit.parameter.Parameters
        parameters of the fit (if not specified, we derive them from the results)
    hm_steps : INTEGER
        how many steps: number of steps for the MCMC, default = 7000
    hm_walkers : INTEGER
        how many walkers: number of walkers for MCMC, default = 2000
    hm_jump : INTEGER
        how many first step not to consider, default = 500
    plot_corner : BOOLEAN
        if the corner_plot has to be plotted
    high_part : BOOLEAN
        if True the latex labels interpret Gaussians as E_cyc, if False as E_Fe
    latex_dict :
        a dictionary for formatting labels in latex (default is from the module)
    title :
        a title for the plot
    stem :
        the base outpt file, if == '' then no output
    read :
        if False it forces recumputation, if true, it tries to read output (experimental)
    para_hash :
        a unique hash to encode all used input parameters for output of json and fits dumps
    Returns
    -------
    explore: lmfit.minimizer.MinimizerResult (result of the minimization using emcee)
    emcee_plot: corner plot of the posterior distribution


    '''

    if int(hm_steps) == 0:
        return None, None
    from astropy.table import Table
    import json

    output_base = stem + para_hash + '_posterior'
    output_base_nohash = stem + '_posterior'

    if high_part:
        output_base += '-high'
        output_base_nohash += '-high'

    else:
        output_base += '-low'
        output_base_nohash += '-low'

    if read and os.path.isfile(output_base+'.json') and os.path.isfile(output_base+'.fits'):
        logger.warning('Experiemntal reconstruction of object, it assumes the same call as for construction')
        with open(output_base+'.json') as jf:
            json_string = jf.read()
        import lmfit
        explore = lmfit.minimizer.MinimizerResult()
        flatchain = Table.read(output_base+'.fits').to_pandas()
        # print(flatchain.shape)
        n_pars = flatchain.shape[1]
        new_array = np.zeros([int(flatchain.shape[0]/hm_walkers), hm_walkers, n_pars])
        for i, ff in enumerate(flatchain.columns):
            new_array[:,:, i] = flatchain[ff].values.reshape(new_array.shape[0:2])
        # print(new_array.shape)
        explore.nvarys = n_pars
        explore.chain = new_array
        explore.params = lmfit.Parameters()
        explore.params.loads(json_string)
        tmp_var_names = [pp for pp in explore.params if '_fwhm' not in pp and '_height' not in pp]
        var_names = [tmp_var_names[i] for i in range(n_pars)]
        # print(var_names, len(var_names))
        explore.var_names = var_names
        #TODO put it in json output and reconstruct

        json_dict = json.loads(json_string)
        if 'extra' in json_dict:
            explore.chisqr = json_dict['extra']['chisqr']
            explore.nfree = json_dict['extra']['nfree']
        else:
            logger.warning('Inserting dummy chisqr and nfree')
            explore.chisqr = -1
            explore.nfree = -1
    else:
        read = False

    if hm_steps <= hm_jump :
        logger.error(" You almost did it!. However, the number of steps must be higher than the jumped ones:"
                     "hm_steps > hm_jump")

    if pars ==[]:
        pars = model_fitted.params.copy()

    if read is False:
        explore = model_fitted.emcee(params=pars, steps=hm_steps, nwalkers=hm_walkers,
                                is_weighted=True, burn=hm_jump)

        if explore.success is False:
            raise RuntimeError('lmfit MCMC failed')

        var_names = explore.var_names

        highest_prob = np.argmax(explore.lnprob)
        hp_loc = np.unravel_index(highest_prob, explore.lnprob.shape)
        mle_soln = explore.chain[hp_loc]

        pars2 = {}
        for el in pars.keys():
            if (pars[str(el)]).expr is None:
                pars2[str(el)] = pars[str(el)]

        for i, par in enumerate(pars2):
            pars2[par].value = mle_soln[i]

        fmt = '{:5s} {:11.5f} {:11.5f} {:11.5f}'.format

        logger.info('\nMaximum Likelihood Estimation from emcee ')
        logger.info('-------------------------------------------------')
        logger.info('Parameter MLE Value Median Value Uncertainty')

        for name, param in pars2.items():
            logger.info(fmt(name, param.value, explore.params[name].value, explore.params[name].stderr))

        logger.info('\Error estimates from emcee:')
        logger.info('------------------------------------------------------')
        logger.info('Parameter -3sigma -2sigma -1sigma median +1sigma +2sigma +3sigma')

        if print_file:

            o_f_emcee = open(output_base + '.out', 'w')

            o_f_emcee.write('# Maximum Likelihood Estimation from emcee \n#Parameter MLE Value Median Value Uncertainty \n')
            for name, param in pars2.items():
                o_f_emcee.write(fmt(name, param.value, explore.params[name].value, explore.params[name].stderr) + '\n')
            o_f_emcee.write(
                '#\Error estimates from emcee: \n#Parameter -3sigma -2sigma -1sigma median +1sigma +2sigma +3sigma \n')

            for name in pars2.keys():
                quantiles = np.percentile(explore.flatchain[name], [0.135, 2.275, 15.865, 50, 84.135, 97.725, 99.865])
                median = quantiles[3]
                err_m3 = quantiles[0] - median
                err_m2 = quantiles[1] - median
                err_m1 = quantiles[2] - median
                err_p1 = quantiles[4] - median
                err_p2 = quantiles[5] - median
                err_p3 = quantiles[6] - median
                fmt = '{:5s} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}'.format
                logger.info(fmt(name, err_m3, err_m2, err_m1, median, err_p1, err_p2, err_p3))
                o_f_emcee.write(fmt(name, err_m3, err_m2, err_m1, median, err_p1, err_p2, err_p3) + '\n')

            o_f_emcee.close()


        flatchain_fits= Table.from_pandas(explore.flatchain)
        if stem != '':
            json_dump_dict = json.loads(explore.params.dumps(cls=NpEncoder))
            json_dump_dict.update({'extra': {'chisqr': explore.chisqr,
                                             'nfree': explore.nfree}})
            json_str = json.dumps(json_dump_dict, cls=NpEncoder)
            with open(output_base+'.json', 'w') as jf:
               jf.write(json_str)
            flatchain_fits.write(output_base+ '.fits', overwrite=True)

    if plot_corner:
        import corner
        labels = []
        for kk in var_names:
            try:
                if high_part:
                    labels.append(latex_dict[kk.replace('g','gg')] )
                else:
                    labels.append(latex_dict[kk])
            except:
                logger.info('%s not in the latex dictionary' % kk)
                labels.append(kk)

        emcee_plot = corner.corner(explore.flatchain, labels=labels, show_titles=True,
                                   plot_datapoints=False,figsize = (16,16), title_fmt='.1e')
        if title != '':
            axes = emcee_plot.get_axes()
            index_title = int(np.floor(np.sqrt(len(axes))/2.))
            axes[index_title].set_title(title)
        if stem != '':
            emcee_plot.savefig(output_base_nohash+'_corner.pdf')

    else:
        emcee_plot = None

    return explore, emcee_plot


def error_from_simul_rms(counts, counts_err, n_simul=100, n_harm=3, **kwargs):

    return get_error_from_simul(counts, counts_err, 
                                pulse_fraction_from_data_rms,
                                n_simul=n_simul, n_harms=n_harm, **kwargs)


def get_error_from_simul(counts, counts_err, method, n_simul=100, 
                         use_poisson=True, background=None,
                         background_error=None, 
                         trimmed_limits=default_trimmed_limit, **kwargs):
    '''
    :param counts: vector of input data
    :param counts_err: vector of input data errors
    :param method: a function with the method to compute the quantity
    :param n_simul: number of simulations
    ;param background: vector of background values
    ;param background_error: vector of background errors
    :param kwargs: additional arguments to the function to be computed
    :return:
    '''

    simul_rms = []
    simul_harm = []
    fp_back = background
    fp_back_error = background_error

    if use_poisson:
        logger.debug('We use Poissonian statistics for simulation')
        to_simulate = counts
        if np.sum(counts==0):
            to_simulate[counts==0] = np.min(counts[counts>0])/2.0
            logger.warning("WARNING: some counts are zero in simulation, we use %f instead" % (np.min(counts[counts>0])/2.0) )
            #print(counts)
    else:
        logger.debug('We use Gaussian statistics for simulation')


    for i in range(n_simul):
        if use_poisson:
            fp = random.poisson(to_simulate)
            if background is not None:
                fp_back = random.poisson(np.ones(len(background))*background.mean())
                fp_back_error = np.sqrt(fp_back)
        else:
            fp = random.normal(counts, np.max( [np.ones(len(counts_err)), counts_err], axis=0))
            if background is not None and background_error is not None:
                fp_back = random.normal(background, np.max( [np.ones(len(background_error)), background_error], axis=0))
        if 'verbose' in kwargs and kwargs['verbose']:
            x,y = method(fp, counts_err, background=fp_back, background_error=fp_back_error, **kwargs)
            simul_rms.append(x)
            simul_harm.append(y)
        else:
            simul_rms.append(method(fp, counts_err, background=fp_back, background_error=fp_back_error, **kwargs))

    if 'plot' in kwargs and kwargs['plot']:
        fig, axes = plt.subplots(1,2)
        axes[0].hist(simul_rms, bins=10)
        axes[1].hist(simul_harm, bins=10)

    if 'verbose' in kwargs and kwargs['verbose']:
        return corrected_trimmed_std( (simul_rms), axis=0, limits=(trimmed_limits,trimmed_limits), relative=True), np.max(simul_harm), np.min(simul_harm)
    else:
        return corrected_trimmed_std( (simul_rms), axis=0, limits=(trimmed_limits,trimmed_limits), relative=True)

def get_n_harm(x, dx=None, level=0.1, n_harm_min=2, n_harm_max=-1, statistics='cstat'):
    """This returns the number of harmonics necessary to describe the signal in x with uncertainty dx
    at minimal Significance level (=1- confidence level) (note that for lower values, you get lower harmonics)
    Available statistics are: cstat, chi2, archibald.
    cstat is based on Kaastra et al (2017) https://doi.org/10.1051/0004-6361/201629319
    chi2 is a standard implementation
    archibald is from Archibald et al. (2014), appendix A (inaccurate !)

    Args:
        x (numpy array): signal
        dx (numpy array): signal uncertainty, necesssary only for chi2
        level (float, optional): minimum confidence . Defaults to 0.1.
        n_harm_min (int, optional): minimum number of harmonics. Defaults to 2.
        n_harm_max (int, optional): maximum number of harmonics. Defaults to -1.
        statistics (str, optional): methods, see above. Defaults to 'cstat'.

    Returns:
        int: number of necessary harmonics
    """

    if statistics == 'chi2' and dx is None:
        raise Exception('For chi2 statistics, you need to provide uncertaintis')

    from scipy.stats import chi2
    from scipy.stats import norm
    import cashstatistic as cstat

    # Quantile (the cumulative probability)
    q = 1 - (level / 2 )
    # Critical z-score, calculated using the percent-point function (aka the
    # quantile function) of the normal distribution
    z_star = norm.ppf(q)
    n = len(x)
    if n_harm_max < n_harm_min or n_harm_max+1 > n/2:
        logger.debug('n_harm max = %d' % n_harm_max)
        n_harm_max = n / 2 - 1

    n = len(x)
    fft = np.fft.fft(x)
    old_chi2_sf = -1.0
    #old_cstat = 1e10
    for n_harm in range(int(n_harm_min), int(n_harm_max)+1):
        mask = np.ones(n, dtype=np.cdouble)
        mask[n_harm:-(n_harm - 1)] = 0 + 0j
        ifft = np.fft.ifft(fft * mask)
        y = np.real(ifft)
        #Necessary to avoid infinite for zero uncertaity
        ind = dx > 0
        #print(ind)
        if statistics == 'chi2':
            chi2_val = np.sum(((x[ind] - y[ind]) / dx[ind]) ** 2)
            dof = max(1, n - (1 + 2 * (n_harm - 1)))
            chi2_sf = chi2.sf(chi2_val, dof)
            logger.debug('%d %f %d %f %f' % (n_harm, chi2_val, dof,  chi2_sf, old_chi2_sf))

            #Sometimes, we do ot reach the required level, but we cannot describe the pulse significantly better,
            # so we stop in any case (condition chi2_sf < old_chi2_sf)
            if chi2_sf > level or (chi2_sf < old_chi2_sf and chi2_sf > level/100.):
                logger.debug('chi2_sf = %e (level is %.5f) old_chi2_sf = %e' % (chi2_sf, level, old_chi2_sf))
                break
            old_chi2_sf = chi2_sf
            if n_harm == n_harm_max:
                logger.debug('maximum number of harmonics reached')
        elif statistics=='cstat':
            mask = (y>0) & (x>=0) # the second part should never be needed
            cstat_val = cstat.cash_mod(y[mask],x[mask]).sum()
            c_e, c_v = cstat.cash_mod_expectations(y[mask])
            tmp1 = np.sum(c_e)
            tmp2 = z_star * np.sqrt(np.sum(c_v))
            logger.debug("%d %e %e %e" %(n_harm, cstat_val, tmp1, tmp2 ))
            if  cstat_val < tmp1 + tmp2:
                # These conditions are harmful
                # or cstat_val > old_cstat: #cstat_val > tmp1 - tmp2 and
                logger.debug('cstat = %e (expected is %e +/- %e) ' % (cstat_val, tmp1, tmp2))
                break
            #old_cstat = cstat_val
            if n_harm == n_harm_max:
                logger.debug('maximum number of harmonics reached')
        elif statistics == 'archibald':
            a,b,sigma_a,sigma_b = compute_a_b_sigma_a_sigma_b(x, dx, int(n_harm_max))
            m4 = 4*np.arange(1,n_harm_max+1)
            cumulative_sum = np.zeros(int(n_harm_max))
            for k in range(1,int(n_harm_max)):
                cumulative_sum[k] = np.sum( (a[0:k]/sigma_a[0:k])**2 + (b[0:k]/sigma_b[0:k])**2)
            #print(cumulative_sum)
            n_harm = np.argmax(cumulative_sum - m4) + 1
            #print("We stop at %d harmonics" % max_harm)
        else:
            raise Exception('Statistics %s is not implemented' % statistics)

    logger.debug("Used %d harmonics for pulse description" % n_harm)

    return n_harm

def fft_pulsed_fraction(x, dx, level=0.1, n_harm_min=2, n_harm_max=-1, plot=False, verbose=False, label='',
                        background=None, background_error=None, statistics='cstat'):
    '''
    Computes the pulsed fraction using an FFT. It stops as soon as the pulse is described at better than level
    :param x: pulse profile
    :param dx: pulse profile uncertainty
    :param level: minimum confidence level to stop number of harmonics (default 0.1, lower values give less harmonics)
    :param n_harm_min: minimum number of harmonics to use (default 2)
    :param n_harm_max: maximum number of harmonics to use (default -1 takes the size of pulse profile)
    :param plot: plot the pulse profile
    :param lavel: to save the plot with name "rms_`label`.pdf", if label=='' it does not save the plot
    ;parma verbose (bool): if true it returns both pulsed_frac, n_harm, if false just the pulsed_frac
    ;param background the vector of the background
    ;param backgroun_error the uncertainty vector of the background
    ;param statistics : the method to compute the optimal number of harmonics (chi2, cstat, archibald) de cstat, see the function get_n_harm
    :return: pulsed fraction (float)
    '''

    from matplotlib import cm
    n = len(x)
    n_harm = get_n_harm(x, dx, level=level, n_harm_min=n_harm_min, n_harm_max=n_harm_max, statistics=statistics)
    fft = np.fft.fft(x)
    a = np.absolute(fft) / n
    if background is not None and background_error is not None:
        a[0] = subtract_background(a[0], background,background_error)

    pulsed_frac = np.sqrt(np.sum(a[1:n_harm] ** 2) + np.sum(a[-n_harm + 1:] ** 2)) / a[0]
    col = cm.viridis(np.linspace(0, 1,int(n_harm)+1))
    if plot:
        import matplotlib.pyplot as plt
        f = np.linspace(0, 1, n)
        #plt.errorbar(f, x, yerr=dx, fmt='.', label='data %s' % label, color = col[n_harm])
        #plt.plot(f, y, label='%d harmonics' % n_harm, linestyle='--', color = col[n_harm])
        plt.errorbar(f, x, yerr=dx, fmt='.', color=col[n_harm])
        fft = np.fft.fft(x)
        mask = np.ones(n, dtype=np.cdouble)
        mask[n_harm:-(n_harm - 1)] = 0 + 0j
        ifft = np.fft.ifft(fft * mask)
        y = np.real(ifft)
        plt.plot(f, y, linestyle='--', color=col[n_harm])
        #plt.text(0.4,120,str(n_harm)+'  harmonics',color = col[n_harm])
        plt.xlabel('Phase')
        plt.ylabel('Counts')
        #plt.legend()
        if label != '':
            plt.savefig('rms_%s.pdf' % label)
    if verbose:
        return pulsed_frac, n_harm
    else:
        return pulsed_frac

def pf_rms_counts(x,dx, background=None, background_error=None):
    '''
    param x : pulse profile
    param dx: error on pulse profile
    return: pf_counts
    '''
    avg_cts=np.mean(x)
    dev = (np.array(x)-avg_cts)**2
    devi = np.fabs(np.sum(dev-np.array(dx)**2))
    if background is not None and background_error is not None:
        avg_cts = subtract_background(avg_cts, background, background_error)
    if avg_cts != 0:
        pf_rms_cts = (1./ avg_cts) * np.sqrt( devi/len(x) )
    else:
        pf_rms_cts = 0
    return pf_rms_cts


def pulse_fraction_from_data_min_max(x,dx, background=None, background_error=None):

    i_min = np.argmin(x)
    i_max = np.argmax(x)
    x_min = x[i_min]
    x_max = x[i_max]
    dx_min = dx[i_min]
    dx_max = dx[i_max]
    if background is not None:
        x_min -= background[i_min]
        x_max -= background[i_max]
        dx_min = np.sqrt(background_error[i_min] **2 + dx_min **2)
        dx_max = np.sqrt(background_error[i_max] **2 + dx_max **2)

    tmp1 = (x_min + x_max)
    pulsed_frac = (x_max - x_min) / tmp1
    dpulsed_frac = 2*np.sqrt((x_max/tmp1**2)**2 * dx_max**2 + (x_min/tmp1**2)**2 * dx_min**2)

    return pulsed_frac, dpulsed_frac
import matplotlib.cm


def get_fourier_coeff(pulse, n=2):
    """returns the first n Fourier coefficients in polar form

    Args:
        pulse (array): the pulse profile
        n (int, optional): number of harmonics. Defaults to 2.

    Raises:
        IndexError: if n is larger than len(pulse/2)

    Returns:
       a, phi: numpy arrays: amplitudes and phases of the first n Fourier coefficients
    """

    # phi = np.linspace(0, 2 * np.pi, len(pulse))
    # i_c = np.sum(np.cos(phi) * pulse) / np.pi
    # i_s = np.sum(np.sin(phi) * pulse) / np.pi
    # i_c2 = np.sum(np.cos(2 * phi) * pulse) / np.pi
    # i_s2 = np.sum(np.sin(2 * phi) * pulse) / np.pi

    # phi0 = np.arctan2(i_s, i_c) / 2 / np.pi
    # phi0_2 = np.arctan2(i_s2, i_c2) / 2 / np.pi
    # a = np.sqrt(i_c * i_c + i_s * i_s) / len(pulse) / np.mean(pulse)
    # a2 = np.sqrt(i_c2 * i_c2 + i_s2 * i_s2) / len(pulse) / np.mean(pulse)

    ff = np.fft.rfft(pulse)
    if n>len(pulse)/2:
        raise IndexError('get_fourier_coeff: you asked for too many coefficients %d' %n )

    a = np.abs(ff[1:n+1])/ff[0].real
    phi = np.angle(ff[1:n+1])/2/np.pi
    return a, phi

def get_fourier_coeff_error( counts, counts_err, n_simul=1000, use_poisson=False, n=2, debug=False, margin=0.1, 
                            trimmed_limits=default_trimmed_limit):
    """ge uncertainty on Fourir coefficients

    Args:
        counts (numpy array): the counts
        counts_err (numpy array): the count encertainties
        n_simul (int, optional): how many bootstra simulation. Defaults to 1000.
        use_poisson (bool, optional): Use Poisson statistics. Defaults to False.
        n (int, optional): how many harmnonics. Defaults to 2.
        debug (bool, optional): If making debug plots. Defaults to False.
        margin (float, optional): option for the phase alignement, see phase_align. Defaults to 0.1.
	trimmed_limits: when computing a trimmed standard deviation, this value (in percentage) removes both the highest and the lowest values from the simulated sample. Default is 0.05

    Returns:
        two numpy arrays: uncertainties on amplitudes and phases
    """
    sim_a = []
    sim_phi = []

    for i in range(n_simul):
        if use_poisson:
            fp = random.poisson(counts)
        else:
            fp = random.normal(counts, counts_err)
        a , phi = get_fourier_coeff(fp, n=n)
        sim_phi.append(phi)
        sim_a.append(a)
    err_a = np.zeros(n)
    err_phi = np.zeros(n)
    for i in range(n):
        y = np.array([x[i] for x in sim_a ])
        err_a[i] = corrected_trimmed_std( (y), axis=0, limits=(trimmed_limits,trimmed_limits), relative=True)
        y = np.array([x[i] for x in sim_phi ])
        y = align_phases(y, debug=debug, margin=margin)
        err_phi[i] = corrected_trimmed_std( (y), axis=0, limits=(trimmed_limits,trimmed_limits), relative=True)

    return err_a, err_phi

def align_phases(y, nbins=20, debug=False, distance_factor=2, margin=0.5, label=None):
    """align_phases: tries to align phases by building an histogram of phases.
    If only one peak is found, it is considered as a phae shiter only if it is
    - in 0-margin(0.1) phases higher than 0.1+margin are shifted by -1
    - in (1-margin)(0.9)-1. phases lower than 0.9-margin are shifted by +1

    If more than one peak in the interval 0-margin(0.1) or (1-margin)(0.9)-1.0 are found, the higher phases are
    shifted by -1 (these peaks are often artifact of the algorithm)

    Args:
        y (numpy array): the phases to be aligned (in 0.-1.0 interval)
        nbins (int, optional): number of bins of the histogram to be built. Defaults to 20.
        debug (bool, optional): if True makes debug plots. Defaults to False.
        distance_factor (float, optional): if peaks are closer than 1/distace_factor times the maximum span, they are
                                            rejected. Defaults to 1.5.
        margin (float, optional): . Defaults to 0.1.
        label (str, optional): a label of the debug plot (e.g. the energy). Defaults to None.

    Returns:
        numpy array: the aligned phases
    """
    hist,bins = np.histogram(y, bins=nbins)
    from scipy.signal import find_peaks
    peaks, properties = find_peaks(np.concatenate(([np.min(hist)],hist, [np.min(hist)])),
                          distance=nbins/distance_factor, prominence=0)
    peaks-=1
    if(debug):
        fig, ax = plt.subplots()
        ax.bar(bins[:-1], hist, width=np.diff(bins), edgecolor="blue", align="edge")
        for ppp in peaks:
            ax.axvline(bins[ppp+1], color='red')
        if label is not None:
            ax.set_title(label)

    out_method = logger.debug
    if debug:
        out_method = logger.info

    out_method(label)
    out_method(hist)
    out_method(bins)
    out_method('Peaks :')
    out_method(peaks)
    out_method(properties['prominences'])

    if (len(peaks) == 2):
        ind_division = int((peaks[0]+peaks[1])/2)
        if (peaks[0] > margin*nbins and peaks[0] < (1.-margin)*nbins ) or \
        (peaks[1] > margin*nbins and peaks[1] < (1.-margin)*nbins ) or \
        np.fabs(bins[peaks[1]] - bins[peaks[0]]) < 1./distance_factor:
            out_method("%s %s %s %f", (peaks[0] > margin*nbins and peaks[0] < (1.-margin)*nbins ), \
                       (peaks[1] > margin*nbins and peaks[1] < (1.-margin)*nbins ), \
                        np.fabs(bins[peaks[1]] - bins[peaks[0]]) < 1./distance_factor,
                        np.fabs(bins[peaks[1]] - bins[peaks[0]]))
            out_method("%f %f", margin*nbins,(1-margin)*nbins)
            out_method("No phase shift for two peaks")

        else:
            phase_division = bins[ind_division]
            out_method("%f %f", margin*nbins,(1-margin)*nbins)
            out_method("two peaks, phase_Division %f" % phase_division)
            y[y>phase_division]-=1.
    elif len(peaks) == 1:
        if peaks[0] < margin*nbins:
            phase_division = bins[int((0.9-margin)*nbins)]
            out_method("Phase_division minus %f"  % phase_division)
            out_method(np.sum(y>phase_division))
            y[y>phase_division]-=1
        if peaks[0]>(1-margin)*nbins:
            phase_division = bins[int((0.1+margin)*nbins)]
            out_method("Phase_division plus %f " % phase_division)
            out_method(np.sum(y>phase_division))
            y[y<phase_division]+=1

    return y

def write_orbit_file_from_gbm_page(url, file_name='orbit.dat',
                                   orbital_parameters = ['axsin', 'Eccentricity', 'periastron',
                                                         'T<sub>', 'Orbital Period', 'Period Deriv.']):
    '''
    It writes a file to be used in timingsuite for the orbit starting from the GBM page
    This is tested just for Cen X-3 at the moment and it is very fragile

    :param url: The url of the GBM page of the source
        (e.g. 'https://gammaray.nsstc.nasa.gov/gbm/science/pulsars/lightcurves/cenx3.html')
    :param file_name: the name of output file default 'orbit.dat'
    :param orbital_parameters the orbital parameters to be extracted from the table
        default: ['axsin', 'Eccentricity', 'periastron',
                 'T<sub>', 'Orbital Period', 'Period Deriv.']
    :return: file_name or None
    '''
    import requests
    from bs4 import BeautifulSoup
    from astropy.time import Time

    #Parses the table with a particular argument (fragile)
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    orbit_table = soup.find('table', attrs={'border': 2})
    if orbit_table is None:
        logger.warning('Could not find at table in the page %s no orbit file written' % url)
        return None
    trs = orbit_table.find_all('tr')

    #removes the first row as it contains the table title
    trs[0].extract()

    #Find numbers (https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string)
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)

    #for each parmeter it extracts the value as string
    orbit = {}
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) < 2:
            continue
        for k in orbital_parameters:
            if k.lower() in str(tds[0]).lower():
                orbit.update({k: rx.findall(str(tds[1]))[0]})

    if orbital_parameters[0] not in orbit:
        logger.warning('Not able to retrieve the orbital parameters as %s could not be read' % orbital_parameters[0])
        return None
    # it writes the orbit file
    logger.info('Writing the following orbit parameters')
    with open(file_name, 'w') as ff:
        for kk in orbital_parameters:
            if 'T' in kk:
                t_90 = Time(orbit[kk], format='jd')
                # The orbit file contains the longitude of periastron or the lower conjunction
                if float(orbit['Eccentricity']) >= 0.:
                    print('Special eccentricity')
                    ff.write('%f\n' % (t_90.mjd + (float(orbit['periastron']) - 90.)/360. *\
                                       float(orbit['Orbital Period'])))
                else:
                    print('Non Special eccentricity')
                    ff.write('%f\n' % (t_90.mjd - 0.25 * float(orbit['Orbital Period'])))
            else:
                ff.write(orbit[kk] + '\n')
            logger.info('%s %s' % (kk , orbit[kk]))
    return file_name

def get_cross_correlation(pp, plot=False, n_to_fit = 3):
    """makes the cross correlation and lags of a matrix by fitting a Gaussian plus constant to the peak of the
    correlation vector

    Args:
        pp (numpy array): the pulse profile from the energy or the time-phase matrix
        plot (bool, optional): if making debug plots. Defaults to False.
        n_to_fit (int, optional): number of bins to use for the fit on each side of the peak. Defaults to 3.

    Returns:
        numpy arrays: lag, correlation
    """

    from lmfit.models import PolynomialModel, GaussianModel
    poly_mod = PolynomialModel(prefix='poly_', degree=0)
    gauss = GaussianModel(prefix='g'  + '_')

    n_pulse=pp.shape[1]
    if n_to_fit > n_pulse/3:
        logger.warning('The pulse has size %s and you try to use %d points' %(n_pulse, 2*n_to_fit+1))

    correlation = []
    lag = []
    for i in range(pp.shape[0]):

        x = (pp[i, :] - np.mean(pp[i, :])) / np.std(pp[i, :])
        y = np.sum(pp[0:i, :], 0) + np.sum(pp[i + 1:, :], 0)
        y = (y - np.mean(y)) / np.std(y)
        corr = np.correlate(np.tile(x, 2), y) / len(x)

        i_max = np.argmax(corr)

        if i_max - n_to_fit >= 0 and i_max + n_to_fit <= len(x) :
            to_fit =  corr[i_max-n_to_fit:i_max+n_to_fit+1]
        elif i_max - n_to_fit < 0:
            logger.debug('First')
            to_fit = np.concatenate([corr[i_max-n_to_fit-1:-1], corr[0:i_max+n_to_fit+1]])
        else:
            logger.debug('Last !')
            to_fit = np.concatenate([corr[i_max-n_to_fit:], corr[1:i_max+n_to_fit-len(x)+1]])
        logger.debug("Check vector %f %f " %( corr[0], corr[-1]) )

        x_to_fit = np.arange(i_max-n_to_fit,i_max+n_to_fit+1, dtype=float)

        #for aa,bb in zip(x_to_fit, to_fit):
        #    print(aa,bb)

        pars = poly_mod.guess(to_fit, x=x_to_fit, degree=0)
        mod = poly_mod

        pars.update(gauss.make_params())
        pars['g' +  '_center'].set(value=float(i_max), min=i_max-n_to_fit, max=i_max+n_to_fit)
        pars['g' +  '_sigma'].set(value=1., min=0, max=n_to_fit)
        pars['g' +  '_amplitude'].set(value=np.max(to_fit), min=0.0, max=2*np.max(to_fit))
        mod = mod + gauss

        out = mod.fit(to_fit, pars, x=x_to_fit)

        correlation.append(np.max(out.eval(x=np.linspace(x_to_fit[0], x_to_fit[-1], 100))))
        lag.append(out.best_values['g' +  '_center'])

        if plot:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(6, 6*(5**.5 - 1)/2.))
            plt.subplot(1, 2, 1)
            plt.plot(x_to_fit, to_fit, label='X-corr values', color='blue', marker='o', linestyle='')
            plt.plot(np.linspace(x_to_fit[0], x_to_fit[-1],100),
                                 out.eval(x=np.linspace(x_to_fit[0], x_to_fit[-1], 100))
                                 , label='X-corr fit', color='orange')

            plt.title('correlation')
            plt.axvline(lag[-1])
            plt.axhline(correlation[-1])
            plt.xlabel('Phase bin')
            plt.subplot(1, 2, 2)
            plt.plot(x, label='Pulse', color='blue')
            plt.plot(y, linestyle='--', label='Average', color='orange')
            plt.title('Pulse and average')
            plt.xlabel('Phase bin')
            plt.legend()

    lag = np.array(lag) / n_pulse

    return lag, np.array(correlation)

def get_cross_correlation_with_error(pp, dpp, ee_pulsed=[], dee_pulsed=[], n_simul=100,
			    trimlowlimit=default_trimmed_limit, trimhighlimit=default_trimmed_limit,
                            use_poisson=False, n_to_fit=3, debug_plot=False, stem=None, title='',
                            margin=0.1, debug_indexes=[], distance_factor=1.5,
                            read=False, output_file=None):
    """Makes the cross correlation of each pulse in the matrix with the average of the rest of the matrix

    Args:
        pp (numpy array): pulse profile from the energy-phase matrix
        dpp (numpy array): pulse profile errors from the energy-phase matrix erro
        ee_pulsed (list, optional): energy scale (only for plotting). Defaults to [].
        dee_pulsed (list, optional): energy scale uncertainty (only for plotting). Defaults to [].
        n_simul (int, optional): number of simulations to compute the error. Default is 100.
        trimlowlimit (float,optional): low limit for computing trimmed standard deviation. Default is 0.1.
	trimhighlimit (float,optional): high limit for computing trimmed standard deviation. Default is 0.1.
	use_poisson (bool, optional): If using Poisson error. Default is False.
        n_to_fit (int, optional): number of bins to fit the peak on each side of the maximum cross correlation. Defaults to 3.
        debug_plot (bool, optional): if making debug plots for correlation. Defaults to False.
        stem (_type_, optional): If not nome, it saves the plot with this prefix adding _lag_correlation.png. Defaults to None.
        title (str, optional): Title of the plot. Defaults to ''.
        margin (float, optional): parameter to realign the phases, see the align_phases function.
        distance_factor (float, optional): parameter to realign phases, see align_phases
        debug_indexes (list, ptional): indexes to perform debug output for phase_align. Defaults to [].

    Raises:
        ValueError: Value Error if the energy scale does not match the matrix when plotting

    Returns:
        numpy arrays: lags, lag_errors, correlations, correlation_errors
    """

    if output_file is not None and read is True:
        if os.path.isfile(output_file):
            with open(output_file) as ff:
                first_line = ff.readline()
            if first_line.startswith('lag'):
                lags, lag_errors, correlations, correlation_errors =  \
                    np.loadtxt(output_file, unpack=True, skiprows=1)
            else:
                _,_, lags, lag_errors, correlations, correlation_errors =  \
                    np.loadtxt(output_file, unpack=True, skiprows=1)
            return lags, lag_errors, correlations, correlation_errors
        else:
            logger.warning(f'{output_file} is not a file, recomputing lags')


    lags, correlations = get_cross_correlation(pp, n_to_fit=n_to_fit, plot=debug_plot)

    fake_lags = np.empty([n_simul, pp.shape[0]], dtype=float)
    fake_corrs = np.empty([n_simul, pp.shape[0]], dtype=float)

    for i in range(n_simul):
        if use_poisson:
            fake_pp = random.poisson(pp)
        else:
            fake_pp = random.normal(pp, dpp)
        debug = False
        if i in debug_indexes:
            debug=True
        fake_lags[i, :], fake_corrs[i, :] = get_cross_correlation(fake_pp, n_to_fit=n_to_fit, plot= (debug_plot & debug))


    for i in range(fake_lags.shape[1]):
        debug = False
        if i in debug_indexes:
            debug=True
        fake_lags[:,i] = align_phases(fake_lags[:,i], debug=debug, label='%.1f kev' % (ee_pulsed[i]), margin=margin,
                                      distance_factor=distance_factor )


    lag_errors = corrected_trimmed_std( (fake_lags), axis=0, limits=(trimlowlimit,trimhighlimit), relative=True)
    lag_checks = trimmed_mean(( fake_lags), axis=0, limits=(trimlowlimit,trimhighlimit), relative=True)
    correlation_errors = corrected_trimmed_std(  (fake_corrs), axis=0, limits=(trimlowlimit,trimhighlimit), relative=True)

    lags[lags>0.5] -= 1.0
    lag_checks[lag_checks>0.5] -= 1.0

    lags[lags<-0.5] += 1.0
    lag_checks[lag_checks<-0.5] += 1.0

    if output_file is not None:
        with open(output_file, 'w') as ff:
            ff.write('ee dee lag lag_error correlation correlation_error\n')
            for ee, dee, x, y, z, t in zip(ee_pulsed, dee_pulsed, lags, lag_errors, correlations, correlation_errors):
                ff.write('%e %e %e %e %e %e\n' % (ee, dee, x,y,z,t) )

    if debug_plot:
        for i in range(fake_lags.shape[1]):
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 8))
            ax1.hist(fake_lags[:,i], bins=int(n_simul/5))
            ax1.set_xlabel('Lags')
            ax1.set_title('%.1f keV' % ee_pulsed[i])
            ax2.hist(fake_corrs[:,i], bins=int(n_simul/5))
            ax1.set_ylabel('Correlations')


    if stem is not None:
        if len(ee_pulsed) != len(lags):

            raise ValueError('You should provide energy vectors with size %d to plot, but was %d' % \
                             (len(lags), len(ee_pulsed)))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4.5, 7), sharex=True, gridspec_kw={'height_ratios': [1, 1],
                                                                              'hspace': 0.0, 'right':0.99, 'left':0.2})

        cc = iter(plt.cm.viridis(np.linspace(0, 1, 5)))
        ax1.errorbar(ee_pulsed, correlations, xerr=dee_pulsed, yerr=correlation_errors, marker='.', linestyle='',color = next(cc))
        ax1.set_title(title)
        ax1.set_ylabel('Correlation')
        ax2.set_xscale('log')
        ax1.set_xscale('log')
        ax2.errorbar(ee_pulsed, lags, xerr=dee_pulsed, yerr=lag_errors, marker='.', linestyle='',color = next(cc))
        if debug_plot:
            ax2.scatter(ee_pulsed, lag_checks, marker='o', color='green')

        ax2.set_ylabel('Lag (phase units)')
        ax2.set_xlabel('Energy (keV)')
        fig.savefig(stem+'_lag_correlation.png' )

    return lags, lag_errors, correlations, correlation_errors


def retrieve_nh(srcname):
    '''

    get Nh/1.0e22 to be used in spectral fitting or whatever
    taken from HEASARC
    inputs:
    par: srcname, as in SINBAD
    output:
    Nh/1.0e22
    '''
    import requests
    from bs4 import BeautifulSoup
    import string
    ra_src, dec_src =get_target_coords_extern(srcname)
    url = 'https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/w3nh/w3nh.pl?Entry=' + str(ra_src) + '%2C+' + str(
        dec_src) + '&NR=GRB%2FSIMBAD%2BSesame%2FNED&CoordSys=Equatorial&equinox=2000&radius=0.1&usemap=0'
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    a = soup.get_text()
    b = np.array(a.splitlines())
    infoline = np.where(['Average' in line for line in b])
    b[infoline][0].split()
    nh = b[infoline][0].split()[-1]
    nh = float(nh) / 1.0e22
    nh = round(nh, 3)
    return nh


def find_sudden_changes(
        input_e,input_y,input_de,input_dy, p0 = 0.05, logscale_e = False, use_ncp_prior = False, poly_detrend= False
    ):
    """ Find sudden changes/edges into a spectrum using Bayesian blocks (Scargle et al. 2013).
        It is possible to use a logarithmic scaling for the energies.

    Args:
        input_e: array of energy values
        input_y: array of y values
        input_de: array of energy errors
        input_dy: array of y errors
        p0: false alarm probability
        logscale_e: If True, the energies are first transformed into logarithmic space before the bayesian blocks search
        use_ncp_prior: If True, ncp prior is used for normally distributed point measurements
        poly_detrend: If True, detrenting is first conducted using a polynomial fit, before the bayesian blocks search

    Returns:
        array containing the energy values of edges
    """
    # pytest available
    from astropy.stats import bayesian_blocks
    from scipy import interpolate

    if logscale_e:
        e = np.log10(input_e)
        de = (1/input_e)*input_de # simple error propagation
    else:
        e = input_e
        de = input_de

    if poly_detrend:
        smoothing = interpolate.UnivariateSpline(e, input_y, w=1./input_dy, k=3)
        y = input_y - smoothing(e)
        dy = input_dy
    else:
        y = input_y
        dy = input_dy

    if use_ncp_prior:
        # page 12, last paragraph of section 3, Scargle et al. 2013
        changes = bayesian_blocks(e, y, sigma=dy, fitness='measures', ncp_prior = 1.32 + 0.577 *np.log10(len(y)))
    else:
        changes = bayesian_blocks(e, y, sigma=dy, fitness='measures', p0 = p0)

    # Output
    if logscale_e:
        results = 10**changes
    else:
        results = changes

    return results


def align_using_ssd(a_in, b_in, period = None, smoothing=False, n_to_fit=3):

    """Takes two arrays - signals - pulse profiles and aligns them by finding the minimum of the sum of squared differences (SSD).
       It rolls the second array `b` over the first array `a`, computes the SSD at each shift, and fits a Gaussian to the SSD
       values around the minimum to refine the best shift. If the period is given, it returns the time in seconds that the second
       pulse profile should be shifted. Else, it returns the phase bins.
       The new t_ref would be: tref = tref - period*phi

    Args:
        a (numpy array): The reference array on which the second array will be aligned.
        b (numpy array): The second array that is being aligned to the first array.
        period (float): If given, it returs the time in seconds of the shift
        smoothing (bool, optional): If True, applies spline smoothing to both arrays before alignment.
        n_to_fit (int, optional): The number of points on either side of the minimum SSD to use for fitting the Gaussian.

    Returns:
        phbins (float) [-0.5,+0.5]: The phase bin shift based on the best shift and the phase bin spacing.
    or
        seconds (float): The shift in seconds ( plus or minus)
    """

    from lmfit.models import GaussianModel, PolynomialModel
    from scipy import interpolate

    phase = np.linspace(0,1,len(a_in))
    phase_bin_spacing = phase[1] - phase[0]

    # Defining a and b depending whether if smoothing or not
    if smoothing:
        a_smoothed = interpolate.UnivariateSpline(phase, a_in, s=0.05, k=3)
        b_smoothed = interpolate.UnivariateSpline(phase, b_in, s=0.05, k=3)
        a = a_smoothed(phase)
        b = b_smoothed(phase)
    else:
        a = a_in
        b = b_in

    shifts = np.arange(-len(a) + 1, len(a))  # all possible shifts (left and right)
    ssd_values = []

    # For each shift, calculate ssd
    for shift in shifts:
        b_shifted = np.roll(b, shift)

        # Calculate ssd
        ssd = np.sum((a - b_shifted) ** 2)
        ssd_values.append(ssd)

    # Find shift with minimum SSD
    i_min = np.argmin(ssd_values)

    # in case the i_min is near the bounds
    if i_min - n_to_fit >= 0 and i_min + n_to_fit + 1 <= len(shifts):
        to_fit = ssd_values[i_min - n_to_fit:i_min + n_to_fit + 1]
        x_to_fit = shifts[i_min - n_to_fit:i_min + n_to_fit + 1]
    elif i_min - n_to_fit < 0:
        to_fit = np.concatenate([ssd_values[i_min-n_to_fit-1:], ssd_values[:i_min + n_to_fit + 1]])
        x_to_fit = np.concatenate([shifts[i_min-n_to_fit-1:], shifts[:i_min + n_to_fit + 1]])
    else:
        to_fit = np.concatenate([ssd_values[i_min-n_to_fit:], ssd_values[:i_min + n_to_fit - len(shifts) + 1]])
        x_to_fit = np.concatenate([shifts[i_min - n_to_fit:], shifts[:i_min + n_to_fit - len(shifts) + 1]])

    # poly
    poly_mod = PolynomialModel(degree=0)
    pars = poly_mod.guess(to_fit, x=x_to_fit, degree=0)
    mod = poly_mod

    # gauss
    gauss_mod = GaussianModel()
    pars.update(gauss_mod.make_params())

    pars['center'].set(value=shifts[i_min], min=x_to_fit[0], max=x_to_fit[-1])
    pars['sigma'].set(value=1, min=0, max=shifts[n_to_fit]-shifts[0])
    pars['amplitude'].set(value=-np.max(to_fit), min=-np.inf)

    # gauss + poly
    mod = mod + gauss_mod

    fit_result = mod.fit(to_fit, pars, x=x_to_fit)

    # in case the gaussian fit is not succesfull
    if fit_result.success:
        best_shift = fit_result.params['center'].value
    elif not fit_result.success:
        logger.warning("Gaussian fit failed, using the phase bin with the minimum SSD.")
        best_shift = shifts[i_min]  # fallback to raw minimum

    #  phase bin shift
    phbins = best_shift * phase_bin_spacing
    if phbins > 0.5:
        phbins = phbins - 1

    # return x_to_fit, fit_result.best_fit, best_shift, ssd_values[i_min], ssd_values, phbins, shifts
    if period:
        seconds = period*phbins
        return seconds
    else:
        return phbins


def adjust_energy_range(e_min, e_max, ene_min, ene_max, narrow=False):
    '''
    Tool for exact energy range selection of the energy resolved pulse profile.
    After creating the energy-phase matrix, one wants to plot the pulse profile of a specific energy range.
    In this case, they will choose an energy range of 3-20 keV, for insance. However, if this energy range given by the user,
    does not exactly follow the energy binning of the instrument, then the 3-20 keV is NOT the exact energy range of the
    plotted pulse profile. This tool allows the user to give as an input the e_min and e_max arrays of the energy bins of the matrix,
    and it will return the indices of the matrix of the pulse profile that correspond to the "new" energy range that respects
    the energy binning of the instrument, narrowed or expanded depending on the narrow value (True or False).

    For example: if ene_min = 3.1 keV but the actual energy bins there are 3 and 3.2 kev, then in the case of narrow,
    the resulting minimum energy will be 3.2 keV (and therefore narrowing the energy range).
    If narrow = True, then the new minimum of the energy range will be 3 keV (therefore, expanding the energy range).
    If the ene_min chosen by the user has the same value as an existent energy bin, then nothing happens to that value.
    Same exact story for the ene_max.

    Example:
    # construction of the matrix:
    e_min_orig, e_max_orig, pp_orig, dpp_orig, pp_orig_back, dpp_orig_back =  utils.read_and_sum_matrixes(...)

    # rebinning:
    e_min, e_max, pp, dpp, pp_back, dpp_back = utils.rebin_matrix(e_min_orig,e_max_orig, pp_orig, dpp_orig, ...)

    # Then,
    ene_ensel = adjust_energy_range(e_min, e_max, ene_min, ene_max, narrow=False)
    energy_resolved_pulse_profile = pp[ene_ensel]
    errors_energy_resolved_pulse_profile = dpp[ene_ensel]

     ====================================================================================
     Args:
        e_min, e_max (array): Full arrays contaning the e_min and e_max for each energy bin.
        ene_min, ene_max (float): Single values that specify the min and max of the energy range of the energy resolved pulse profile
        narrow (boolean): A flag to narrow or expand the energy range.

     Returns:
        ene_ensel (array): the indices of the pp of the new energy range that respects the energy binning of the instrument

    '''

    ene_min_exists = np.any(np.isclose(e_min, ene_min))
    ene_max_exists = np.any(np.isclose(e_max, ene_max))

    # Find the closest indices to emin and emax and use them
    idx_min = np.searchsorted(e_min, ene_min, 'left')
    if idx_min > 0 and not ene_min_exists:
        idx_min -= 1

    idx_max = np.searchsorted(e_max, ene_max, 'right') - 1
    if idx_max < len(e_max) - 1 and not ene_max_exists:
        idx_max += 1

    ene_where = np.arange(idx_min, idx_max + 1)

    if narrow:
        # Narrowing:
        if ene_min_exists and ene_max_exists:
            ene_ensel = ene_where
        else:
            ene_ensel = ene_where[1:-1] if not ene_min_exists and not ene_max_exists else ene_where
            ene_ensel = ene_where[1:] if not ene_min_exists and ene_max_exists else ene_ensel
            ene_ensel = ene_where[:-1] if ene_min_exists and not ene_max_exists else ene_ensel
    else:
        # Expanding
        ene_ensel = ene_where
        if not ene_min_exists and idx_min > 0:
            ene_ensel = np.insert(ene_ensel, 0, idx_min - 1)
        if not ene_max_exists and idx_max < len(e_max) - 1:
            ene_ensel = np.append(ene_ensel, idx_max + 1)

    print('energy range before:', ene_min, ene_max)
    print('energy range after:', e_min[ene_ensel[0]], e_max[ene_ensel[-1]])

    return ene_ensel
