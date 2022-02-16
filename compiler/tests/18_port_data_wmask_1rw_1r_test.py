#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# All rights reserved.
#
import unittest
from testutils import *
import sys, os

import globals
from globals import OPTS
from sram_factory import factory
import debug


class port_data_wmask_1rw_1r_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        from modules import sram_config

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        globals.setup_bitcell()

        c = sram_config(word_size=16,
                        write_size=4,
                        num_words=16)

        c.words_per_row = 1
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "No column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)

        c.num_words = 32
        c.words_per_row = 2
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Two way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)

        c.num_words = 64
        c.words_per_row = 4
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Four way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)

        c.num_words = 128
        c.words_per_row = 8
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Eight way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)

        OPTS.num_rw_ports = 0
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1
        globals.setup_bitcell()

        c.num_words = 16
        c.words_per_row = 1
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "No column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)
        a = factory.create("port_data", sram_config=c, port=1)
        self.local_check(a)
        #
        c.num_words = 32
        c.words_per_row = 2
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Two way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)
        a = factory.create("port_data", sram_config=c, port=1)
        self.local_check(a)

        c.num_words = 64
        c.words_per_row = 4
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Four way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)
        a = factory.create("port_data", sram_config=c, port=1)
        self.local_check(a)

        c.word_size = 8
        c.num_words = 128
        c.words_per_row = 8
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Eight way column mux")
        a = factory.create("port_data", sram_config=c, port=0)
        self.local_check(a)
        a = factory.create("port_data", sram_config=c, port=1)
        self.local_check(a)

        globals.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())