import pytest
import numpy as np
import os
import nustarpipeline.utils as u
import warnings
mylocation = os.getcwd()
data_folder = os.path.join(mylocation, 'data_tests/')
# All tests for the utils.py
# In order to test only a specific function: pytest test_mod.py::test_func


# =======================================
# utils.corrected_trimmed_std pytest
@pytest.mark.parametrize('trim_fraction', 0.05)
def test_corrected_trimmed_std(trim_fraction):
    from scipy.stats.mstats import trimmed_std
    # Generate 1000 random numbers from a normal (Gaussian) distribution
    data = np.random.normal(loc=0, scale=1, size=1000)
    # Standard deviation (population std by default)
    std_dev = np.std(data)

    # Trimmed standard deviation: exclude 10% of the lowest and highest values
    trimmed_std_dev = trimmed_std(data,
                                  limits=(trim_fraction,
                                          trim_fraction))
    corrected_trimmed_std = u.corrected_trimmed_std(data,
                                                    limits=(trim_fraction,
                                                            trim_fraction))
    # Check if the trimmed standard deviation is close to the expected value
    print(f"Standard deviation: {std_dev:.4f}")
    print(f"Trimmed standard deviation: {trimmed_std_dev:.4f}")
    print(f"Corrected trimmed standard deviation: {corrected_trimmed_std:.4f}")
    assert np.isclose(std_dev, corrected_trimmed_std, rtol=1e-1)


# =======================================
# utils.find_sudden_changes pytest
def read_data_for_find_sudden_changes(data_file):
    e,de,y,dy = np.genfromtxt(
        data_file, dtype = 'float', usecols = (0,1,2,3), skip_header = 1, delimiter = ' ',unpack = True
    )
    return e,de,y,dy

# There should be no warnings for this simple data set
@pytest.mark.parametrize('p0', [1e-5,0.01,0.1,1,10])
@pytest.mark.parametrize('logscale_e', [True, False])
@pytest.mark.parametrize('use_ncp_prior', [True, False])
@pytest.mark.parametrize('poly_detrend', [True, False])
def test_no_warnings(p0, logscale_e, use_ncp_prior, poly_detrend):
    data_changes_test = os.path.join(data_folder, 'data_pytest_find_sudden_changes.dat')
    e, de, y, dy = read_data_for_find_sudden_changes(data_changes_test)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always") #catch all warnings
        # Filtering out specific numpy RuntimeWarnings (has to do with the incompatibility between different libraries)
        warnings.filterwarnings("ignore", message="numpy.ndarray size changed, may indicate binary incompatibility", category=RuntimeWarning)
        result = u.find_sudden_changes(e, y, de, dy, p0, logscale_e, use_ncp_prior, poly_detrend)
        if len(w) > 0:
            for warning in w:
                print(f"Warning: {warning.message}, Category: {warning.category}, File: {warning.filename}, Line: {warning.lineno}")
            pytest.fail("Expected no warnings, but warnings were raised")

#Testing output
@pytest.mark.parametrize('p0', [1e-5,0.01,0.1,1,10])
@pytest.mark.parametrize('logscale_e', [True, False])
@pytest.mark.parametrize('use_ncp_prior', [True, False])
@pytest.mark.parametrize('poly_detrend', [True, False])
def test_outputs(p0,logscale_e,use_ncp_prior,poly_detrend):
    data_changes_test = data_folder + 'data_pytest_find_sudden_changes.dat'
    e,de,y,dy = read_data_for_find_sudden_changes(data_changes_test)
    try:
        result = u.find_sudden_changes(e,y,de,dy, p0, logscale_e, use_ncp_prior, poly_detrend)
        assert isinstance(result, np.ndarray)  # Check if the result is an array
        assert len(result) > 0  # Check if the result is not empty
    except Exception as e:
        pytest.fail(f"find_sudden_changes raised an exception: {e}")

# Testing if for p = 0.05 and no detrending, it can find the most obvious discontinuities of the specific data file
def test_discontinuities():
    data_changes_test = data_folder + 'data_pytest_find_sudden_changes.dat'
    e,de,y,dy = read_data_for_find_sudden_changes(data_changes_test)
    points = [1.,16.5,34.5,50.]
    try:
        result = u.find_sudden_changes(e,y,de,dy)
        assert np.all(np.isin(points, result))
    except Exception as e:
        pytest.fail(f"find_sudden_changes raised an exception: {e}")

# =======================================
# utils.align_using_ssd

# Reads the data of two already aligned signals. The phase returned should be close to zero
@pytest.mark.parametrize('smoothing',[False,True])
def test_align_using_ssd(smoothing):
    # Assuming 'test_data.txt' is the file containing the two arrays with headers.
    data_align_test = os.path.join(data_folder, 'data_pytest_align_using_ssd.dat')
    a,b = np.genfromtxt(
        data_align_test, dtype = 'float', usecols = (0,1), skip_header = 1, delimiter = None ,unpack = True
    )
    shift = u.align_using_ssd(a, b, smoothing)
    # Testing if the phase bin shift is near zero
    assert np.isclose(shift, 0, atol=0.01), f"Phase bin shift too large: {phbins}"

# =======================================
