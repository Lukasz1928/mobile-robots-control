import math
import cv2
import numpy as np
from mrc.localization.camera.projections import projections


class DataSizeException(Exception):
    pass


class ParamsGenerator:

    def __init__(self, photos, coordinates, photo_centres, height_difference):
        if len(photos) != len(coordinates) or len(photos) != len(photo_centres):
            raise DataSizeException
        self.photos = photos
        self.coordinates = coordinates
        self.h = height_difference
        self.photo_centres = photo_centres

    def get_parameters(self):
        diodes_in_reality = self.coordinates
        distances_in_reality = [self._vector_length(v) for v in diodes_in_reality]
        thetas = [math.atan(rd / self.h) for rd in distances_in_reality]

        diodes_in_photo = [self._find_diode(img) for img in self.photos]
        diodes_in_photo_vectors = [
            (diodes_in_photo[i][0] - self.photo_centres[i][0], self.photo_centres[i][1] - diodes_in_photo[i][1]) for i
            in range(len(diodes_in_photo))]
        diodes_in_photo_normalized_vectors = [self._normalize_vector(v, self.photos[i].shape) for i, v in
                                              enumerate(diodes_in_photo_vectors)]
        normalized_vector_lengths = [self._vector_length(v) for v in diodes_in_photo_normalized_vectors]

        calculated_focals = [
            self._calculate_focal_length(p, normalized_vector_lengths, thetas) for p in
            projections]  # thetas: angle Ground-Camera-Diode
        selected_projection, focal, _ = np.min(calculated_focals, axis=2)
        return selected_projection, focal

    @staticmethod
    def _normalize_vector(vector, resolution):
        return vector[0] / resolution[0], vector[1] / resolution[1]

    @staticmethod
    def _find_diode(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        leds_image = cv2.inRange(gray_image, 225, 255)
        kpts = ParamsGenerator._prepare_blob_detector().detect(leds_image)
        return kpts[0].pt

    @staticmethod
    def _prepare_blob_detector():
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByCircularity = True
        params.minCircularity = 0.5
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByArea = True
        params.maxArea = 250
        params.minArea = 10
        detector = cv2.SimpleBlobDetector_create(params)
        return detector

    @staticmethod
    def _vector_length(v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    @staticmethod
    def _calculate_focal_length(projection, normalised_vector_lengths, theta):
        res = []
        for r, t in zip(normalised_vector_lengths, theta):
            res.append(projection.focal(t, r))
        return projection, np.mean(res), np.std(res)
