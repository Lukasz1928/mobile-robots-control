import math

import cv2
import numpy as np


def r1(theta, f):
    return 2 * f * math.tan(theta / 2)


def r2(theta, f):
    return f * theta


def r3(theta, f):
    return 2 * f * math.sin(theta / 2)


def r4(theta, f):
    return f * math.tan(theta)


def f1(theta, r):
    return r / (2 * math.tan(theta / 2))


def f2(theta, r):
    return r / theta


def f3(theta, r):
    return r / (2 * math.sin(theta / 2))


def f4(theta, r):
    return r / math.sin(theta)


def th1(r, f):
    return 2 * math.atan(r / (2 * f))


def th2(r, f):
    return r / f


def th3(r, f):
    return 2 * math.asin(r / (2 * f))


def th4(r, f):
    return math.asin(r / f)


functions_r = [r1, r2, r3, r4]
functions_f = [f1, f2, f3, f4]
functions_t = [th1, th2, th3, th4]


class ParamsGenerator:
    def __init__(self, photos, coordinates, height_difference, photo_centres):
        if len(photos) != len(coordinates):
            raise Exception("TODO")  # TODO: Zrup to
        self.photos = photos
        self.coordinates = coordinates
        self.h = height_difference
        self.photo_centres = photo_centres

    def get_parameters(self):
        diodes_in_photo = [self._find_diode(img) for img in self.photos]
        diodes_in_reality = self.coordinates
        distances_in_reality = [self._vector_length(v) for v in diodes_in_reality]
        thetas = [math.atan(rd / self.h) for rd in distances_in_reality]
        diodes_in_photo_vectors = [
            (diodes_in_photo[i][0] - self.photo_centres[i][0], self.photo_centres[i][1] - diodes_in_photo[i][1]) for i
            in range(len(diodes_in_photo))]
        diodes_in_photo_normalized_vectors = [self._normalize_vector(v, self.photos[i].shape) for i, v in
                                              enumerate(diodes_in_photo_vectors)]
        normalized_vector_lengths = [self._vector_length(v) for v in diodes_in_photo_normalized_vectors]
        calculated_focals = [
            self._calcualte_focal_length(f, normalized_vector_lengths, thetas) for f in
            functions_f]  # thetas: angle Ground-Camera-Diode
        selected_function = np.min(calculated_focals, axis=1)

    def _normalize_vector(self, vector, resolution):
        return (vector[0] / resolution[0], vector[1] / resolution[1])

    def _calculate_diode_location(self, diode, function):
        return

    def _find_diode(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        leds_image = cv2.inRange(gray_image, 225, 255)
        kpts = self.prepare_blob_detector().detect(leds_image)
        return kpts[0].pt

    def prepare_blob_detector(self):
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

    def _vector_length(self, v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def _calcualte_focal_length(self, function, normalised_vector_lengths, theta):
        res = []
        for r, t in zip(normalised_vector_lengths, theta):
            res.append(function(t, r))
        return np.mean(res), np.std(res), function.__name__
