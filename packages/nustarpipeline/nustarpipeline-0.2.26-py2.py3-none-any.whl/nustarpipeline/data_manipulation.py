import logging
import numpy as np
import os
import re
import json

logger = logging.getLogger('')

mcmc_latex_dict = {
    'poly_c0' : '$c_0$',
    'poly_c1' : '$c_1$',
    'poly_c2' : '$c_2$',
    'poly_c3' : '$c_3$',
    'poly_c4' : '$c_4$',
    'poly_c5' : '$c_5$',
    'poly_c6' : '$c_6$',
    'poly_c7' : '$c_7$',

    'g1_amplitude': '$A_\\mathrm{Fe}$',
    'g1_center': '$E_\\mathrm{Fe}$',
    'g1_sigma': '$\\sigma_\\mathrm{Fe}$',

    #This is for the case of fit of only one line (still missing case of no iron)
    'g2_amplitude': '$A_\\mathrm{Cyc}$',
    'g2_center': '$E_\\mathrm{Cyc}$',
    'g2_sigma': '$\\sigma_\\mathrm{Cyc}$',
    
    'g3_amplitude': '$A_\\mathrm{Cyc2}$',
    'g3_center': '$E_\\mathrm{Cyc2}$',
    'g3_sigma': '$\\sigma_\\mathrm{Cyc2}$',
    
    'g4_amplitude': '$A_\\mathrm{Cyc3}$',
    'g4_center': '$E_\\mathrm{Cyc3}$',
    'g4_sigma': '$\\sigma_\\mathrm{Cyc3}$',


    'gg1_amplitude': '$A_\\mathrm{Cyc}$',
    'gg1_center': '$E_\\mathrm{Cyc}$',
    'gg1_siggma': '$\\sigma_\\mathrm{Cyc}$',
    
    'gg2_amplitude': '$A_\\mathrm{Cyc2}$',
    'gg2_center': '$E_\\mathrm{Cyc2}$',
    'gg2_siggma': '$\\sigma_\\mathrm{Cyc2}$',
    
    'gg3_amplitude': '$A_\\mathrm{Cyc3}$',
    'gg3_center': '$E_\\mathrm{Cyc3}$',
    'gg3_siggma': '$\\sigma_\\mathrm{Cyc3}$',

    'gg4_amplitude': '$A_\\mathrm{Cyc4}$',
    'gg4_center': '$E_\\mathrm{Cyc4}$',
    'gg4_siggma': '$\\sigma_\\mathrm{Cyc4}$',

    'gg5_amplitude': '$A_\\mathrm{Cyc5}$',
    'gg5_center': '$E_\\mathrm{Cyc5}$',
    'gg5_siggma': '$\\sigma_\\mathrm{Cyc5}$',

    'cstat' : '$\\chi^2_\\mathrm{red,lo}$/d.o.f.',
    'cstat_high' : '$\\chi^2_\\mathrm{red,hi}$/d.o.f.',
    'e_turn' : '$E_\\mathrm{split}$',
    'deg_low' : '$n_\\mathrm{pol}^\\mathrm{(lo)}$',
    'deg_high' : '$n_\\mathrm{pol}^\\mathrm{(hi)}$',
}


mcmc_html_dict = {
    'poly_c0' : '<i>c</i><sub>0</sub>',
    'poly_c1' : '<i>c</i><sub>1</sub>',
    'poly_c2' : '<i>c</i><sub>2</sub>',
    'poly_c3' : '<i>c</i><sub>3</sub>',
    'poly_c4' : '<i>c</i><sub>4</sub>',
    'poly_c5' : '<i>c</i><sub>5</sub>',
    'poly_c6' : '<i>c</i><sub>6</sub>',
    'poly_c7' : '<i>c</i><sub>7</sub>',
    'g1_amplitude': '<i>A</i><sub>Fe</sub>',
    'g1_center': '<i>E</i><sub>Fe</sub>',
    'g1_sigma': '&sigma;<sub>Fe</sub>',
    'gg1_amplitude': '<i>A</i><sub>Cyc</sub>',
    'gg1_center': '<i>E</i><sub>Cyc</sub>',
    'gg1_siggma': '&sigma;<sub>Cyc</sub>',
    
    'gg2_amplitude': '<i>A</i><sub>Cyc2</sub>',
    'gg2_center': '<i>E</i><sub>Cyc2</sub>',
    'gg2_siggma': '&sigma;<sub>Cyc2</sub>',

    'gg3_amplitude': '<i>A</i><sub>Cyc3</sub>',
    'gg3_center': '<i>E</i><sub>Cyc3</sub>',
    'gg3_siggma': '&sigma;<sub>Cyc3</sub>',

    'gg4_amplitude': '<i>A</i><sub>Cyc4</sub>',
    'gg4_center': '<i>E</i><sub>Cyc4</sub>',
    'gg4_siggma': '&sigma;<sub>Cyc4</sub>',

    'gg5_amplitude': '<i>A</i><sub>Cyc5</sub>',
    'gg5_center': '<i>E</i><sub>Cyc5</sub>',
    'gg5_siggma': '&sigma;<sub>Cyc5</sub>',

    'cstat' : '&chi;<sup>2</sup><sub>red,lo</sub>/d.o.f.',
    'cstat_high' : '&chi;<sup>2</sup><sub>red,hi</sub>/d.o.f.',
    'e_turn' : '<i>E</i><sub>split</sub>',
    'deg_low' : '<i>n</i><sub>pol</sub><sup>(lo)</sup>',
    'deg_high' : '<i>n</i><sub>pol</sub><sup>(hi)</sup>',
}


def get_target_coords_extern(input_name):
    from astroquery.simbad import Simbad
    from astropy import units as u
    from astropy.coordinates import SkyCoord

    name = input_name
    simbad = Simbad.query_object(name)
    if simbad is not None and 'RA' in simbad.colnames:
        coord = SkyCoord(simbad['RA'][0], simbad['DEC'][0],
                        unit=[u.hour, u.deg])
    elif simbad is not None and 'ra' in simbad.colnames:
        coord = SkyCoord(simbad['ra'][0], simbad['dec'][0],
                        unit=[u.deg, u.deg])
    else:
        logger.warning(f'Warning: Simbad could not resolve the object {input_name}. Returning None')
        return None

    # coord = coord.fk5 # Probably does not change anything, as the coord is already in the fk5 system

    logger.info("Coordinates for %s are RA=%.4f, Dec=%.4f" % (name, coord.ra.deg, coord.dec.deg))

    return coord.ra.deg, coord.dec.deg



def lmfit_chain_to_dict(dict_name, my_chain, high_part = False, cstat_obj=None):
    """reformats the mcmc results to be used as
    pysas.dump_latex_table(dict_param, utils.mcmc_latex_dict))
    where dict_param is the output of this function

    Args:
        dict_name (str): name of the disctionary to be put in the table
        my_chain (object): first output of utils.explore_fit_mcmc
        high_part (bool, optional): this flag changes the name of gaussians from gX to ggX. Defaults to True.
        castat_obj : lmfit result object to get the chisquared, if None it uses the chain object (it is screwed up sometimes)

    Returns:
        dict: a dictionary of parameters as expected by pysas.dump_latex_table
    """

    if my_chain is not None:
        quantiles = my_chain.flatchain.quantile([0.32, 0.5, 0.68])
        
        out_dict = { dict_name : {} }
        
        for kk in quantiles.keys():       
            if high_part:
                key_name = kk.replace('g','gg')
            else:
                if kk.startswith('g2_'):
                    key_name = kk.replace('g2', 'gg1')
                elif kk.startswith('g3_'):
                    key_name = kk.replace('g3', 'gg2')
                elif kk.startswith('g4_'):
                    key_name = kk.replace('g4', 'gg3')
                elif kk.startswith('g5_'):
                    key_name = kk.replace('g5', 'gg4')
                else:
                    key_name = kk
            out_dict[dict_name].update( {key_name: [ quantiles[kk][0.50], quantiles[kk][0.32], quantiles[kk][0.68]]})
        if cstat_obj is None:
            cstat_obj = my_chain
        if high_part:
            out_dict[dict_name].update({'cstat_high' : [cstat_obj.chisqr, cstat_obj.nfree, cstat_obj.nfree]})
        else:
            out_dict[dict_name].update({'cstat' : [cstat_obj.chisqr, cstat_obj.nfree, cstat_obj.nfree]})
        return out_dict
    elif cstat_obj is not None:
        out_dict = { dict_name : {} }
        for kk, ii in cstat_obj.params.items():
            if '_fwhm' in kk or '_heig' in kk:
                continue
            #print(kk)      
            if high_part:
                key_name = kk.replace('g','gg')
            else:
                if kk.startswith('g2_'):
                    key_name = kk.replace('g2', 'gg1')
                elif kk.startswith('g3_'):
                    key_name = kk.replace('g3', 'gg2')
                elif kk.startswith('g4_'):
                    key_name = kk.replace('g4', 'gg3')
                elif kk.startswith('g5_'):
                    key_name = kk.replace('g5', 'gg4')
                else:
                    key_name = kk
                
            out_dict[dict_name].update( {key_name: [ii.value, ii.value-ii.stderr, ii.value+ii.stderr]})
            
        if high_part:
            out_dict[dict_name].update({'cstat_high' : [cstat_obj.chisqr, cstat_obj.nfree, cstat_obj.nfree]})
        else:
            out_dict[dict_name].update({'cstat' : [cstat_obj.chisqr, cstat_obj.nfree, cstat_obj.nfree]})
        return out_dict
    else:
        return None

def merge_dicts(out_name, dict_list, patterns=None, patterns_to_exclude=None):
    """Merge dictionaries of parameters

    Args:
        out_name (str): key of output dictionary
        dict_list (list): list of dictionaries to merge
        patterns (list): list of strings with patterns to merge

    Returns:
        dict: the merged dictionary
    """    
    
    if patterns is None:
        patterns=[]
        for dd in dict_list:
            for k1, i1 in dd.items():
                for kk in i1.keys():
                    patterns.append(kk)
    
    if patterns_to_exclude is not None:
        new_patterns =[]
        
        for kk in patterns:
            for k1 in patterns_to_exclude:
                if k1 not in kk:
                    new_patterns.append(kk)

        patterns = sorted(list(set(new_patterns)))

    new_dict = {out_name: {}}
    for dd in dict_list:
        for k1, i1 in dd.items():
            for kk in i1.keys():
                include = False
                for pp in patterns:
                    if pp in kk:
                        include = True
                if include:
                    new_dict[out_name].update({kk: i1[kk]})
    return new_dict

def literature_to_dict(dict_name, fe=None, cyc=None):
    """It is a utility to format the manual literature input into a dictionary to be used to dump the latex table

    Args:
        dict_name (str): name of the dictionary key
        fe (list): List with values for Fe line paramters 
            e.g. iron_line  = [[6.79, 0.04, 0.04], [0.16, 0.06, 0.06] , [31, 6, 6], ‘gaus’]
            if None it skips
        cyc (list): List with values for Fe line paramters 
            e.g. cyclotron_line  = [[37.9, -0.15, 0.15], [6.0, -0.3, +0.3] , [23, -0.9, 0.9], ‘gabs’]
            if None it skips

    Returns:
        dict: dictionary with formatted parameters
    """    
    out_dict = { dict_name : {} }
    def get_values(en):
        if isinstance(en, list):
            if len(en) > 1:
                x = float(en[0])
                x_l = x - np.abs(float(en[1]))
                x_h = x + np.abs(float(en[2]))
                
                val = [x, x_l, x_h ]
            elif len(en) == 1 :
                x = float(en[0])
                val = [x, x, x ]
            else:
                x=-1
                val = [x, x, x ]
        else:
            val = [en, en, en]

        return val
    
    def get_para(pp, cyc_flag=True, index=0):
        base_name = 'g%d_' %  (index + 1)
        tmp_dict = {base_name+'center': pp[0+3*index],
                    base_name+'sigma': pp[1+3*index],
                    base_name+'amplitude': pp[2+3*index]}
        para_dict = {}
        for kk, ii in tmp_dict.items():        

            if cyc_flag:
                kk = kk.replace('g', 'gg')
            val = get_values(ii)
            para_dict.update({kk: val})
        return para_dict
    if fe is not None:
        out_dict[dict_name].update(get_para(fe, False))
    if cyc is not None:
        n_lines = int(np.floor(len(cyc)/3))
        for i in range(n_lines):
            out_dict[dict_name].update(get_para(cyc, True, i))

    return out_dict

## These functions should be moved to another project because they are of general intrest

def evaluate_type(name: str):
    """it return the type from its string represenation
    first it looks in global variables for user-defined types, then in builtins

    Args:
        name (str): String representation

    Raises:
        ValueError: if the type is not found

    Returns:
        _type_: type object
    """    
    t = globals().get(name)
    if t:
        return t
    else:
        import builtins
        try:
            t = getattr(builtins, name)
            if isinstance(t, type):
                return t
            else:
                raise ValueError(name)
        except:
            raise ValueError(name)


def infer_type_from_string_representation(ss : str):
    """it infers the variable type from its string repreentation

    Args:
        ss (str): the string representation of a variable

    Returns:
        _type_: type object
    """    

    if 'True' in ss or 'False' in ss:
        return bool
    
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    
    number_list = [float(x) for x in re.findall(match_number, str(ss))]
    
    if ss.startswith('http'):
        return str

    if len(number_list) == 0 or \
        len(re.findall(r'\b10\.\d{4,9}/[-.;()/:\w]+', str(ss)))>0 or \
            len(re.findall(r'[^\deE+-^\ ]{1}', str(ss))) > 0: 
        #this matches DOIs
        #from https://stackoverflow.com/questions/73196058/regex-match-on-string-doi
        return str
    
    if len(number_list) >1 :
        #print(number_list)
        return list
    
    fv = number_list[0]
    
    if np.floor(fv) - fv == 0 and '.' not in ss:        
        return int
    else:
        return float
    

def convert_list(x: str) -> list:
    """it makes a list from its string representation

    Args:
        x (str): String representation

    Returns:
        list: the list (with string representations as values)
    """    
    #from https://stackoverflow.com/questions/1894269/how-to-convert-string-representation-of-list-to-a-list
    x = x.replace('"', '').replace(' ', '').replace('\'','')
    # Look ahead for the bracketed text that signifies nested list
    l_x = re.split(r',(?=\[[A-Za-z0-9\',]+\])|(?<=\]),', x[1:-1])
    #print(l_x)
    # Flatten and split the non nested list items
    l_x0 = [item for items in l_x for item in items.split(',') if not '[' in items]
    # Convert the nested lists to lists
    l_x1 = [
        i[1:-1].split(',') for i in l_x if '[' in i
    ]
    # Add the two lists
    l_x = l_x0 + l_x1
    return l_x

def cast_type(t, x):

    if t is bool:
        if x.lower() == 'true':
            return True
        else:
            return False
    else:
        return t(x)

def convert_list_values(ll : list) -> list:

    """it converts the values of a list from their string representation
    Args :
        ll input list
    Returns:
        list: converted list
    """    
    new_list = []
    
    for x in ll:
        t = infer_type_from_string_representation(x)
        
        if t == list:
            y = convert_list_values(x)
        else:
            y = cast_type(t, x)
        new_list.append(y)
    
    return new_list
        

def get_value_from_papermill_dict(oo):
    """it gets the default value from the papermill returned dictionary

    Args:
        oo (dict): the papermill representation of a parameter

    Returns:
        _type_: the default value with the right type
    """    
    val_str = oo['default']
    inferred_type_name = oo['inferred_type_name']

    if inferred_type_name != 'None':
        t = evaluate_type(inferred_type_name)
    else:
        t = infer_type_from_string_representation(val_str)
    
    if t == str:
        val_str = val_str.replace('\'','')
    #print(t)
    if t == list:
        #print(val_str)
        list_out = convert_list(val_str)
        #print(list_out)
        return convert_list_values(list_out)
        
    return cast_type(t, val_str)

def get_period_formatted(fname='obs_lc/ef_pipe_res.dat', raw=False, frequency=False, fname2='frequency_output.json', html=False):
    """Gets the frequency of period formatted as a latex string or not from the
    run of epoch folding in timingsuite (see utils.get_efold_frequency)


    Args:
        fname (str, optional): file name of the output. Defaults to 'obs_lc/ef_pipe_res.dat'.
        raw (bool, optional): if true return a 2-tuple of numbers, if False a latex-formatted string. Defaults to False.
        frequency (bool, optional): If true returns frequency, if false period. Defaults to False.
        fname2 (str, optional): the json files where we store also the derivative when present. Defaults to frequency_output.json
        html (bool, optional): if the output should be in html format. Defaults to false.

    Returns:
        2-tuple or string: 
            2-tuple:  (x, dx) where x and dx anre period with uncertainty or frequency with uncertainty
            string: a latex-formatted string to be inserted in a table
    """    
    import pyxmmsas as pysas
    
    def expo2html(x):
        return x.replace('$\\times', '&times;').replace('^{', '<sup>').replace('}$', '</sup>')
    
    if os.path.isfile(fname2):
        with open(fname2) as in_fi:
            freq_result = json.load(in_fi)
        if 'freq' not in freq_result:
            logger.warning(fname2 + ' does not contain the frequency result')
        x = freq_result.get('freq', [1.0, 1.0, 1.0])
        dx = freq_result.get('nudot', [1.0, 1.0, 1.0])

        if frequency:
            if raw:
                return (x[1], x[2], dx[1], dx[2])
            else:
                expo, unit, ff, par_name = default_get_unit_latex('nu', '', (x[1], x[0], x[2]), '$\\nu$', flux_norm=1e10)
                format_str = pysas.get_format_string(ff[0], -np.abs(ff[1]), ff[2])
                expo_2, unit_2, dff, par_name_2 = default_get_unit_latex('nudot', '', (dx[1], dx[0], dx[2]), '$\\dot \\nu$', flux_norm=1e10)
                format_str_2 = pysas.get_format_string(dff[0], -np.abs(dff[1]), dff[2])
                if html:
                    return format_str % ff[0] +'&plusmn;' + format_str % ((np.abs(ff[1]) + ff[2])/2) + expo2html(expo) + '<br>' + \
                    '<span class="d-inline-flex justify-content-center dot-wrapper">&nu;</span> =' + \
                    format_str_2 % dff[0] +'&plusmn;' + format_str_2 % ((np.abs(dff[1]) + dff[2])/2)  + expo2html(expo_2)
                else:
                    return (par_name + ' & ' + format_str % ff[0] +' & $\\pm$ ' + format_str % ((np.abs(ff[1]) + ff[2])/2) + expo + ' & ' + unit, 
                        par_name_2 + ' & ' + format_str_2 % dff[0] +' & $\\pm$ ' + format_str_2 % ((np.abs(dff[1]) + dff[2])/2)  + expo_2 + ' & ' + unit_2)
        else:
            p = 1./x[1]
            dp = p**2 * (np.abs(x[0]) + x[2])/2
            pdot = -p**2 * dx[1]
            dpdot = np.sqrt( (2*p * dx[1])**2 * dp**2 + p**4 * (np.abs(dx[0]) + dx[2])**2/4. )
            if raw:
                return (p, dp, pdot, dpdot)
            else:
                expo, unit, ff, par_name = default_get_unit_latex('p', '', (p, dp, dp), '$p$', flux_norm=1e10)
                format_str = pysas.get_format_string(p, dp, dp)
                expo_2, unit_2, dff, par_name_2 = default_get_unit_latex('pdot', '', (pdot, dpdot, dpdot), '$\\dot p$', flux_norm=1e10)
                format_str_2 = pysas.get_format_string(dff[0], dff[1], dff[2])
                if html:
                    return format_str % ff[0] +'&plusmn;' + format_str % (ff[2]) + expo2html(expo) + '<br>' + \
                    '<span class="d-inline-flex justify-content-center dot-wrapper">P</span> =' + \
                    format_str_2 % dff[0] +'&plusmn;' + format_str_2 % (dff[2]) + expo2html(expo_2)
                else:
                    return (par_name + ' & ' + format_str % ff[0] +' & $\\pm$ ' + format_str % ff[2] + expo + ' & ' + unit, 
                        par_name_2 + ' & ' + format_str_2 % dff[0] +' & $\\pm$ ' + format_str_2 % dff[2] + expo_2 + ' & ' + unit_2)

    if os.path.isfile(fname) is False:
        raise FileExistsError(fname + ' does not exist, run the epoch foldding first')   
    x = np.loadtxt(fname, dtype=np.double)

    if frequency:
        if raw:
            return (x[2], x[3])
        else:
            format_str = pysas.get_format_string(x[4], x[5], x[5])
            if html:
                return format_str % x[2] + '&plusmn;' + format_str % x[3]
            else:
                return format_str % x[2] + ' & $\\pm$ ' + format_str % x[3]
    else:
        if raw:
            return (x[4], x[5])
        else:
            format_str = pysas.get_format_string(x[4], x[5], x[5])
            if html:
                return format_str % x[4] + '&plusmn;' + format_str % x[5]
            else:
                return format_str % x[4] + ' & $\\pm$ ' + format_str % x[5]


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def default_get_unit_latex(par, kk, ff, par_name, flux_norm=1e10):
    unit = ''
    if 'flux' in par:
        ff *= flux_norm
        unit = '$10^{%d}\\mathrm{erg\\,s^{-1}\\,cm^{-2}}$' % (-np.log10(flux_norm))

    if 'norm' in par and ('bbody' in kk or 'diskbb' in kk):
        ff = np.sqrt(ff)
        unit = 'km/10 kpc'
        par_name = 'r'

    if 'kT' in par or 'peak' in par or 'E' in par or 'g1_center' in par or 'g1_sigma' in par or 'poly_c1' in par \
            or 'gg1_siggma' in par or 'e_turn' in par:
        unit = 'keV'
    
    if 'poly_c2' in par:
        unit = 'keV$^{-2}$'

    if 'poly_c3' in par:
        unit = 'keV$^{-3}$'
    
    if 'poly_c3' in par:
        unit = 'keV$^{-3}$'

    if 'poly_c4' in par:
        unit = 'keV$^{-4}$'

    if 'poly_c5' in par:
        unit = 'keV$^{-5}$'

    if 'poly_c6' in par:
        unit = 'keV$^{-6}$'

    if 'poly_c7' in par:
        unit = 'keV$^{-7}$'

    if 'nH' in par:
        unit = 'cm$^{-2}$'

    if 'nu' == par:
        unit = 'Hz'
    if 'p' == par:
        unit ='s'
    if 'nudot' == par:
        unit = 'Hz\,s$^{-1}$'
    if 'pdot' == par:
        unit = 's\,s$^{-1}$'
    
    #print(np.log10(ff[0]))
    if float(ff[0]) != 0.0:
        if np.abs(np.log10(np.abs(ff[0])))>= 2:
            tmp = np.floor(np.log10(np.abs(ff[0])))
            expo = '$\\times10^{%d}$' % int(tmp)
            ff = np.array(ff) / 10**tmp
        else:
            expo = ''
    else:
        expo = ''
        #print(tmp, ff)

    return expo, unit, ff, par_name
        
        
def default_get_unit_html(par, kk, ff, par_name, flux_norm=1e10):
    unit = ''
    if 'flux' in par:
        ff *= flux_norm
        unit = '$10<sup>%d</sup> erg s<sup>-1</sup>cm<sup>-2</sup>' % (-np.log10(flux_norm))

    if 'norm' in par and ('bbody' in kk or 'diskbb' in kk):
        ff = np.sqrt(ff)
        unit = 'km/10 kpc'
        par_name = 'r'

    if 'kT' in par or 'peak' in par or 'E' in par or 'g1_center' in par or 'g1_sigma' in par or 'poly_c1' in par \
            or 'gg1_siggma' in par or 'e_turn' in par:
        unit = 'keV'
    
    if 'poly_c2' in par:
        unit = 'keV<sup>-2</sup>'

    if 'poly_c3' in par:
        unit = 'keV<sup>-3</sup>'
    
    if 'poly_c3' in par:
        unit = 'keV<sup>-3</sup>'

    if 'poly_c4' in par:
        unit = 'keV<sup>-4</sup>'

    if 'poly_c5' in par:
        unit = 'keV<sup>-5</sup>'

    if 'poly_c6' in par:
        unit = 'keV<sup>-6</sup>'

    if 'poly_c7' in par:
        unit = 'keV<sup>-7</sup>'

    if 'nH' in par:
        unit = 'cm<sup>-2</sup>'

        
    if 'nu' == par:
        unit = 'Hz'
    if 'p' == par:
        unit ='s'
    if 'nudot' == par:
        unit = 'Hz s<sup>-1</sup>$'
    if 'pdot' == par:
        unit = 's s<sup>-1</sup>$'
    
    #print(np.log10(ff[0]))
    if float(ff[0]) != 0.0:
        if np.abs(np.log10(np.abs(ff[0])))>= 2:
            tmp = np.floor(np.log10(np.abs(ff[0])))
            expo = '&times;10<sup>%d</sup>' % int(tmp)
            ff = np.array(ff) / 10**tmp
        else:
            expo = ''
        #print(tmp, ff)
    else:
        expo = ''
    return expo, unit, ff, par_name

