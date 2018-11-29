import math
from operator import itemgetter
import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy.optimize import curve_fit

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


###################################################################
# shitty code begins here #########################################
###################################################################
def normalize_point(point, resolution, rx, ry=None):
    if ry is None:
        ry = rx
    image_centre = (resolution[0] // 2, resolution[1] // 2)
    point_vector = [image_centre[0] - point[0], point[1] - image_centre[1]]
    npv = [point_vector[0] / ry, point_vector[1] / rx]
    length = math.sqrt(npv[0]**2+npv[1]**2)
    return length



# polynomial calculation
real_distances = [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9, 10, -10, 11, -11, 12, -12, 13, -13]
real_angles = [math.atan(abs(x)/6) for x in real_distances]

points = [[320, 240],
          [282, 239], [357, 240],
          [247, 240], [394, 239],
          [214, 241], [424, 240],
          [188, 242], [451, 240],
          [166, 243], [471, 241],
          [147, 244], [489, 242],
          [133, 245], [503, 242],
          [122, 246], [514, 243],
          [113, 247], [523, 243],
          [106, 248], [530, 245],
          [100, 248], [536, 244],
          [95, 248], [541, 245],
          [90, 249], [545, 245]]


lengths = [normalize_point(p, (640, 480), 320-47, (320-47) * (480 / 640)) for p in points]


def f(x, a, b, c, d):
    return a*x**4 + b*x**3 + c*x**2 + d*x


print('lengths: ' + str(lengths))
coef, _ = curve_fit(f, lengths, real_angles)

xs = np.linspace(0, 1, 1000)
ys = [f(x, *coef) for x in xs]
plt.plot(xs, ys)
plt.show()
calculated_angles = []
lengths = [normalize_point(p, (640, 480), 320-47, (320-47)) for p in [[423, 376]]]
for l in lengths:
    angle = f(l, *coef)
    calculated_angles.append(angle)
calculated_distances = []
for a in calculated_angles:
    distance = 6 * math.tan(a)
    calculated_distances.append(distance)
print('calculated angles: ' + str(calculated_angles))
print('real angles: ' + str(real_angles))
print('calculated distances: ' + str(calculated_distances))
print('real distances: ' + str([abs(x) for x in real_distances]))

exit()
# Test
print("#######################################################################################")
real_locs = [(250, 440), (330, 130), (400, 310), (510, 440), (480, 190), (520, 90), (580, 150), (660, 400), (430, 20)]
rel_locs = [((a-40+18)/10, (b-300+5)/10) for (a, b) in real_locs]
real_dist = [math.sqrt(u**2+v**2) for (u, v) in rel_locs]
print('real dist: ' + str(real_dist))


path = "C:/Users/Lukasz1928/Desktop/inz/pomiary/probe_2/"
imgs = [cv2.imread('{}{}.jpg'.format(path, i)) for i in range(1, 10)]
shapes = [img.shape for img in imgs]
diodes_in_photo = [ParamsGenerator._find_diode(img) for img in imgs]
photo_centre = [750//2, 750//2]
circle_radius = math.sqrt((750/2 - 93)**2+(750/2 - 75)**2)
radiuses = []
for i in range(len(diodes_in_photo)):
    nd = normalize_point(diodes_in_photo[i], (750, 750), circle_radius, circle_radius * 480/640)
    radiuses.append(nd)
print('radiuses: ' + str(radiuses))
angles = [f(x, *coef) for x in radiuses]
print('angles: ' + str(angles))
calc_distances = [(185-37)/10 * math.tan(a) for a in angles]
print('calc dist: ' + str(calc_distances))