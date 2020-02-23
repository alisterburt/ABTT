import matplotlib.pyplot as plt
import numpy as np

import ABTT.math.spatial_frequency as spatial_frequency
import ABTT.plotting_utils.axis as axis_utils
import ABTT.plotting_utils.colours as colours
from ABTT.io.star import read as read_star


class Plotter:
    """
    plots the FSC from a RELION star file, optionally into a matplotlib axis object
    :param star_file: postprocess.star from RELION
    :return:
    """

    def __init__(self, star_file):
        star_dicts = read_star(star_file)
        self.fsc_dict = star_dicts['data_fsc']
        self.fpix_extent = self.get_fpix_extent()
        self.box_size = self.get_box_size()
        self.apix = self.get_apix()
        self.fpix_05 = self.get_fpix_at_cutoff(0.5)
        self.resolution_05 = self.get_resolution_at_cutoff(0.5)
        self.fpix_0143 = self.get_fpix_at_cutoff(0.143)
        self.resolution_0143 = self.get_resolution_at_cutoff(0.143)
        self.colours = colours.generate_categorical_colourblind(3)

    def plot(self, ax=None,
             hide_spines=True,
             legend=True,
             plot_cutoff_0143=True,
             plot_cutoff_05=True,
             plot_zero_line=True,
             xaxis_precision=1,
             reported_resolution_precision=2,
             file_out=None):

        # Which axis should I plot in?
        if ax is None:
            fig, ax = plt.subplots()
            fig.set_size_inches(13, 8)
        else:
            fig = plt.gcf()

        # Plot FSC curves
        fsc_linewidth = 4
        FSC_unmasked = ax.plot('rlnSpectralIndex', 'rlnFourierShellCorrelationUnmaskedMaps',
                               data=self.fsc_dict,
                               label='Unmasked FSC',
                               linestyle='--',
                               linewidth=fsc_linewidth,
                               c=self.colours[0],
                               zorder=10)

        FSC_phase_randomised = ax.plot('rlnSpectralIndex',
                                       'rlnCorrectedFourierShellCorrelationPhaseRandomizedMaskedMaps',
                                       data=self.fsc_dict,
                                       label='Phase-Randomised FSC',
                                       linestyle='--',
                                       linewidth=fsc_linewidth,
                                       c=self.colours[1],
                                       zorder=8)

        # FSC_masked = ax.plot('rlnSpectralIndex', 'rlnFourierShellCorrelationMaskedMaps',
        #                      data=self.fsc_dict,
        #                      label='Masked FSC',
        #                      linestyle='--',
        #                      linewidth=fsc_linewidth,
        #                      c='tab:blue',
        #                      zorder=20)

        FSC_corrected = ax.plot('rlnSpectralIndex', 'rlnFourierShellCorrelationCorrected',
                                data=self.fsc_dict,
                                label='Masked & Corrected FSC',
                                linestyle='-',
                                linewidth=fsc_linewidth,
                                c=self.colours[2],
                                zorder=15)
        # Adjust limits
        ax.set_xlim(0, self.fpix_extent)

        # plot horizontal line at 0
        if plot_zero_line:
            horizontal_0 = ax.axhline(0, linestyle='-', c='tab:gray', zorder=0, linewidth=3)

        # Change xticklabels to be in angstroms
        fig.canvas.draw()
        resolution_labels = []

        labels = ax.get_xticklabels()
        for label in labels:
            fpix = label.get_position()[0]
            resolution_angstrom = spatial_frequency.fpix2res(fpix, self.apix, self.box_size)
            resolution_labels.append(f'{resolution_angstrom:.{xaxis_precision}f}')

        ax.set_xticklabels(resolution_labels)

        # Add cutoffs 0.5, 0.143
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()
        cutoff_linecolor = 'tab:gray'
        cutoff_linestyle = ':'
        cutoff_linewidth = 3

        if plot_cutoff_05:
            cutoff_05 = ax.scatter(self.fpix_05, 0.5,
                                   marker='o',
                                   c='tab:gray',
                                   s=200,
                                   label=r'FSC$_{0.5}$ = ' + f'{self.resolution_05:.{reported_resolution_precision}f}',
                                   edgecolors='k',
                                   linewidths=2,
                                   zorder=50)

            fsc_05_v = ax.axvline(self.fpix_05, ymax=(0.5 - ymin) / (ymax - ymin),
                                  linestyle=cutoff_linestyle,
                                  zorder=1,
                                  linewidth=cutoff_linewidth,
                                  c=cutoff_linecolor)

            fsc_05_h = ax.axhline(0.5, xmax=(self.fpix_05 - xmin) / (xmax - xmin),
                                  linestyle=cutoff_linestyle,
                                  zorder=1,
                                  linewidth=cutoff_linewidth,
                                  c=cutoff_linecolor)

        if plot_cutoff_0143:
            cutoff_0143 = ax.scatter(self.fpix_0143, 0.143,
                                     marker='*',
                                     c='gold',
                                     s=300,
                                     label=r'FSC$_{0.143}$ = ' + f'{self.resolution_0143:.{reported_resolution_precision}f}',
                                     edgecolors='k',
                                     linewidths=2,
                                     zorder=50)

            fsc_0143_v = ax.axvline(self.fpix_0143, ymax=(0.143 - ymin) / (ymax - ymin),
                                    linestyle=cutoff_linestyle,
                                    zorder=1,
                                    linewidth=cutoff_linewidth,
                                    c=cutoff_linecolor)

            fsc_0143_h = ax.axhline(0.143, xmax=(self.fpix_0143 - xmin) / (xmax - xmin),
                                    linestyle=cutoff_linestyle,
                                    zorder=1,
                                    linewidth=cutoff_linewidth,
                                    c=cutoff_linecolor)

        # Label axes
        ax.set_xlabel(r"Resolution / $\AA$")
        ax.set_ylabel('Fourier Shell Correlation')

        # Resize axes labels and ticklabels
        axis_utils.change_axis_ticklabel_size(ax, 24)
        axis_utils.change_axis_label_size(ax, 28)

        # Hide spines and make sure remaining spines are on top
        if hide_spines:
            axis_utils.hide_spines(ax)

        axis_utils.raise_spines(ax)

        # Change axis and tick thickness
        axis_utils.change_axis_thickness(ax, 4)

        # Plot legend
        if legend:
            ax.legend(fontsize=14)

        # Save plot
        if file_out is not None:
            if any(file_out.endswith(extension) for extension in ('.svg', '.jpg', '.png', '.pdf')):
                plt.savefig(file_out)
            else:
                plt.savefig(file_out, format='svg')

    def get_fpix_at_cutoff(self, cutoff):
        """
        Finds the fpix number defined by the FSC at a given cutoff
        This function takes the last crossing in the case where there are multiple
        :param cutoff: float 0-1
        :return: fpix of FSC at cutoff
        """
        fsc = self.fsc_dict['rlnFourierShellCorrelationCorrected']
        fpix = self.fsc_dict['rlnSpectralIndex']

        # Get index into arrays where value is greater than defined cutoff
        greater_than_cutoff_idx = np.nonzero(fsc > cutoff)
        max_idx_gt_cutoff = np.amax(greater_than_cutoff_idx)

        # Get fpix value at cutoff by linear interpolation
        FSC_value_above_below_cutoff = fsc[[max_idx_gt_cutoff, max_idx_gt_cutoff + 1]]
        fpix_value_above_below_cutoff = fpix[[max_idx_gt_cutoff, max_idx_gt_cutoff + 1]]
        extent = (FSC_value_above_below_cutoff[0] - cutoff) / (
                    FSC_value_above_below_cutoff[0] - FSC_value_above_below_cutoff[1])
        fpix_value_at_cutoff = fpix_value_above_below_cutoff[0] + (
                    extent * (fpix_value_above_below_cutoff[1] - fpix_value_above_below_cutoff[0]))
        return fpix_value_at_cutoff

    def get_box_size(self):
        box_size = self.fsc_dict['rlnSpectralIndex'][-1] * 2
        return box_size

    def get_fpix_extent(self):
        fpix_extent = self.fsc_dict['rlnSpectralIndex'][-1]
        return fpix_extent

    def get_apix(self):
        apix = self.fsc_dict['rlnAngstromResolution'][-1] / 2.0
        return apix

    def get_resolution_at_cutoff(self, cutoff):
        fpix_at_cutoff = self.get_fpix_at_cutoff(cutoff)
        resolution = spatial_frequency.fpix2res(fpix_at_cutoff, self.apix, self.box_size)
        return resolution
