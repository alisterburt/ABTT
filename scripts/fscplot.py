#!/usr/bin/env python
import sys

import click

sys.path.append("/mnt/storage/documents/IBS_PhD/programming/ABTT")
import ABTT.fsc.relion as relion_fsc


@click.command()
@click.option('--star', default='postprocess.star', help='star file output from relion_postprocess')
@click.option('--output', default='fscplot.png', help='filename in which to save figure (pdf, png, jpg, svg)')
@click.option('--hide_spines', default=True, help='hide the top and right spines which bound the axis?')
@click.option('--show_legend', default=True, help='show the legend on the plot?')
@click.option('--plot_cutoff_0143', default=True, help='plot cutoff at FSC = 0.143?')
@click.option('--plot_cutoff_05', default=True, help='plot cutoff at FSC = 0.5?')
@click.option('--plot_zero_line', default=True, help='plot line at FSC = 0?')
@click.option('--precision_reported_resolution', default=2,
              help='precision for reporting of resolution values in legend')
@click.option('--precision_resolution_axis', default=1, help='precision for the resolution values on the x-axis')
def main(star,
         output,
         hide_spines,
         show_legend,
         plot_cutoff_0143,
         plot_cutoff_05,
         plot_zero_line,
         precision_reported_resolution,
         precision_resolution_axis):
    plotter = relion_fsc.Plotter(star_file=star)
    plotter.plot(file_out=output,
                 hide_spines=hide_spines,
                 legend=show_legend,
                 plot_cutoff_0143=plot_cutoff_0143,
                 plot_cutoff_05=plot_cutoff_05,
                 plot_zero_line=plot_zero_line,
                 xaxis_precision=precision_resolution_axis,
                 reported_resolution_precision=precision_reported_resolution)


if __name__ == '__main__':
    main()
