import math
from operator import itemgetter

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
        diodes_in_photo_vectors = [self._calculate_diode_vector(diodes_in_photo[i], self.photo_centres[i]) for i in
                                   range(len(diodes_in_photo))]
        diodes_in_photo_normalized_vectors = [self._normalize_vector(v, self.photos[i].shape) for i, v in
                                              enumerate(diodes_in_photo_vectors)]
        normalized_vector_lengths = [self._vector_length(v) for v in diodes_in_photo_normalized_vectors]

        calculated_focals = [
            list(self._calculate_focal_length(p, normalized_vector_lengths, thetas)) for p in
            projections]  # thetas: angle Ground-Camera-Diode
        selected_projection, focal, t = min(calculated_focals, key=itemgetter(2))
        return selected_projection, focal

    @staticmethod
    def _calculate_diode_vector(diode_in_photo, photo_centre):
        if diode_in_photo is not None:
            return diode_in_photo[0] - photo_centre[0], photo_centre[1] - diode_in_photo[1]
        return None

    @staticmethod
    def _normalize_vector(vector, resolution):
        if vector is not None:
            return vector[0] / resolution[0], vector[1] / resolution[1]
        return None

    @staticmethod
    def _find_diode(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        leds_image = cv2.inRange(gray_image, 225, 255)
        kpts = ParamsGenerator._prepare_blob_detector().detect(leds_image)
        if len(kpts) > 0:
            return kpts[0].pt
        return None

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
        params.minArea = 1
        detector = cv2.SimpleBlobDetector_create(params)
        return detector

    @staticmethod
    def _vector_length(v):
        if v is not None:
            return math.sqrt(v[0] ** 2 + v[1] ** 2)
        return None

    @staticmethod
    def _calculate_focal_length(projection, normalised_vector_lengths, theta):
        res = []
        for r, t in zip(normalised_vector_lengths, theta):
            if r is not None:
                res.append(projection.focal(t, r))
        return projection, np.mean(res), np.std(res)
