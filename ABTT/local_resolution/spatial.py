import logging

import numpy as np
from scipy.cluster.vq import whiten, kmeans2
from scipy.ndimage.morphology import distance_transform_edt

import ABTT.io.mrc as mrc
import ABTT.io.pdb as pdb


class SpatialLocRes:
    """
    An object for the analysis of local resolution distributions
    """

    def __init__(self, local_resolution_volume_file, mask_volume_file):
        logging.info("created an analysis object for assessing local resolution distribution")
        self.voxel_size = mrc.voxel_size(local_resolution_volume_file)
        self.local_resolution = mrc.data(local_resolution_volume_file)
        self.mask = mrc.data(mask_volume_file)

    def simple(self):
        """
        Gives the distribution of local resolution values everywhere that the mask is greater than 0.5
        :return: 1d numpy array
        """
        self.distribution_in_mask = self.local_resolution[self.mask > 0.5].reshape(-1)
        return self.distribution_in_mask

    def pdb_chain_array(self, pdb_file):
        """
        Gives an np.chararray of same shape as local resolution volume, filled with chain IDs at each atom position
        in the model
        :param pdb_file: pdb file from which to take chain IDs and atomic coordinates
        :return:
        """
        chain_array = np.zeros_like(self.local_resolution, dtype=str)
        voxel_size = float(self.voxel_size[0])

        for (chain, coord) in pdb.chains_coords(pdb_file):
            coord /= voxel_size
            indices = np.rint(coord)
            x = indices[0].astype(int)
            y = indices[1].astype(int)
            z = indices[2].astype(int)

            chain_array[z, y, x] += chain

        self.chain_array = chain_array

        return self.chain_array

    def unique_chains(self, pdb_file):
        """
        gets the unique chain IDs in the pdb file
        :param pdb_file: pdb file from which to get chain IDs
        :return: list of chain IDs
        """
        self.chains = pdb.unique_chains(pdb_file)

    def distribution_per_chain(self):
        """
        Gets the distribution of local resolution values for each chain on the chain array
        :return: dict { 'chain' : [local resolution values] }
        """
        distribution_per_chain = {}
        for chain in self.chains:
            mask = np.logical_and(self.mask > 0.5, self.chain_array == chain)
            local_resolution_distribution = self.local_resolution[mask].reshape(-1)
            distribution_per_chain[chain] = local_resolution_distribution
        self.distribution_per_chain = distribution_per_chain

    def fill_mask(self):
        """
        Assign each voxel inside the mask to the
        :return:
        """
        # Binarise array of chain IDs, 1 empty, 0 filled
        binary_array = self.chain_array == ''

        # Compute distance transform, outputting indices of nearest zero-element (i.e. where we have a chain ID)
        # output (for 3D cubic input) is a (3,N,N,N) array where (:,Z,Y,X) gives the indices for finding the nearest chain
        # in the chain array
        nearest_indices = distance_transform_edt(binary_array,
                                                 return_distances=False,
                                                 return_indices=True)

        # initialise output chain array and fill empty values with closest (in space) values from original chain array
        chain_array_filled = np.empty_like(chain_array)
        chain_array_filled = chain_array[nearest_indices[0], nearest_indices[1], nearest_indices[2]]
        chain_array_filled[mask <= 0.5] = ''

        self.chain_array = chain_array_filled

    def kmeans(self, number_of_clusters):
        """
        Groups local resolution values (inside a mask) into a number of clusters using kmeans clustering
        :param number_of_clusters: k for k-means clustering
        :return: (observations (z, y, x, local_res), label)
        """
        indices_to_consider = np.where(self.mask > 0.5)
        number_of_observations = len(indices_to_consider[0])
        observations = np.zeros((number_of_observations, 4), dtype=np.float16)
        # add spatial dimensions
        for dimension in range(3):
            observations[:, dimension] = indices_to_consider[dimension]

        # add local resolution
        observations[:, 3] = self.local_resolution[indices_to_consider]

        # normalise observations on a per feature basis prior to k-means
        observations_normalised = whiten(observations).astype(float)

        # perform k-means clustering
        centroids, labels = kmeans2(observations_normalised,
                                    k=number_of_clusters,
                                    minit='points')

        self.kmeans_out = (observations, labels)
