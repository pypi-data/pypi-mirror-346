# Copyright 2025 ArchiStrata, LLC and Andrew Dabrowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections.abc import Sequence
import warnings
import numpy as np
import pandas as pd
from scipy import stats

def alternative_fit_assessment(
    s: pd.Series,
    alpha: float = 0.05,
    distributions: Sequence[str] = ('norm', 'lognorm', 'gamma', 'expon'),
    n_bins: int | None = None,
) -> dict:
    """
    Assess non-normal data by:
      1. Fitting a set of candidate distributions & running KS/AD GOF.
      2. Running a binned χ² goodness-of-fit to a target distribution.

    Args:
        s (pd.Series): The data to assess.
        alpha (float): Significance level for all tests.
        distributions: Names of scipy.stats distributions to fit & test.
        n_bins (int|None): Number of bins for χ² GOF. Defaults to Sturges’ rule.

    Returns:
        dict: {
            'alternative_fits': {
                dist_name: { 'params': tuple, 'ks': {...}, 'ad'?: {...} }, …
            },
            'chi2_binned': { 'statistic': float, 'p_value': float, 'reject': bool }
        }
    """
    print("Performing Alternative Assessment")

    # 1. Fit & GOF for each candidate
    alt_fits = {}
    for name in distributions:
        print(f"Performing alternative fit using [{name}]")
        dist = getattr(stats, name)

        # skip known-positive-only if data has non-positives
        if name in ('lognorm','gamma') and s.min() <= 0:
            alt_fits[name] = {'error': 'requires positive data'}
            continue

        if name == 'expon':
            # OK to include zeros, just guard against negatives:
            if s.min() < 0:
                alt_fits['expon'] = {'error': 'requires non-negative data'}
                continue

        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                params = dist.fit(s)
        except Exception as e:
            alt_fits[name] = {'error': str(e)}
            continue

        ks_stat, ks_p = stats.kstest(s, name, params)
        alt_fits[name] = {
            'params': params,
            'ks': {'statistic': ks_stat, 'p_value': ks_p, 'reject': ks_p < alpha}
        }

    # 2. Binned χ² GOF against normal
    # TODO: Expand Binned Data analysis
    # Determine bins
    if n_bins is None:
        # Sturges’ rule
        n_bins = int(np.ceil(np.log2(len(s)) + 1))

    print(f"Performing Binned χ² GOF against normal using bins [{n_bins}]")
    # Compute observed & expected counts
    obs, edges = np.histogram(s, bins=n_bins)
    mu, sigma = s.mean(), s.std(ddof=1)
    cdf_vals = stats.norm.cdf(edges, loc=mu, scale=sigma)
    exp = np.diff(cdf_vals) * len(s)

    # Drop zero‐expected bins
    mask = exp > 0
    obs = obs[mask]
    exp = exp[mask]

    total_obs = obs.sum()
    total_exp = exp.sum()
    if total_exp > 0:
        exp = exp * (total_obs / total_exp)

    chi2_stat, chi2_p = stats.chisquare(obs, f_exp=exp)
    chi2_res = {
        'statistic': float(chi2_stat),
        'p_value': float(chi2_p),
        'reject': bool(chi2_p < alpha),
        'n_bins_used': int(obs.size)
    }

    return {
        'alternative_fits': alt_fits,
        'chi2_binned': chi2_res
    }
