import math

import cv2

from mrc.utils.maths import points_2d_sqr_distance, point_in_rectangle, rescale_rectangle


class ConnectedComponentsDetector:
    """
    Class responsible for detecting connected components.

    Intended for internal usage.
    """

    def detect(self, image, remove_background=True, remove_irrelevant=True):
        """
        Parameters
        ----------
        image : numpy.ndarray
            Image to detect blobs on. It must be in binary (two-valued) format.

        remove_background : bool, optional
            Should function ignore background. Default is True.

        remove_irrelevant : bool, optional
            Should function ignore tiny specks, most probably reflections. Default is True.
            Parameter is ignored if `remove_background` is False.

        Returns
        -------
        list of array-like, list of array-like
            First one is list of five-element lists, containing info about connected component.
            Second one is list of (x, y) localizations of centers of mass of connected component.

        """
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image)
        stats_list = stats.tolist()
        centroids_list = centroids.tolist()
        if remove_background:
            background_component_index = self._get_background_component_index(image, stats, centroids)
            stats_list.pop(background_component_index)
            centroids_list.pop(background_component_index)
        if remove_irrelevant and remove_background:
            irrelevant_indexes = self._get_irrelevant_components_indexes(stats_list, centroids_list, 500, 25)
            stats_list = [stats_list[i] for i in range(len(stats_list)) if i not in irrelevant_indexes]
            centroids_list = [centroids_list[i] for i in range(len(centroids_list)) if i not in irrelevant_indexes]
        return stats_list, centroids_list

    def _get_background_component_index(self, image, stats, centroids):
        image_centre = (image.shape[0] / 2, image.shape[1] / 2)
        areas = [s[cv2.CC_STAT_HEIGHT] * s[cv2.CC_STAT_WIDTH] for s in stats]
        max_area = max(areas)
        max_indexes = [i for i, a in enumerate(areas) if a == max_area]
        distances_to_centre = [points_2d_sqr_distance(image_centre, centroids[mid]) for mid in max_indexes]
        min_distance_to_centre = min(distances_to_centre)
        min_dist_index = [max_indexes[i] for i, a in enumerate(distances_to_centre) if a == min_distance_to_centre]
        if len(min_dist_index) == 1:
            return min_dist_index[0]
        max_blob_area = max([s[cv2.CC_STAT_AREA] for s in stats])
        background_component = [i for i, s in enumerate(stats) if s[cv2.CC_STAT_AREA] == max_blob_area]
        return background_component[0]

    @staticmethod
    def _point_not_used(pt, diode_indexes, stats):
        for index in diode_indexes:
            if point_in_rectangle(pt, (stats[index][cv2.CC_STAT_LEFT], stats[index][cv2.CC_STAT_TOP]),
                                  (stats[index][cv2.CC_STAT_WIDTH], stats[index][cv2.CC_STAT_HEIGHT])):
                return False
        return True

    @staticmethod
    def _point_not_used_restrictive(pt, rescaled_components):
        for (tl, s) in rescaled_components:
            if point_in_rectangle(pt, tl, s):
                return False
        return True

    def _get_irrelevant_components_indexes(self, stats, centroids, diode_threshold, not_diode_threshold):
        if len(stats) == 0:
            return []
        s, c, indexes = (list(t) for t in
                         zip(*sorted(zip(stats, centroids, list(range(len(stats)))),
                                     key=lambda x: x[0][cv2.CC_STAT_HEIGHT] * x[0][cv2.CC_STAT_WIDTH],
                                     reverse=True)))

        rescaled_components_stats = []
        diode_indexes = []
        i = 0
        while i < len(c) and s[i][cv2.CC_STAT_HEIGHT] * s[i][cv2.CC_STAT_WIDTH] >= diode_threshold:
            if self._point_not_used(c[i], diode_indexes, s):
                diode_indexes.append(i)
                rescaled_components_stats.append(
                    tuple(rescale_rectangle((s[i][cv2.CC_STAT_LEFT], s[i][cv2.CC_STAT_TOP]),
                                            (s[i][cv2.CC_STAT_WIDTH], s[i][cv2.CC_STAT_HEIGHT]), math.sqrt(2))))
            i += 1
        while i < len(c) and s[i][cv2.CC_STAT_HEIGHT] * s[i][cv2.CC_STAT_WIDTH] >= not_diode_threshold:
            if self._point_not_used_restrictive(c[i], rescaled_components_stats):
                diode_indexes.append(i)
            i += 1
        return [indexes[i] for i in list(set(range(len(stats))) - set(diode_indexes))]
