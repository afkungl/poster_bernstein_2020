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
    gs_main = gs.GridSpec(4, 1, hspace=0.3,
                          height_ratios=[1.,.4,.7,1.],
                          left=0.09, right=0.96, top=.97, bottom=0.05)
    gs_minor1 = gs.GridSpecFromSubplotSpec(1, 2, gs_main[0, 0], wspace=0.2,
                                         hspace=0.2,
                                         width_ratios=[1.,1.])
    gs_minor4 = gs.GridSpecFromSubplotSpec(1, 2, gs_main[3, 0], wspace=0.2,
                                         hspace=0.2,
                                         width_ratios=[1.,1.])
    gs_minor2 = gs.GridSpecFromSubplotSpec(1, 8, gs_main[1, 0], wspace=0.15,
                                        hspace=0.2,
                                        width_ratios=[1.2,1.2,1.2,0.3,1.2,1.2,1.2,0.3])
    gs_minor3 = gs.GridSpecFromSubplotSpec(2, 2, gs_main[2, 0], wspace=0.04,
                                        hspace=0.01,
                                        height_ratios=[.5,1.],
                                        width_ratios=[1.,.01])
    #gs_minor6 = gs.GridSpecFromSubplotSpec(1, 2, gs_main[4, 0], wspace=0.3,
    #                                    hspace=0.2,
    #                                    width_ratios=[1.,1.])
    #gs_minor7 = gs.GridSpecFromSubplotSpec(1, 2, gs_main[5, 0], wspace=0.3,
    #                                    hspace=0.2,
    #                                    width_ratios=[1.,1.])
    return {
        # these are needed for proper labelling
        # core.make_axes takes care of them

        "mnistExample": gs_minor1[0, 0],

        "mnistIterError": gs_minor1[0,1],

        "mnistOrigSandP": gs_minor2[0, 0],
        "mnistClampSandP": gs_minor2[0, 1],
        "mnistNetworkSandP": gs_minor2[0, 2],
        "mnistLabelSandP": gs_minor2[0,3],

        "mnistOrigPatch": gs_minor2[0, 4],
        "mnistClampPatch": gs_minor2[0, 5],
        "mnistNetworkPatch": gs_minor2[0, 6],
        "mnistLabelPatch": gs_minor2[0, 7],

        "compPics": gs_minor3[0,0],
        "compLabel": gs_minor3[1,0],
        "compColorBar": gs_minor3[0:,1],

        "mseMnist": gs_minor4[0,0],
        "errorMnist": gs_minor4[0,1],
    }


def adjust_axes(axes):
    """
        Settings for all plots.
    """
    for ax in axes.itervalues():
        core.hide_axis(ax)

    for k in [
        'mnistExample',
        'compPics',
        'compColorBar',
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

                         "mseMnist",

                         "errorMnist",

                         "mnistOrigSandP",
                         "compPics",
                     ],
                     label_ypos={'mnistExample': .95,
                                 "mnistOrigSandP": 1.05,
                                 "compPics": 1.07
                                 },
                     label_xpos={'mnistExample': -.15,
                                 "mnistOrigSandP": -.15,
                                 "compPics": -.02
                                 }
                     )


def get_fig_kwargs():
    width = 8.
    alpha = 1.3
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
    ax.text(120., 20., 'original', rotation=90)
    ax.text(120., 80., 'reduced', rotation=90)

    ax.text(-28., 35., 'MNIST', weight='bold', fontsize=15, rotation=90)

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
               fontsize=8)

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

def plot_compPics(ax):

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)
    respImages = core.get_data('application/686respPatchMnistDyn.npy')

    # set up the parameters
    dt = 2
    tMin = 100.
    tMax = 350.
    tMinIndex = int(tMin/dt)
    tMaxIndex = int(tMax/dt)
    N_vertical = 1
    N_horizontal = 15
    N_all = N_vertical * N_horizontal
    half = 0
    frame = 1
    picSize = (24, 24)
    picSizeOrig = (12, 12)
    indices = np.floor(np.linspace(tMinIndex,tMaxIndex, N_all)).astype(int)
    respImages = respImages[indices,:]

    # Plot the upper 8 examples (originals)
    pic = np.ones((( N_vertical + 1) * frame + N_vertical * picSize[0] + half,
                   (N_horizontal + 1) * frame + N_horizontal * picSize[1])) * 255.
    for counter in xrange(N_vertical * N_horizontal):
        j = counter % N_horizontal
        i = int(counter / N_horizontal)
        picVec = respImages[counter, :]
        picCounter = np.reshape(picVec, picSizeOrig)
        picCounter = imresize(picCounter, picSize, interp='nearest')


        pic[(i + 1) * frame + i * picSize[0]: (i + 1) * frame + (i + 1) * picSize[0],
            (j + 1) * frame + j * picSize[1]: (j + 1) * frame + (j + 1) * picSize[1]] = picCounter

    ax.imshow(pic, cmap='Greys', aspect='equal')
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    ax.set_ylabel('visible', fontsize=10, labelpad=5)


    pass

def plot_compLabel(ax):

    core.show_axis(ax)
    labels = [0,1,4,7]
    N_labels = len(labels)
    dt = 2
    tMin = 100.
    tMax = 350.
    tMinIndex = int(tMin/dt)
    tMaxIndex = int(tMax/dt)

    labelImage = core.get_data('application/686labelPatchMnistDyn.npy')[tMinIndex:tMaxIndex,:]
    ax.imshow(np.flipud(labelImage.T),
             cmap=cm.gray_r,
             vmin=0., vmax=1.,
             aspect='auto',
             interpolation='nearest',
             extent=(-50., 200., -.5,N_labels - .5))
             #extent=(-.5, N_labels - .5,200.,-50.))
    ax.set_yticks(range(N_labels))
    ax.set_yticklabels(labels)
    for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(11)
    ax.tick_params(width=0, length=0)
    ax.set_xlabel(r'$t$ [ms]', fontsize=12)
    ax.set_ylabel('label', labelpad=0, fontsize=12)
    ax.axvline(x=0, ymin=-.02, ymax=1.5, color='red', linestyle='--',
               clip_on=False)
    ax.text(0., -2.,
            r'stimulus onset' + '\n' + r' at $t=0\, ms$',
            color='red',
            horizontalalignment='center')

def plot_compColorBar(ax):

    cax = inset_axes(ax,
                 width="100%",  # width = 10% of parent_bbox width
                 height="100%",  # height : 50%
                 loc=3,
                 bbox_to_anchor=(0., 0.03, 1, .92),
                 bbox_transform=ax.transAxes,
                 borderpad=0,
                 )
    cmap = mpl.cm.Greys
    norm = mpl.colors.Normalize(vmin=0., vmax=1.0)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                #norm=norm,
                                ticks=[0., 0.2, 0.4, 0.6, 0.8, 1.])

    return

def plot_mseMnist(ax):

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    timeArray = core.get_data('application/fashionTimeArray.npy')
    mseMnistSandp = core.get_data('application/mnistMseSandp.npy')
    mseMnistPatch = core.get_data('application/mnistMsePatch.npy')
    abstractMnistSandp = core.get_data('application/mnistAbstractMseSandpMseArray.npy')
    abstractMnistPatch = core.get_data('application/mnistAbstractMsePatchMseArray.npy')

    aux.plotMse(ax, timeArray, mseMnistPatch, mseMnistSandp,
                abstractMnistPatch, abstractMnistSandp)

    return


def plot_errorMnist(ax):

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # load the data
    timeArray = core.get_data('application/fashionTimeArray.npy')
    errorMnistSandp = core.get_data('application/mnistAccSandp.npy')
    errorMnistPatch = core.get_data('application/mnistAccPatch.npy')
    errorMnistRef = core.get_data('application/mnistAccHW.npy')
    abstractMnistSandp = core.get_data('application/mnistAbstractMseSandp.npy')
    abstractMnistPatch = core.get_data('application/mnistAbstractMsePatch.npy')

    aux.plotErrorTime(ax, timeArray,
                          errorMnistPatch,
                          errorMnistSandp,
                          errorMnistRef,
                          abstractMnistPatch,
                          abstractMnistSandp)

    return



# MNIST
def plot_mnistOrigSandP(ax):

    image = core.get_data('application/145origSandpMnist.npy')
    aux.plotVisible(ax, image, (12,12), 'O')

def plot_mnistClampSandP(ax):

    image = core.get_data('application/145clampSandpMnist.npy')
    aux.plotClamping(ax, image, (12,12), 'C')

def plot_mnistNetworkSandP(ax):

    image = core.get_data('application/145respSandpMnist.npy')
    aux.plotClamping(ax, image, (12,12), 'R')

def plot_mnistLabelSandP(ax):

    image = core.get_data('application/145labelSandpMnist.npy')
    aux.plotLabel(ax, image, [7,4,1,0],'L')


def plot_mnistOrigPatch(ax):

    image = core.get_data('application/27origPatchMnist.npy')
    aux.plotVisible(ax, image, (12,12), 'O')

def plot_mnistClampPatch(ax):

    image = core.get_data('application/27clampPatchMnist.npy')
    aux.plotClamping(ax, image, (12,12), 'C')

def plot_mnistNetworkPatch(ax):

    image = core.get_data('application/27respPatchMnist.npy')
    aux.plotClamping(ax, image, (12,12), 'R')

def plot_mnistLabelPatch(ax):

    image = core.get_data('application/27labelPatchMnist.npy')
    aux.plotLabel(ax, image, [7,4,1,0],'L')
