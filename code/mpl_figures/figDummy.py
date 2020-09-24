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


def get_gridspec():
    """
        Return dict: plot -> gridspec
    """
    # TODO: Adjust positioning
    gs_main = gs.GridSpec(1, 2, hspace=0.65,
            left=0.05, right=0.95, top=.95, bottom=0.16)

    return {
            # these are needed for proper labelling
            # core.make_axes takes care of them

            "dummy1" : gs_main[0, 0],

            "dummy2" : gs_main[0, 1],
        }

def adjust_axes(axes):
    """
        Settings for all plots.
    """
    # TODO: Uncomment & decide for each subplot!
    for ax in axes.itervalues():
        core.hide_axis(ax)

    #for k in [
    #        "dummy1",
    #        "dummy2"
    #    ]:
    #    axes[k].set_frame_on(False)

def plot_labels(axes):
    core.plot_labels(axes,
        labels_to_plot=[
            "dummy1",
            "dummy2",
        ],
    #    label_ypos = {'delays_all': 0.95},
        label_xpos = { 'dummy2': 0.02,
                    "dummy1": 0.02
                    }
        )

def get_fig_kwargs():
    return { "figsize" : (7.16, 3) }



###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#
def plot_dummy1(ax):
    volts = np.linspace(2., 20., 100.)

    core.show_axis(ax)
    core.make_spines(ax)

    ax.plot(volts)


def plot_dummy2(ax):
    
    data = core.get_data('dummy.npy')

    core.show_axis(ax)
    core.make_spines(ax)

    ax.plot(data)
    ax.set_xlabel('The x axis')
    ax.set_ylabel('The y axis')


    pass
