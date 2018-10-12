from typing import List

import cv2
from numpy import ndarray

from mrc.localization.color.analyser import Analyser
from mrc.localization.color.values import ColorValue


class Extractor:
    def __init__(self, image, blob_coordinates):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.blob_coordinates = blob_coordinates
        self.analyser = Analyser()
        self.analysis = None

    def extract(self) -> List[ColorValue]:
        results = []
        for chunk in self._chop_blobs():
            results.append(self._execute_analysis(chunk))
        return results

    def _execute_analysis(self, chunk: ndarray) -> ColorValue:
        self.analysis = Analyser().analyse_chunk(chunk)
        max_value = -1
        final_color = None
        for key in self.analysis.keys():
            if self.analysis[key] > max_value:
                max_value = self.analysis[key]
                final_color = key
        return final_color

    def _chop_blobs(self) -> List[ndarray]:
        result = []
        for ((x, y), r) in self.blob_coordinates:
            x, y, r = [int(cord) for cord in (x, y, r)]
            result.append(self.image[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r])
        return result
