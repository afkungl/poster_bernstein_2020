#!/usr/bin/env python2
# encoding: utf-8

import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib import gridspec as gs
from matplotlib import collections as coll
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition, inset_axes
import pylab as p
import copy
import numpy as np
import scipy as scp
import scipy.special as special

from . import core
from .core import log


def get_gridspec():
    """
        Return dict: plot -> gridspec
    """
    # TODO: Adjust positioning
    gs_main = gs.GridSpec(1, 2, hspace=0.3, width_ratios = [1.2,1.],
                          left=0.03, right=0.95, top=.95, bottom=0.08)
    gs_left = gs.GridSpecFromSubplotSpec(2, 1, gs_main[0, 0], hspace=0.3,
                                           height_ratios=[1., 1.])
    gs_right = gs.GridSpecFromSubplotSpec(2, 1, gs_main[0, 1], hspace=0.3,
                                           height_ratios=[1., 1.])
    gs_bot = gs.GridSpecFromSubplotSpec(1, 2, gs_right[1, 0], wspace=0.3,
                                           width_ratios=[1.,1.])

    return {
        # these are needed for proper labelling
        # core.make_axes takes care of them

        "strucPoisson": gs_left[0, 0],

        "actFunc": gs_right[0, 0],

        "strucSon": gs_left[1, 0],

        "histMiddle": gs_bot[0, 0],

        "histSigma": gs_bot[0, 1],

    }


def adjust_axes(axes):
    """
        Settings for all plots.
    """
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
        "strucPoisson",
        "strucSon",
    ]:
        axes[k].set_frame_on(False)


def plot_labels(axes):
    core.plot_labels(axes,
                     labels_to_plot=[
                         "strucPoisson",
                         "strucSon",
                         "actFunc",
                         "histMiddle",
                         "histSigma",
                     ],
                     label_ypos = {},
                     label_xpos={'strucPoisson': -.02,
                                 'strucSon': -.02},
                     )


def get_fig_kwargs():
    width = 12.
    alpha = 0.4
    return {"figsize": (width, alpha*width)}


###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#


def plot_strucPoisson(ax):

    # Structure of the network with Poisson noise sources

    pass

def plot_strucSon(ax):

    # Structure of the network with sea of noise sources

    pass

def plot_actFunc(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # Do the activation function
    # Dummy data to work with something
    wBias  = np.arange(-15, 16)
    data = core.get_data('setup/actFunc.npy')
    dataSon = core.get_data('setup/actFuncSon.npy')
    meanFreq = np.mean(data, axis=1)
    stdFreq = np.std(data, axis=1)
    meanFreqSon = np.mean(dataSon, axis=1)
    stdFreqSon = np.std(dataSon, axis=1)
    ax.errorbar(wBias, meanFreq, yerr=stdFreq,
                linewidth=0.6, marker='x',
                label='Poisson',
                color='#1b9e77')
    ax.errorbar(wBias, meanFreqSon, yerr=stdFreqSon,
                linewidth=0.6, marker='x',
                label='DN',
                color='#d95f02')
    ax.set_xlabel(r'$w_\mathrm{bias} \; [HW. u.]$')
    ax.set_ylabel(r'Frequency $\nu \; [Hz]$')
    ax.set_xlim([-15.5, 15.5])
    ax.legend(loc=4)

    # make the inset
    # make dummy data
    data = core.get_data('setup/biasTraces.npy')
    index = np.where(data[:,0] == 0)[0]
    time = data[index,1]
    voltage = data[index,2]
    iax = inset_axes(ax,
                     width = "80%",
                     height= "80%",
                     loc=10,
                     bbox_transform=ax.transAxes,
                     bbox_to_anchor=(.08,.3, .4, .5))
    core.show_axis(iax)
    core.make_spines(iax)
    iax.plot(time, voltage, linewidth=1, color='xkcd:brick red')
    iax.set_ylabel(r'$u_\mathrm{bias} \; [mV]$', fontsize=8)
    iax.set_xlabel(r'$t \; [ms]$', fontsize=8)
    iax.set_xlim([2000., 2080.])
    iax.set_title('bias neuron', fontsize=10)
    iax.tick_params(axis='both', which='both', labelsize=7, size=3)


    return

def plot_histMiddle(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # Generate dummy data
    midPoisson = core.get_data('setup/poisson_middle.npy')
    midSon = core.get_data('setup/son_middle.npy')

    # Cut off outlier
    midSon = midSon[np.where(midSon>-10.)[0]]

    # Make the histograms
    maxVal = np.max([np.max(midPoisson), np.max(midSon)])
    minVal = np.min([np.min(midPoisson), np.min(midSon)])
    upper = maxVal + 0.1 * (maxVal - minVal)
    lower = minVal - 0.1 * (maxVal - minVal)
    bins = np.linspace(lower, upper, 30)
    alpha = 0.7
    ax.hist(midPoisson,
            color='#1b9e77',
            label='Poisson',
            bins=bins,
            alpha=alpha,
            normed=True)
    ax.hist(midSon,
            color='#d95f02',
            label='DN',
            bins=bins,
            alpha=alpha,
            normed=True)
    ax.set_xlabel(r'$\hat{w}_\mathrm{b}[HW.u.]$')
    ax.set_ylabel(r'density [1]')
    ax.legend(loc='upper left', bbox_to_anchor=(0.4, 0.8))

    return

def plot_histSigma(ax):

    core.show_axis(ax)
    core.make_spines(ax)

    # Generate dummy data
    midPoisson = core.get_data('setup/poisson_sigma.npy')
    midSon = core.get_data('setup/son_sigma.npy')

    # Cut off outlier
    midSon = midSon[np.where(midSon<10.)[0]]

    # Make the histograms
    maxVal = np.max([np.max(midPoisson), np.max(midSon)])
    minVal = np.min([np.min(midPoisson), np.min(midSon)])
    upper = maxVal + 0.1 * (maxVal - minVal)
    lower = minVal - 0.1 * (maxVal - minVal)
    bins = np.linspace(lower, upper, 30)
    alpha = 0.7
    ax.hist(midPoisson,
            color='#1b9e77',
            label='Poisson',
            bins=bins,
            alpha=alpha,
            normed=True)
    ax.hist(midSon,
            color='#d95f02',
            label='DN',
            bins=bins,
            alpha=alpha,
            normed=True)
    ax.set_xlabel(r'$\sigma [HW.u.]$')
    ax.set_ylabel(r'density [1]')
    ax.legend(loc='upper left', bbox_to_anchor=(0.5, 0.8))

    return
