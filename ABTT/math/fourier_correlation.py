import numpy as np
from numpy.fft import fftn, fftshift


class FSC:
    def __init__(self, image_one, image_two):
        """
        An object which allows the calculation of the fourier shell correlation between two images
        Images can be 2D or 3D
        """
        self.images = image_one, image_two
        self.image_dimensions = self._check_image_dimensions()
        self.center = self._get_center()
        self.spectral_indices = self._get_spectral_indices()
        self.fourier_transforms = self._compute_fourier_transforms()
        self.fourier_transforms = self._shift_fourier_transforms()

    def _compute_fourier_transforms(self):
        fourier_transforms = fftn(self.images[0]), fftn(self.images[1])
        return fourier_transforms

    def _check_image_dimensions(self):
        # Get dimensionality
        dim1 = self.images[0].shape
        dim2 = self.images[1].shape

        # Check for same dimensions between images
        message = f'image dimensions ({dim1}, {dim2}) are not the same'
        assert self.images[0].shape == self.images[1].shape, message

        # Check for square/cubic images
        message = f'image dimensions are {dim1} but images must be square/cubic'
        assert np.all(dim1 == dim1[0]), message

        # Check for even image size
        assert dim1[0] % 2 == 0

        # return image dimensions
        return dim1

    def _shift_fourier_transforms(self):
        shifted_fourier_transforms = fftshift(self.fourier_transforms[0]), fftshift(self.fourier_transforms[1])
        return shifted_fourier_transforms

    def _get_distance_meshgrid(self):
        """
        Returns a grid of distances from the center of the image
        :return:
        """
        indices = np.indices(self.image_dimensions)
        n_rows = np.prod(indices.shape[1:])
        indices_reshaped = indices.reshape((indices.shape[0], n_rows))
        positions = indices_reshaped - self.center
        distances = np.sqrt(np.sum(np.power(positions, 2), 0)).reshape(self.image_dimensions)

    def _get_center(self):
        center = self.image_dimensions / 2
        center.reshape((-1, 1))  # need shape (n,1) for broadcasting later
        return center

    def _get_spectral_indices(self):
        spectral_indices = np.arange(self.center[0])
        return spectral_indices
