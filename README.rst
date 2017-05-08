tidysol
=========

*Tidysol, a CLI for creating a tidy CSV from exported COMSOL data.*


Purpose
-------
I do a lot of extra data analysis on some of my CFD projects. I often prefer other tools and the best way for me to work with COMSOL's exported data is to get it into a well-formed (i.e. tidy_) CSV format.

If you're very interested in tidy data, the Tidy Data[1] article describing is available_ via open access.  

Usage
-----
  tidysol times <name>
  tidysol vars <name>
  tidysol meta <name> [--values]
  tidysol tidy <name> [--times=<time> ... ] [--cols=<variable> ...] [--output=<outfile>]
  tidysol -h | --help
  tidysol -v | --version

Commands
--------
  times         List the timesteps for which data are recorded
  vars          List the variables recorded for each time step
  meta          List the metadata preceding the variables
  tidy          Create a tidy CSV from exported data, optionally using only certain variables and timesteps.

Options
-------
  -h --help     Show this screen.
  -v --version  Version number
  <name>        Exported COMSOL data to process
  -d --describe  Include the variable's description.
  --time=<time>  Include data only from the specified time step(s)
  --col=<variable>  Include data only for the given variable(s). Variables from


.. _tidy: http://r4ds.had.co.nz/tidy-data.html
.. [#] Wickham, H. (2014). Tidy data. Journal of Statistical Software, 59(10), 1-23.
.. _available: http://r4ds.had.co.nz/tidy-data.html
