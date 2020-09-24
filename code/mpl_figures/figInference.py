#!/usr/bin/env python2
# encoding: utf-8

import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib import gridspec as gs
from matplotlib import collections as coll
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition, inset_axes
import matplotlib.pyplot as plt
import pylab as p
import copy
import numpy as np
from scipy.misc import imresize

from . import core
from .core import log
from . import aux


def get_gridspec():
    """
        Return dict: plot -> gridspec
    """
    # TODO: Adjust positioning
    gs_main = gs.GridSpec(1, 1, hspace=0.3,
                          height_ratios=[1.],
                          left=0.04, right=0.94, top=.95, bottom=0.13)
    gs_minor1 = gs.GridSpecFromSubplotSpec(1, 2, gs_main[0, 0], wspace=0.3,
                                         hspace=0.2,
                                         width_ratios=[1.,1.])
    return {
        # these are needed for proper labelling
        # core.make_axes takes care of them

        "mnistExample": gs_minor1[0, 0],

        "mnistIterError": gs_minor1[0,1],

    }


def adjust_axes(axes):
    """
        Settings for all plots.
    """
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
        'mnistExample',
    ]:
        axes[k].set_frame_on(False)

    # Share the y-axes of specific subplots
    for pair in [
    ]:
        axes[pair[0]].get_shared_x_axes().join(axes[pair[0]], axes[pair[1]])



def plot_labels(axes):
    core.plot_labels(axes,
                     labels_to_plot=[
                         "mnistExample",

                         "mnistIterError",
                     ],
                     label_ypos={'mnistExample': .95,
                                 'mnistIterError': .945,
                                 },
                     label_xpos={'mnistExample': -.09,
                                 }
                     )


def get_fig_kwargs():
    width = 6.
    alpha = .5
    return {"figsize": (width, alpha * width)}


###############################
# Plot functions for subplots #
###############################
#
# naming scheme: plot_<key>(ax)
#
# ax is the Axes to plot into
#

def plot_mnistExample(ax):

    # load the data
    original = core.get_data('application/mnist_test_red.npy')

    # Do the actual plotting
    aux.plotExamplePictures(ax, original, (12,12), (28,28), (2,4),
                            indices=[3,4,0,2,5,13,1,6])
    ax.text(-9., 20., 'original', fontsize=11, rotation=90)
    ax.text(-9., 80., 'reduced', fontsize=11, rotation=90)

    #ax.text(-28., 35., 'MNIST', weight='bold', fontsize=15, rotation=90)

    return


def plot_mnistIterError(ax):

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # Load the data
    abstractRatio = core.get_data('application/mnistAbstract.npy')
    classRatio = core.get_data('application/mnistClassRatios.npy')
    iterNumb = core.get_data('application/mnistClassRatiosArray.npy')

    # Do the plot
    aux.plotITLTrainingError(ax, abstractRatio, classRatio, iterNumb)
    ax.set_ylim([-.04, .25])
    ax.legend(loc='lower left', bbox_to_anchor=(0.05, 0.01),
               fontsize=11)

    # Add inset with mixture matrix
    #iax = plt.axes([0, 0, 1, 1])
    #ip = InsetPosition(ax, [0.45, 0.25, 0.3, 0.7]) #posx, posy, width, height
    #iax.set_axes_locator(ip)
    iax = inset_axes(ax, width = "50%", height= "50%", loc=1)

    # Load the data
    mixtureMatrix = core.get_data('application/mnistConfMatrix.npy')
    labels = [0, 1, 4, 7]

    # Do the plot
    iax.set_frame_on(False)
    aux.plotMixtureMatrix(iax, mixtureMatrix, labels)

    return

