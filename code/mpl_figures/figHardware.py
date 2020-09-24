#!/usr/bin/env python2
# encoding: utf-8

import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib import gridspec as gs
from matplotlib import collections as coll
import pylab as p
import copy
import numpy as np

from . import core
from .core import log
from . import aux

def get_gridspec():
    """
        Return dict: plot -> gridspec
    """
    # TODO: Adjust positioning
    gs_main = gs.GridSpec(1, 2, hspace=0.65, width_ratios=[1.,1.],
            left=0.05, right=0.95, top=.93, bottom=0.1)
    gs_aux = gs.GridSpecFromSubplotSpec(2, 1, gs_main[0, 1], hspace=0.5,
                                           height_ratios=[1., 1.])

    return {
            # these are needed for proper labelling
            # core.make_axes takes care of them
            
        "waferPhoto": gs_main[0, 0],

        "pspPreCalib": gs_aux[0, 0],

        "pspPostCalib": gs_aux[1,0],

        }

def adjust_axes(axes):
    """
        Settings for all plots.
    """
    # TODO: Uncomment & decide for each subplot!
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
            "waferPhoto",
        ]:
        axes[k].set_frame_on(False)

def plot_labels(axes):
    core.plot_labels(axes,
        labels_to_plot=[
            "waferPhoto",
            "pspPreCalib",
            "pspPostCalib"
        ],
        label_ypos = {'waferPhoto': 0.96},
        label_xpos = {}
        )

def get_fig_kwargs():
    return { "figsize" : (7.16, 4) }



###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#

def plot_waferPhoto(ax):

    # Photo of an assembled wafer unit

    pass



def plot_pspPreCalib(ax):

    # Bunch of psps on several neurons overleaid using the ideal
    # translation formula
    time = core.get_data('hardware/pspTimePre.npy')
    v = core.get_data('hardware/pspVoltagePre.npy')

    aux.plotPSPs(ax, time, v)
    ax.set_title('pre-calibration')

    pass


def plot_pspPostCalib(ax):

    # Bunch of psps on several neurons overleaid 
    # using the calibration
    time = core.get_data('hardware/pspTimePost.npy')
    v = core.get_data('hardware/pspVoltagePost.npy')

    aux.plotPSPs(ax, time, v)
    ax.set_title('current state of calibration')

    pass
