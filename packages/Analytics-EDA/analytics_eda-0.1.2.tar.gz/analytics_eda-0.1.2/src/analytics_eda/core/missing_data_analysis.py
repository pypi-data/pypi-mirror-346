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
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def missing_data_analysis(
        series: pd.Series,
        report_dir: Path
    ) -> dict:
    """
    Perform missing data analysis on a pandas Series.

    Args:
        series (pd.Series): Series to analyze.
        report_dir (Path): Directory for saving report files.

    Returns:
        dict: {
            'total': int,
            'missing': int,
            'pct_missing': float,
            'missing_count': str (file path to plot)
        }
    """
    print(f"Analyzing Missing Data in Series [{series.name}]")

    # 1. Compute missingness
    total = int(len(series))
    missing = int(series.isna().sum())
    pct_missing = missing / total if total else 0.0
    summary = {'total': total, 'missing': missing, 'pct_missing': pct_missing}

    # 2. Plot and save
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(x=series.isna())
    ax.set_title(f"Missing vs Non-Missing: {series.name}")
    ax.set_xlabel('Is Missing')
    ax.set_ylabel('Count')
    fig = ax.get_figure()

    filename = f"{series.name.replace(' ', '_')}_missingness.png" if series.name else "series_missingness.png"
    missing_data_count_path = report_dir / filename
    fig.savefig(missing_data_count_path)
    plt.close(fig)

    summary['missing_count'] = str(missing_data_count_path)

    return summary
