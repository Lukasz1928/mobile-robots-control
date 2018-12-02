import cv2


class Extractor:
    """
    Class responsible for extracting all colors in whole image.

    Intended for internal usage.
    """

    def __init__(self, analyser):
        """
        Parameters
        ----------
        analyser : `mrc.localization.color.kmeans.Analyser`
            Instance of Analyser.
        """
        self.analyser = analyser

    def extract(self, image, blob_coordinates):
        """
        Function extracting colors from image in given blob coordinates.

        Parameters
        ----------
        image : `ndarray`
            Numpy array representing BGR image.
        blob_coordinates : ((`float`, `float`), `float`)
            ((x, y), r), where (x,y) are coordinates of blob centers and r is their radius.

        Returns
        -------
        `list` of `str`
            List of color names.
        """
        _image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return [self._execute_analysis(chunk) for chunk in self._chop_blobs(_image, blob_coordinates)]

    def _execute_analysis(self, chunk):
        analysis = self.analyser.analyse_chunk(chunk)
        max_value = -1
        final_color = None
        for key, value in analysis.items():
            if value > max_value:
                max_value = value
                final_color = key
        return final_color

    def _chop_blobs(self, image, blob_coordinates):
        result = []
        for ((x, y), r) in blob_coordinates:
            x, y, r = [int(cord) for cord in (x, y, r)]
            result.append(image[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r])
        return result
