#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This script will characterize an SRAM previously generated by OpenRAM given a
configuration file. Configuration option "use_pex" determines whether extracted
or generated spice is used and option "analytical_delay" determines whether
an analytical model or spice simulation is used for characterization.
"""

import sys
import datetime
from globals import *
from importlib import reload

(OPTS, args) = parse_args()

# Override the usage
USAGE = "Usage: {} [options] <config file>\nUse -h for help.\n".format(__file__)

# Check that we are left with a single configuration file as argument.
if len(args) != 2:
    print(USAGE)
    sys.exit(2)

# These depend on arguments, so don't load them until now.
import debug

# Parse config file and set up all the options
init_openram(config_file=args[0], is_unit_test=False)

print_banner()

# Configure the SRAM organization (duplicated from openram.py)
from characterizer.fake_sram import fake_sram
s = fake_sram(name=OPTS.output_name,
                word_size=OPTS.word_size,
                num_words=OPTS.num_words,
                write_size=OPTS.write_size,
                num_banks=OPTS.num_banks,
                words_per_row=OPTS.words_per_row,
                num_spare_rows=OPTS.num_spare_rows,
                num_spare_cols=OPTS.num_spare_cols)

s.parse_html(args[1])
s.setup_multiport_constants()

OPTS.netlist_only = True
OPTS.check_lvsdrc = False

# Characterize the design
start_time = datetime.datetime.now()
from characterizer import lib
debug.print_raw("LIB: Characterizing... ")
lib(out_dir=OPTS.output_path, sram=s, sp_file=OPTS.output_path + OPTS.output_name + ".sp", use_model=False)
print_time("Characterization", datetime.datetime.now(), start_time)

# Output info about this run
print("Output files are:\n{0}*.lib".format(OPTS.output_path))
#report_status() #could modify this function to provide relevant info

# Delete temp files, remove the dir, etc.
end_openram()