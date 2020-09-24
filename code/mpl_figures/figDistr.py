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
    gs_main = gs.GridSpec(2, 1, hspace=0.3,
                          left=0.1, right=0.96, top=.96, bottom=0.08)
    gs_top = gs.GridSpecFromSubplotSpec(1, 3, gs_main[0, 0], wspace=0.3,
                                           width_ratios=[1., .8, 1.5])
    gs_bot = gs.GridSpecFromSubplotSpec(1, 3, gs_main[1, 0], wspace=0.3,
                                           width_ratios=[1., .8, 1.5])

    return {
        # these are needed for proper labelling
        # core.make_axes takes care of them

        "trainingP": gs_top[0, 0],
        "dklP": gs_top[0, 1],
        "jointP": gs_top[0, 2],

        "trainingS": gs_bot[0, 0],
        "dklS": gs_bot[0, 1],
        "jointS": gs_bot[0, 2],

    }


def adjust_axes(axes):
    """
        Settings for all plots.
    """
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
    ]:
        axes[k].set_frame_on(False)


def plot_labels(axes):
    core.plot_labels(axes,
                     labels_to_plot=[
                            "trainingP",
                            "trainingS",
                            "dklP",
                            "dklS",
                            "jointP",
                            "jointS",
                     ],
                     label_ypos = {},
                     label_xpos={'dklP': 0.1,
                                 'dklS': 0.1,
                                 },
                     )


def get_fig_kwargs():
    width = 10.
    alpha = 0.7
    return {"figsize": (width, alpha*width)}


###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#


def plot_trainingP(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    DKLiter = core.get_data('distr/fig4_DKLiterArrPoisson.npy')
    DKLiterValue = core.get_data('distr/fig4_DKLiterValuePoisson.npy')
    DKLfinal = core.get_data('distr/fig4_DKLtimeValuePoisson.npy')

    aux.suppPlotTraining(ax, DKLiterValue, DKLfinal, DKLiter)

    ax.legend(loc='lower left', bbox_to_anchor=(0.3, 0.6))
    ax.set_ylim([8e-3,3.e0])
    ax.text(-210, 0.4, 'Poisson noise', weight='bold', rotation=90)

def plot_dklP(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    DKLtimeValue = core.get_data('distr/fig4_DKLtimeValuePoisson.npy')
    DKLtimeArray = core.get_data('distr/fig4_DKLtimeArrayPoisson.npy')

    aux.suppPlotDklTime(ax, DKLtimeArray, DKLtimeValue)
    ax.set_ylim([7e-3,5e0])

def plot_jointP(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    sampled = core.get_data('distr/fig4_finalJointPoisson.npy')
    target = core.get_data('distr/fig4_targetJoint.npy')

    aux.suppPlotDistributions(ax, sampled, target, errorBar=True)
    ax.set_xlabel(r'$\mathbf{z}$, states')
    ax.legend(loc='lower left', bbox_to_anchor=(0.02, 0.5))
    ax.set_ylim([0., 0.26])


def plot_trainingS(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    DKLiter = core.get_data('distr/fig4_DKLiterArraySon.npy')
    DKLiterValue = core.get_data('distr/fig4_DKLiterValueSon.npy')
    DKLfinal = core.get_data('distr/fig4_DKLtimeValueSon.npy')

    aux.suppPlotTraining(ax, DKLiterValue, DKLfinal, DKLiter)

    ax.text(-210, .9, 'Decorrelation Network', weight='bold', rotation=90)
    ax.legend(loc='lower left', bbox_to_anchor=(0.3, 0.6))
    ax.set_ylim([8e-3,3.e0])

def plot_dklS(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    DKLtimeValue = core.get_data('distr/fig4_DKLtimeValueSon.npy')
    DKLtimeArray = core.get_data('distr/fig4_DKLtimeArraySon.npy')

    aux.suppPlotDklTime(ax, DKLtimeArray, DKLtimeValue)
    ax.set_ylim([7e-3,5e0])

def plot_jointS(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    sampled = core.get_data('distr/fig4_finalJointSon.npy')
    target = core.get_data('distr/fig4_targetJoint.npy')

    aux.suppPlotDistributions(ax, sampled, target, errorBar=True)
    ax.set_xlabel(r'$\mathbf{z}$, states')
    ax.legend(loc='lower left', bbox_to_anchor=(0.02, 0.5))
    ax.set_ylim([0., 0.26])