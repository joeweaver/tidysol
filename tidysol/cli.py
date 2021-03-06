"""
TidySOL, a CLI for creating a tidy CSV from exported COMSOL data.

Usage:
  tidysol times <name>
  tidysol vars <name>
  tidysol meta <name> [--values]
  tidysol tidy <name> [--times=<time> ... ] [--cols=<variable> ...] [--output=<outfile>]
  tidysol -h | --help
  tidysol -v | --version

Commands:
  times         List the timesteps for which data are recorded
  vars          List the variables recorded for each time step
  meta          List the metadata preceding the variables
  tidy          Create a tidy CSV from exported data, optionally using only certain variables and timesteps.

Options:
  -h --help     Show this screen.
  -v --version  Version number
  <name>        Exported COMSOL data to process
  -d --describe  Include the variable's description.
  --time=<time>  Include data only from the specified time step(s)
  --col=<variable>  Include data only for the given variable(s). Variables from metadata are also accepted.

Details:
I do a lot of extra data analysis on some of my CFD projects. I often prefer other tools and the best way for me to work with COMSOL's exported data is to get it into a well-formed (i.e. tidy [http://r4ds.had.co.nz/tidy-data.html]) CSV format.

If you're very interested in tidy data, the open access journal article* describing it can be found here:  http://www.jstatsoft.org/v59/i10/
* Wickham, H. (2014). Tidy data. Journal of Statistical Software, 59(10), 1-23.

Limitations:
Only test on output from COMSOL 4.3a. Further, I only use these options for export:
--If you use a different version or export options, use at your own risk.
-Points to evaluate in: Taken from Data Set
Data format: spreadsheet
Transpose: NOT checked
Space dimension: take from data set
Geometry level: Take from data set
Advanced
Include header: CHECKED
Full precision: CHECKED
Sort: NOT checked
Evaluate in: Gauss points
Gauss Point Order: 1
Smoothing: None

This is not a fast exporter. It has not be optimized and doesn't take guesses. For example, it does not
assum that there will be no more commented lines in the export file (those beginning with %) after it starts reading
them.  This is by intention, although it means this is not a fast reader, it is a slow reader, it is at least not a half-fast reader.
Save as txt. 
Acknowledgements:
This cli was fleshed out from the skeleton CLI framework provided by https://github.com/rdegges/skele-cli
Also, thanks to countless commenters on random google searches and stackoverflow
"""



from inspect import getmembers, isclass

from docopt import docopt


import re

def main():
    """Main CLI entrypoint."""
    import tidysol.commands

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(tidysol.commands, k) and v:
            module = getattr(tidysol.commands, k)
            tidysol.commands = getmembers(module, isclass)
            for command in tidysol.commands:
                if command[0] != 'Base':
                    if re.search('^\<class \'tidysol\.commands\.',str(command[1])): 
                        command=command[1]
                        command=command(options)
                        command.run()

if __name__ == "__main__":
    options = docopt(__doc__)
    main()
else:
    from . import __version__ as VERSION
    options = docopt(__doc__, version=VERSION)