import numpy as np
import pytest
import pandas as pd
from configparser import ConfigParser
from pathlib import Path
from ligo.skymap.postprocess.cosmology import cosmo
from ligo.skymap.io import read_sky_map

from .. import chirp_probabilities


def test_version():
    from .. import __version__
    assert __version__ == '0.1.0'


@pytest.mark.parametrize(
    'chirp_bins',
    [[0.1, 0.87, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7,
      1.9, 2.1, 2.3, 3, 5.5, 11, 22, 44, 88, 1000]]
)
def test_bins(chirp_bins):
    '''Test the bins are correctly read in from the conf file'''
    rel_path = 'conf.ini'
    conf_path = Path(__file__).parents[1] / rel_path
    print(conf_path)
    config = ConfigParser()
    config.read(conf_path)
    conf_bins = np.asarray([float(bin) for bin in config.get('conf', 'chirp_bins').split()])  # noqa E501
    assert all(conf_bins == chirp_bins)


@pytest.mark.parametrize(
    'mchirp_det,correct_bin_idx',
    [[1.7, 1],
     [14.0, 13]]
)
def test_LL_cgmi(mchirp_det, correct_bin_idx):
    '''Checks the highest probability bin is correct for LL cgmi estimate'''
    rel_path = 'conf.ini'
    conf_path = Path(__file__).parents[1] / rel_path
    config = ConfigParser()
    config.read(conf_path)
    chirp_bins = np.asarray([float(bin) for bin in config.get('conf', 'chirp_bins').split()])  # noqa E501

    rel_path = 'data/sample_bayestar_map.fits'
    sky_map_path = Path(__file__).parents[0] / rel_path
    sky_map = read_sky_map(sky_map_path, moc=True)
    probs = chirp_probabilities.chirp_mass_histogram_LL(sky_map, mchirp_det,
                                                        chirp_bins, cosmo,
                                                        save_path=None,
                                                        plot_det_mc=False)
    idx = np.argmax(probs)
    assert idx == correct_bin_idx


@pytest.mark.parametrize(
    'mchirp_source,mchirp_det,correct_bin_idx',
    [[[1.13, 1.21, 1.12, 1.18, 1.14, 1.28, 1.26], 1.19, 3],
     [[12.3, 13.2, 11.1, 9.6, 8.9, 10.2, 13.8], 12.0, 14]]
)
def test_PE_cgmi(mchirp_source, mchirp_det, correct_bin_idx):
    '''Checks the highest probability bin is correct for PE cgmi estimate'''
    rel_path = 'conf.ini'
    conf_path = Path(__file__).parents[1] / rel_path
    config = ConfigParser()
    config.read(conf_path)
    chirp_bins = np.asarray([float(bin) for bin in config.get('conf', 'chirp_bins').split()])  # noqa E501

    probs = chirp_probabilities.chirp_mass_histogram_PE(mchirp_source,
                                                        mchirp_det,
                                                        chirp_bins,
                                                        save_path=None,
                                                        plot_det_mc=False)
    idx = np.argmax(probs)
    assert idx == correct_bin_idx


@pytest.mark.parametrize(
    'group,mchirp_det,mass_1_source,mass_2_source,correct_bin_idx_PE,correct_bin_idx_LL',  # noqa E501
    [['CBC', 1.2, [1.5, 1.6, 1.55], [1.4, 1.3, 1.45], 4, 0],
     ['Burst', 15, [15, 16, 15.5], [14, 13, 14.5], 14, 14]]
)
def test_cgmi_cWB_CBC(group, mchirp_det, mass_1_source,
                      mass_2_source, correct_bin_idx_PE,
                      correct_bin_idx_LL):
    '''Checks the highest probability bin is correct for cgmi estimate'''

    PE_data = pd.DataFrame()
    PE_data['mass_1_source'] = mass_1_source
    PE_data['mass_2_source'] = mass_2_source

    rel_path = 'data/sample_bayestar_map.fits'
    skymap_path = Path(__file__).parents[0] / rel_path
    sky_map = read_sky_map(skymap_path, moc=True)
    chirp_bins, probs_LL, probs_PE = chirp_probabilities.cgmi(group, mchirp_det, PE_data, sky_map, plot=False, plot_det_mc=False, MDC=False)  # noqa E501
    idx_PE, idx_LL = np.argmax(probs_PE), np.argmax(probs_LL)
    # check for correct bins
    assert idx_PE == correct_bin_idx_PE
    assert idx_LL == correct_bin_idx_LL
