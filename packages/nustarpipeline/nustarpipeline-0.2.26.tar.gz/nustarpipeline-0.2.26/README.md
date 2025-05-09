# NuSTAR-pipeline

This package wrpas the nustar pipelines for point sources in convenient format for
an homogeneus analysis.

Two executable scripts are provided in the package:
* process_nustar.py to perform the procesing
* get_nustar_data.py to download the data

## Tasks

* Separate the ds9 region generation from spectral processing 

* Make an Heasarc Docker container with Nustar CalDB. 
	- Use version as input variable.
	- Tag the date of creation (for CALDB).

* Port the use of astroquery to find OBSIDs for a source in a given time interval.

* Adapt script to make image.

* Separate a function to create regions with interactive input from the user.

* Extract spectrum



