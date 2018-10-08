from typing import List

from mrc.localization.color.analyser import Analyser
from mrc.localization.color.values import ColorValue


class Extractor:
    def __init__(self, image, blob_coordinates):
        self.image = image
        self.blob_coordinates = blob_coordinates
        self.analyser = Analyser()

    def extract(self) -> List[ColorValue]:
        results = []
        for chunk in self._chop_blobs():
            results.append(self._execute_analysis(chunk))
        return results

    def _execute_analysis(self, chunk) -> ColorValue:
        analysis = Analyser().analyse_chunk(chunk)
        max_value = -1
        final_color = None
        for key in analysis.keys():
            if analysis[key] > max_value:
                max_value = analysis[key]
                final_color = key
        return final_color

    def _chop_blobs(self) -> List:
        result = []
        for ((x, y), r) in self.blob_coordinates:
            x = int(x)
            y = int(y)
            r = int(r)
            result.append(self.image[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r])
        return result
