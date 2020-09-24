#!/usr/bin/env python2
# encoding: utf-8

from . import core

get = core.get_data

def get_cr():
    """
        Return obtained classification rates.
    """
    return {
        # TODO: Replace sw values with newly obtained measurements
        "sw_train" : 0.934,
        "sw_train_err" : 0.009,
        "sw_test" : 0.866,
        "sw_test_err": 0.017,
        "sw+hw_train" : 0.907,
        "sw+hw_train_err": 0.017,
        "sw+hw_test" : 0.781,
        "sw+hw_test_err": 0.015,
        "hw_all_train" : 0.898,
        "hw_all_train_err" : 0.018,
        "hw_all_test" : 0.807,
        "hw_all_test_err" : 0.023,
        "hw_single" : core.get_data("CR_singleHWneuron.npy"),
    }




