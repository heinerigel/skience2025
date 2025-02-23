# Seismic Noise Analysis at Skience 2025

This repository contains notebooks and data for analyzing seismic noise recorded in Grenoble, France.
The data originates from an instrumentation of the Hautbois Wooden High-Rise building in Grenoble (France) for Structural Health Monitoring and earthquake engineering.

Data Reference: Gueguen, P., & Vieux Champagne, F. (2023). Monitoring of the Hautbois Wooden High-Rise building in Grenoble, France (RESIF-SISMOB)[Data set]. RESIF - Réseau Sismologique et géodésique Français. https://doi.org/10.15778/RESIF.8N2021


## Contents

### Data Analysis Notebooks

1. `01 - Time series`: Basic analysis of seismic time series data, including visualization and processing of daily data.

2. `02 - Noise PSD and RMS vs Time`: Power spectral densities and time-frequency analysis of the noise data.

3. `03 - Noise statistics - i95 and friends`: Computation of noise statistics, and classification of seismic noise into different categories based on statistical parameters.

4. `10 - Continuous HVSR Geopsy`: Analysis of Horizontal-to-Vertical Spectral Ratio (HVSR) using Geopsy software, including:
   - Manual and automatic processing of ambient noise data
   - Virtual borehole analysis
   - Polarization analysis

5. `11 - HVSR from PSD`: Alternative approach to HVSR analysis using Power Spectral Density (PSD) data, including:
   - Comparison with Geopsy results
   - Cross-station spectral ratios
   - Continuous HVSR monitoring

### Additional Analysis Notebooks

##### Cross-Correlation Analysis
- `50 - MSNoise - CCFs`: Comprehensive tutorial on using MSNoise for computing cross-correlation functions (CCFs) from continuous seismic data. Includes database setup, configuration, data processing, and visualization of cross-correlation results.

- `51 - MSNoise - DVV`: Analysis of relative velocity variations (dv/v) using MSNoise. Demonstrates how to compute and visualize temporal velocity changes using Moving Window Cross Spectral (MWCS) analysis.

- `91 - Bonus - HVSR from CCFs`: Alternative approach to computing H/V spectral ratios using the imaginary part of cross-correlation functions. Shows how to process autocorrelations for vertical and horizontal components to derive HVSR.

These notebooks complement the main noise analysis techniques with more advanced processing methods using cross-correlation approaches. They're particularly useful for monitoring temporal changes in structure and comparing different HVSR computation methods.

### Key Features

- Processing of three-component node data
- Multiple approaches to HVSR analysis
- Statistical noise classification
- Time series visualization
- Cross-station comparisons

## Requirements

- Python 3.x
- ObsPy
- Geopsy software
- Additional Python packages: numpy, pandas, matplotlib, etc.

## References

- Van Noten et al. (2022) - Brussels' bedrock paleorelief analysis
- Van Noten et al. (2020) - HVSR to Virtual Borehole
- Gueguen et al. (2023) - Monitoring of the Hautbois Wooden High-Rise building in Grenoble
- Lecocq et al. (2020) - COVID Noise
- Lecocq et al. (2020) - SeismoRMS package
- Lecocq et al. (2014) - MSNoise

## Authors

Includes work and contributions from:
- Koen Van Noten
- Thomas Lecocq
