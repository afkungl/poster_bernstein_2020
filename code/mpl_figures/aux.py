#!/usr/bin/env python2
# encoding: utf-8

import matplotlib as mpl
import matplotlib.image as mpimg
from matplotlib import gridspec as gs
from matplotlib import collections as coll
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from matplotlib.offsetbox import  OffsetImage, AnnotationBbox
from mpl_toolkits.axes_grid1.colorbar import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
import pylab as p
import copy
import numpy as np
from scipy.misc import imresize
from . import core

"""
This file gathers the auxilliary functions which are repeated over several images when the plots are created. This should structre the codes and reduce code redundancy.

Use it well!
"""

def suppPlotDistributions(ax, sampled, target, errorBar=True):
    """
    Keywords:
        -- ax: pointer of the axis object
        -- sampled: numpy matrix with states in columns and repetitions in rows
        -- target: numpy vector of the target distribution
    """

    # Get the medain and the quarters for the emulated distr
    # obtain the data fro the plots
    sampledMedian = np.median(sampled, axis=0)
    sampled75 = np.percentile(sampled, 75, axis=0)
    sampled25 = np.percentile(sampled, 25, axis=0)
    errDown = sampledMedian - sampled25
    errUp = sampled75 - sampledMedian

    x = np.array(range(0, len(sampledMedian)))
    # make the bar plots
    ylabels = ['0.05', '0.1', '0.2']

    ax.bar(x, target, width=0.35,
          label='target', bottom=1E-3, color='tab:blue')
    ax.bar(x + 0.35, sampledMedian, width=0.35,
           label='sampled', bottom=1E-3, color='tab:orange')
    
    if errorBar:
        ax.errorbar(x + .35, sampledMedian, yerr=[errDown, errUp],
                    ecolor='black', elinewidth=1, capthick=1, fmt="none",
                    capsize=0.0, label='IQR')
    # ax.legend()
    # ax.set_yscale('log')
    #ax.set_ylim(5e-2, 3.0001e-1)
    ax.set_xticks([])
    #ax.set_yticks([.05, .1, .2])
    #ax.set_xticklabels(xlabels, rotation='vertical')
    # ax.set_yticklabels(ylabels)
    ylim = ax.get_ylim()
    ylimNew = [0., ylim[1]]
    ax.set_ylim(ylimNew)
    ax.set_xlim([min(x - .35), max(x + 0.35 + .35)])

    ax.set_xlabel(r'$\mathbf{z}$', fontsize=16)
    ax.set_ylabel(r'$p(\mathbf{z})$', fontsize=16)


def suppPlotTraining(ax, DKLiterValue, DKLfinal, DKLiter):
    """
    Keywords:
        -- ax: axes object of the figure
        -- DKLiter: x axes, i.e. vector for the iteration values
        -- DKLiterValue: nupy matrix of the evolution of the DKL in iterations over several repetitions (in rows)
        -- DKLfinal: in rows: DKL over time for several repetitions
    """

    # obtain the data fro the plots
    DKLiterMedian = np.median(DKLiterValue, axis=0)
    DKLiter75 = np.percentile(DKLiterValue, 75, axis=0)
    DKLiter25 = np.percentile(DKLiterValue, 25, axis=0)

    # Obtain the final DKL values
    finalDKLmedian = np.median(DKLfinal[:, -1]) * np.ones(len(DKLiter))
    finalDKL75 = np.percentile(DKLfinal[:, -1], 75) * np.ones(len(DKLiter))
    finalDKL25 = np.percentile(DKLfinal[:, -1], 25) * np.ones(len(DKLiter))

    # Do the plotting
    linewidth = 1.
    ax.plot(DKLiter, DKLiterMedian, color='r', linewidth=linewidth,
            label='training')
    ax.fill_between(DKLiter,
                    DKLiter25,
                    DKLiter75,
                    color='r',
                    alpha=0.5,
                    linewidth=0.0)

    ax.plot(DKLiter, finalDKLmedian, color='b', linewidth=linewidth,
            label='final')
    ax.fill_between(DKLiter,
                    finalDKL25,
                    finalDKL75,
                    color='b',
                    alpha=0.5,
                    linewidth=0.0)

    ax.set_yscale('log')
    ax.set_ylabel(
        r'$\mathregular{D}_\mathregular{KL} \left[ \, p(\mathbf{z}) \, || \, p\!^*(\mathbf{z}) \, \right]$')
    ax.set_xlabel(r'# iteration [1]')


def suppPlotDklTime(ax, DKLtimeArray, DKLtimeValue):
    '''
    Keywords:
        -- DKLtimeValue: in rows: DKL over time for several repetitions
        -- DKLtimeArray: time array corresponding to the DKL evaluations
    '''

    # obtain the data fro the plots
    DKLMedian = np.median(DKLtimeValue, axis=0)
    DKL75 = np.percentile(DKLtimeValue, 75, axis=0)
    DKL25 = np.percentile(DKLtimeValue, 25, axis=0)

    # Do the plotting
    linewidth = 1.
    ax.plot(DKLtimeArray, DKLMedian, color='r', linewidth=linewidth)
    ax.fill_between(DKLtimeArray,
                    DKL25,
                    DKL75,
                    color='r',
                    alpha=0.5,
                    linewidth=0.0)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel(
        r'$\mathregular{D}_\mathregular{KL} \left[ \, p(\mathbf{z}) \, || \, p\!^*(\mathbf{z}) \, \right]$')
    ax.set_xlabel(r'$t$ [ms]')


def plotITLTraining(ax, abstractRatio, classRatio, iterNumb):
    """ helper function to plot the in-the-loop training for both cases

        Keywords:
            --- ax: the axes object
            --- abstractRatio: reference values for classification with abstract RBM in sofware.
            --- classRatio: matrix with several repetitions, values for inference with hardware
            --- iterNumb: array of the iteration corresponding to the classRatio

    """

    # Do the plotting
    CRmedian = np.median(classRatio, axis=0)
    CR75 = np.percentile(classRatio, 75, axis=0)
    CR25 = np.percentile(classRatio, 25, axis=0)
    Amedian = np.median(abstractRatio, axis=0)
    A75 = np.percentile(abstractRatio, 75, axis=0)
    A25 = np.percentile(abstractRatio, 25, axis=0)

    print('Abstract class ratio is: {0}+{1}-{2}'.format(Amedian,
                                                        A75-Amedian,
                                                        Amedian-A25))
    print('Hardware class ratio is: {0}+{1}-{2}'.format(CRmedian[-1],
                                                        CR75[-1]-CRmedian[-1],
                                                        CRmedian[-1]-CR25[-1]))

    ax.plot(iterNumb, CRmedian, linewidth=1.5, color='xkcd:black',
            label='hardware')
    ax.fill_between(iterNumb,
                    CR25,
                    CR75,
                    color='xkcd:black',
                    alpha=0.2,
                    linewidth=0.0,
                    )

    ax.set_ylabel('classification ratio [1]')
    ax.set_xlabel('number of iterations [1]')
    #ax.set_ylim([np.min(classRatio) - 0.05, 1.05])
    ax.set_ylim([0., 1.05])
    # ax.grid(True)
    xmin = min(iterNumb)
    xmax = max(iterNumb)
    ax.axhline(y=Amedian,
               xmin=xmin,
               xmax=xmax,
               linewidth=2,
               color='r',
               label='software')
    xArray = np.linspace(xmin, xmax)
    yArray = np.ones(len(xArray))
    ax.fill_between(xArray, A75 * yArray, A25 * yArray,
                    color='r', alpha=0.2, linewidth=0.0)


def plotITLTrainingError(ax, abstractRatio, classRatio, iterNumb):
    """ helper function to plot the in-the-loop training for both cases

        Keywords:
            --- ax: the axes object
            --- abstractRatio: reference values for classification with abstract RBM in sofware.
            --- classRatio: matrix with several repetitions, values for inference with hardware
            --- iterNumb: array of the iteration corresponding to the classRatio

    """

    # Do the plotting
    errorRatio = 1.0 - classRatio
    errorAbstract = 1.0 - abstractRatio
    CRmedian = np.median(errorRatio, axis=0)
    CR75 = np.percentile(errorRatio, 75, axis=0)
    CR25 = np.percentile(errorRatio, 25, axis=0)
    Amedian = np.median(errorAbstract, axis=0)
    A75 = np.percentile(errorAbstract, 75, axis=0)
    A25 = np.percentile(errorAbstract, 25, axis=0)

    print('Abstract error ratio is: {0}+{1}-{2}'.format(Amedian,
                                                        A75-Amedian,
                                                        Amedian-A25))
    print('Hardware error ratio is: {0}+{1}-{2}'.format(CRmedian[-1],
                                                        CR75[-1]-CRmedian[-1],
                                                        CRmedian[-1]-CR25[-1]))

    ax.plot(iterNumb, CRmedian, linewidth=1.5, color='xkcd:black',
            label='hardware')
    ax.fill_between(iterNumb,
                    CR25,
                    CR75,
                    color='xkcd:black',
                    alpha=0.2,
                    linewidth=0.0,
                    )

    ax.set_ylabel('error ratio [1]', fontsize=12)
    ax.set_xlabel('number of iterations [1]', fontsize=12)
    #ax.set_ylim([np.min(classRatio) - 0.05, 1.05])
    ax.set_ylim([-0.01, 0.25])
    # ax.grid(True)
    xmin = min(iterNumb)
    xmax = max(iterNumb)
    ax.axhline(y=Amedian,
               xmin=xmin,
               xmax=xmax,
               linewidth=1,
               linestyle='--',
               color='r',
               label='software')
    xArray = np.linspace(xmin, xmax)
    yArray = np.ones(len(xArray))
    ax.fill_between(xArray, A75 * yArray, A25 * yArray,
                    color='r', alpha=0.2, linewidth=0.0)


def plotMixtureMatrix(ax, mixtureMatrix, labels):
    """
        auxiliary function to plot the mixture matrix

        Keywords:
            --- ax: the axes object
            --- mixtureMatrix: the data for the mixture matrix
            --- labels: labels in the mixture matrix corresponding to classes

    """

    # Add a finite number to the otherwise zero values
    # to get around the logarithmic nan values
    mixtureMatrix[np.where(mixtureMatrix==0)] += 1

    disc = np.max(mixtureMatrix)
    fonts = {'fontsize': 8}
    tickSize = 6
    cmap = mpl.cm.get_cmap('inferno', disc)
    cmap.set_under((0., 0., 0.))
    im = ax.imshow(mixtureMatrix, cmap=cmap,
                    aspect=1., interpolation='nearest',
                    norm=LogNorm())
    cax = inset_axes(ax,
                 width="5%",  # width = 10% of parent_bbox width
                 height="100%",  # height : 50%
                 loc=3,
                 bbox_to_anchor=(1.05, 0., 1, 1),
                 bbox_transform=ax.transAxes,
                 borderpad=0,
                 )
    f = ticker.ScalarFormatter(useOffset=False, useMathText=True)
    g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
    cbar = colorbar(im, cax=cax, ticks=[100,900],
                    extend='both',
                    format=ticker.FuncFormatter(g))
    cbar.ax.tick_params(labelsize=6)
    ax.set_ylabel('true label', **fonts)
    ax.set_xlabel('predicted label', **fonts)

    for location in ['top', 'bottom', 'left', 'right']:
        ax.spines[location].set_linewidth(5.)

    # Change the ticks to labels names
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(length=0., pad=5)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=tickSize)
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=tickSize)
    ax.tick_params(axis='both', which='minor')


def plotVisible(ax, imageVector, picSize, label):
    """
        plot the visible layer using imshow

        Keywords:
            --- ax: axes object
            --- imageVector: numpy array of the visible units
            --- picSize: size of the picute, tuple
            --- label: x label for the image

    """

    core.show_axis(ax)
    network = imageVector

    pic = np.reshape(network, picSize)
    ax.imshow(pic,
               cmap=cm.gray_r,
               vmin=0., vmax=1.,
               interpolation='nearest')
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    ax.set_xlabel(label, labelpad=5, fontsize=11, rotation=30)
    ax.set_adjustable('box-forced')


def plotClamping(ax, clampingVector, picSize, label):
    """
        plot the clamping layer using imshow

        Keywords:
            --- ax: axes object
            --- clampingVector: image vector with clampings
            --- picSize: size of the picute, tuple
            --- label: x label for the image

    """

    core.show_axis(ax)

    clamping = clampingVector
    clampMask = np.resize(clamping, picSize)

    overlay = np.ma.masked_where(clampMask!=-1,
                                 np.ones(clampMask.shape))
    indices = np.where(clampMask==-1)
    clampMask[indices] = 0.
    cmap = cm.gray_r
    cmap.set_bad(color='w', alpha=0.)
    ax.imshow(clampMask,
                cmap=cm.gray_r,
                vmin=0.,
                vmax=1.,
                interpolation='nearest')
    ax.imshow(overlay,
               cmap=cm.rainbow,
               vmin=0.,
               vmax=1.,
               alpha=0.9,
               interpolation='nearest')
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    ax.set_xlabel(label, labelpad=5, fontsize=11, rotation=30)


def plotLabel(ax, imageVector, labels, label):
    """
        plot the label layer using imshow

        Keywords:
            --- ax: axes object
            --- iamgeVector: activity of the label units
            --- picSize: size of the picute, tuple
            --- labels: labels at the classification
            --- label: x label for the image

    """

    core.show_axis(ax)
    labelResponse = imageVector
    N_labels = len(labelResponse)
    picSizeLabels = (N_labels,1)

    pic = np.reshape(labelResponse, picSizeLabels)
    ax.imshow(pic,
                 cmap=cm.gray_r,
                 vmin=0., vmax=1.,
                 interpolation='nearest',
                 extent=(0., 1., -.5,N_labels - .5))

    ax.set_yticks(range(N_labels))
    ax.set_yticklabels(labels, fontsize=6)
    ax.tick_params(width=0, length=0)
    ax.set_xticks([], [])
    ax.set_xlabel(label, labelpad=5, rotation=30)
    ax.set_adjustable('box-forced')

    pass


def plotExamplePictures(ax, original, picSizeRed, picSize, grid, indices=range(200)):


    # Layout specification
    N_vertical = grid[0]
    N_horizontal = grid[1]
    half = 3
    frame = 1

    # Do the actual plotting
    # create the picture matrix
    pic = np.ones(((2 * N_vertical + 1) * frame + 2 * N_vertical * picSize[0] + half,
                   (N_horizontal + 1) * frame + N_horizontal * picSize[1])) * 255

    # Plot the upper 8 examples (originals)
    for counter in xrange(N_vertical * N_horizontal):
        i = counter % N_vertical
        j = int(counter / N_vertical)
        picVec = original[indices[counter], 1:]
        picCounter = np.reshape(picVec, picSize)

        pic[(i + 1) * frame + i * picSize[0]: (i + 1) * frame + (i + 1) * picSize[0],
            (j + 1) * frame + j * picSize[1]: (j + 1) * frame + (j + 1) * picSize[1]] = picCounter

    # Plot the lower 8 examples (reduced)
    for counter in xrange(N_vertical * N_horizontal):
        i = counter % N_vertical + 2
        j = int(counter / N_vertical)
        picVec = original[indices[counter], 1:]
        picCounter = np.reshape(picVec, picSize)
        picCounter = imresize(picCounter, picSizeRed, interp='nearest')
        median = np.percentile(picCounter, 50)
        picCounter = ((np.sign(picCounter - median) + 1) / 2) * 255.
        picCounter = imresize(picCounter, picSize, interp='nearest')

        pic[(i + 1) * frame + half + i * picSize[0]: (i + 1) * frame + (i + 1) * picSize[0] + half,
            (j + 1) * frame + j * picSize[1]: (j + 1) * frame + (j + 1) * picSize[1]] = picCounter

    # Make the half line white
    lower = 3 * frame + 2 * picSize[0]
    pic[lower:lower+half - 1,:] = 0

    ax.imshow(pic, cmap='Greys', aspect='equal')


def plot_tsne(ax, pics, pos, picSize):
    """
        Make the tsne plot of pictures on a speicified axes object

            Keywords:
                --- ax: axes object
                --- X: matrix of the data, the images are in rows
                --- Y: position matrix of the data with tsne, the 2d coordinates are in rows
                --- picSize: 2d Tuple, the size of the pictures
    """


    # Plot the pictures according to the coordinates
    for i in range(0, len(pos)):
        cmap = mpl.pyplot.get_cmap('gray_r')
        pic = np.reshape(pics[i], picSize)
        img = cmap(np.ma.masked_array(pic, pic<0.1))
        #img = cmap(pic)
        imagebox = OffsetImage(img, zoom = 1.2, interpolation='nearest')
        xy = (pos[i][0],pos[i][1])
        ab = AnnotationBbox(imagebox, xy, boxcoords="data", pad=0.05, frameon=False)
        ab.zorder = 1
        ax.add_artist(ab)

    # make the lines connecting the images
    ax.scatter(pos[:,0], pos[:,1], 20, "w", alpha=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot(pos[:,0], pos[:,1], linewidth = 1, linestyle = '-', color = 'gray', alpha = 0.2, zorder = 0)


def plotMse(ax, timeArray, patch, sandP, patchAbstract, sandpAbstract):
    """
        Convenience function to plot the mse plots

        Keywords:
            --- ax: axes object
            --- timeArray: timeArray
            --- patch: Mse matrix for the patch occlusion
            --- sandP: Mse matrix for the salt and pepper occlusion
    """

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # set up the data
    datas = [patch, sandP, patchAbstract, sandpAbstract]
    labels = ['Patch HW', 'S&P HW', 'Patch SW', 'S&P SW']
    colors = ['xkcd:crimson', 'xkcd:forest green', 'xkcd:red', 'xkcd:green']
    timeArray = timeArray - 150.

    # do the plotting
    for index in range(2):
        data = datas[index]

        median = np.median(data, axis=0)
        value75 = np.percentile(data, 75, axis=0)
        value25 = np.percentile(data, 25, axis=0)
        ax.plot(timeArray, median, linewidth=1.5, color=colors[index],
            label=labels[index])

        ax.fill_between(timeArray,
                        value25,
                        value75,
                        color=colors[index],
                        alpha=0.2,
                        linewidth=0.0,
                        )

    for index in range(2,4):
        data = datas[index]

        median = np.median(data, axis=0)
        value75 = np.percentile(data, 75, axis=0)
        value25 = np.percentile(data, 25, axis=0)
        ax.plot(timeArray, np.ones(len(timeArray))*median,
                linewidth=1.,
                color=colors[index],
                label=labels[index],
                linestyle='--')

        ax.fill_between(timeArray,
                        value25 * np.ones(len(timeArray)),
                        value75 * np.ones(len(timeArray)),
                        color=colors[index],
                        alpha=0.2,
                        linewidth=0.0,
                        )

    # annotate the plot
    ax.set_xlabel(r'$t$ [ms]', labelpad=5, fontsize=12)
    ax.set_ylabel('mean squared error [1]', fontsize=12)
    ax.set_xlim([-50., 200.])
    ax.set_ylim([0.0, 0.55])
    ax.legend(fontsize=11, loc=1)


def plotErrorTime(ax, timeArray, patch, sandP, reference, patchAbstract, sandpAbstract):
    """
        Convenience function to plot the mse plots

        Keywords:
            --- ax: axes object
            --- timeArray: timeArray
            --- patch: error matrix for the patch occlusion
            --- sandP: error matrix for the salt and pepper occlusion
    """

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # set up the data
    datas = [patch, sandP, reference, patchAbstract, sandpAbstract]
    labels = ['Patch HW', 'S&P HW', 'HW ref','Patch SW', 'S&P SW']
    colors = ['xkcd:crimson', 'xkcd:forest green', 'xkcd:black', 'xkcd:red', 'xkcd:green']
    timeArray = timeArray - 150.

    # do the plotting
    for index in range(3):
        data = datas[index]
        error = 1. - np.mean(data, axis=0)
        ax.plot(timeArray, error, linewidth=1.5, color=colors[index],
            label=labels[index])


    for index in range(3,5):
        data = datas[index]

        median = 1. - np.median(data, axis=0)
        value75 = 1. - np.percentile(data, 75, axis=0)
        value25 = 1. - np.percentile(data, 25, axis=0)
        ax.plot(timeArray, np.ones(len(timeArray))*median,
                linewidth=1.,
                color=colors[index],
                label=labels[index],
                linestyle='--')

        ax.fill_between(timeArray,
                        value25 * np.ones(len(timeArray)),
                        value75 * np.ones(len(timeArray)),
                        color=colors[index],
                        alpha=0.2,
                        linewidth=0.0,
                        )

    # annotate the plot
    ax.set_xlabel(r'$t$ [ms]', labelpad=5, fontsize=12)
    ax.set_ylabel('error ratio [1]', fontsize=12)
    ax.set_xlim([-50., 200.])
    ax.set_ylim([0.0, 0.86])
    ax.legend(fontsize=11, loc=1)


def plotPSPs(ax, timeArray, vArray):
    """
    Plot the measured PSPs

    Keywords:
        --- ax: axes object
        --- timeArray: matrix with the time in the rows
        --- vArray: matrix with voltages in the rows
    """

    # Set up the plot
    core.show_axis(ax)
    core.make_spines(ax)

    # do the plotting
    for index in range(len(vArray[:,0])):
        ax.plot(timeArray[index,:],
                vArray[index,:],
                linewidth=1.,
                alpha=0.2,
                color='xkcd:blue')
    ax.set_xlabel(r't [ms]')
    ax.set_ylabel(r'memb. potential [mV]')
    ax.set_xlim([-10., 75.])
