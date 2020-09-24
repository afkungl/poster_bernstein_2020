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
    gs_main = gs.GridSpec(1, 1, hspace=0.65,
                          left=0.02, right=0.98, top=.95, bottom=0.2)
    gs_aux = gs.GridSpecFromSubplotSpec(1, 3, gs_main[0, 0], wspace=0.15,
                                           width_ratios=[.75, 1., 1.])

    return {
        # these are needed for proper labelling
        # core.make_axes takes care of them

        "bmStructure": gs_aux[0, 0],

        "tracesToStates": gs_aux[0, 1],

        "rbmSketch": gs_aux[0, 2],

    }


def adjust_axes(axes):
    """
        Settings for all plots.
    """
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
        "tracesToStates",
        "bmStructure",
        "rbmSketch",
    ]:
        axes[k].set_frame_on(False)


def plot_labels(axes):
    core.plot_labels(axes,
                     labels_to_plot=[
                         "bmStructure",
                         "tracesToStates",
                         "rbmSketch",
                     ],
                     label_ypos = {},
                     label_xpos={'tracesToStates': -.2,},
                     )


def get_fig_kwargs():
    width = 6.
    alpha = 5./12.
    return {"figsize": (width, alpha*width)}


###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#


def plot_bmStructure(ax):

    # Photo of an assembled wafer unit

    pass

def plot_tracesToStates(ax):

    volts = core.get_data('theory/trace.npy')

    for i, v in enumerate(volts):
        ax.plot(v + i * 3. - 3., '-k')
    ax.text(170, -57.5, r't [a.u.]')

    ax.text(-80, -48.5, r'$u_3$')
    ax.text(-80, -51.5, r'$u_2$')
    ax.text(-80, -54.5, r'$u_1$')

    ax.text(130., -45.2, '101', color='r', rotation=90, fontsize=10)
    ax.text(280., -45.2, '100', color='r', rotation=90, fontsize=10)
    ax.text(-80., -46.4, 'z', color='r', fontsize=12)

    ax.axvline(150., ymin=.015, ymax=.78, color='r')
    ax.axvline(300., ymin=.015, ymax=.78, color='r')

    ax.set_ylim(-55.5, -44)

    return

def plot_rbmSketch(ax):

    # Zoom to a retoicle with an incoming connection
    # neurons and synapses are marked

    pass
