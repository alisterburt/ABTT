import numpy as np
from scipy.spatial.distance import pdist, squareform

from ABTT.io.dynamo import DynamoTable
from ABTT.io.star import StarDict


def particles_per_class(dynamo_table):
    """
    calculates the number of particles contributing to each unique class in a DynamoTable object
    :param dynamo_table: DynamoTable object
    :type dynamo_table: dynamo_table
    :return: class_particles: { class_index : n_particles }
    """
    class_indices = np.unique(dynamo_table['ref'])
    class_particles = StarDict

    for idx in class_indices:
        class_particles[idx] = np.sum(dynamo_table['ref'] == idx)

    return class_particles


def tomogram_distribution_per_class(dynamo_table):
    """
    calculates distribution of particles per tomogram per class
    :param dynamo_table: DynamoTable object
    :return: class_tomoidx_particles { class_index : { tomo_idx : n_particles } }_
    """
    class_indices = np.unique(dynamo_table['ref'])
    tomo_indices = np.unique(dynamo_table['tomo'])
    class_tomoidx_particles = {}

    for class_idx in class_indices:
        class_tomoidx_particles[class_idx] = {}
        for tomo_idx in tomo_indices:
            particles_in_class = dynamo_table['ref'] == class_idx
            particles_in_tomogram = dynamo_table['tomo'] == tomo_idx
            class_tomoidx_particles[class_idx][tomo_idx] = np.sum(particles_in_class and particles_in_tomogram)

    return class_tomoidx_particles


def table_per_tomogram(dynamo_table):
    """
    separates a table into dictionary of tables, one per tomogram, accessed by the tomogram index from the original table
    :param dynamo_table: DynamoTable object
    :type dynamo_table: DynamoTable
    :return: dict of DynamoTable objects { tomo_idx : DynamoTable }
    """
    tomo_indices = np.unique(dynamo_table['tomo'])
    dict_of_dynamo_tables = {}

    for tomo_idx in tomo_indices:
        row_idx_for_current_tomogram = dynamo_table['tomo'] == tomo_idx
        table_for_current_tomogram = DynamoTable
        for key in dynamo_table:
            table_for_current_tomogram[key] = dynamo_table[key][row_idx_for_current_tomogram]
        dict_of_dynamo_tables[tomo_idx] = table_for_current_tomogram

    return dict_of_dynamo_tables


def pairwise_distances(dynamo_table):
    """
    returns a squareform pairwise distance matrix for the xyz positions in a DynamoTable object
    :param dynamo_table: DynamoTable object
    :type DynamoTable: DynamoTable
    :return: pairwise_distance_matrix
    """
    xyz = dynamo_table['xyz']
    pairwise_distance_matrix = squareform(pdist(xyz, 'euclidean'))

    return pairwise_distance_matrix


def neighbours_in_range(dynamo_table, min_distance, max_distance):
    """
    computes the number of neighbours within a minimum and maximum distance per particle for a DynamoTable object
    :param dynamo_table: DynamoTable object
    :type dynamo_table: DynamoTable
    :param min_distance: minimum distance above which particles are considered neighbours
    :param max_distance: maximum distance below which particles are considered neighbours
    :return: neighbours_in_range_per_particle : m-element numpy array if xyz in dynamo table is mx3
    """
    pairwise_distance_matrix = pairwise_distances(dynamo_table)
    items_in_range = min_distance <= pairwise_distance_matrix < max_distance
    neighbours_in_range_per_particle = np.sum(items_in_range, 0)

    return neighbours_in_range_per_particle


def neighbourhood_analysis(dynamo_table, min_distance, max_distance, number_of_bins):
    """
    computes a per-particle neighbourhood analysis for a DynamoTable object
    neighbourhood analysis will be performed in equally sized, non-overlapping bins between the minimum and maximum distance
    :param dynamo_table: DynamoTable object
    :type dynamo_table: DynamoTable
    :param min_distance: minimum distance above which particles are considered neighbours
    :param max_distance: maximum distance below which particles are considered neighbours
    :param number_of_bins: number of equally spaced bins in which to measure number of neighbouring particles
    :return: neighbourhood_analysis_result, bin_centres, bin_minmax
    """

    bin_centres = np.linspace(min_distance, max_distance, number_of_bins)
    bin_width = np.abs(bin_centres[1] - bin_centres[0])
    minimum_values = bin_centres - (bin_width / 2.0)
    maximum_values = bin_centres + (bin_width / 2.0)

    bin_minmax = np.vstack((minimum_values, maximum_values)).transpose()

    pairwise_distance_matrix = pairwise_distances(dynamo_table)
    n_rows = pairwise_distance_matrix.shape[0]
    neighbourhood_analysis_result = np.zeros((n_rows, number_of_bins))

    for idx, bin in enumerate(bin_minmax):
        bin_minimum = bin[0]
        bin_maximum = bin[1]
        items_in_range = bin_minimum <= pairwise_distance_matrix < bin_maximum
        neighbours_in_range_per_particle = np.sum(items_in_range, 0)
        neighbourhood_analysis_result[:, idx] = neighbours_in_range_per_particle

    return neighbourhood_analysis_result, bin_centres, bin_minmax
