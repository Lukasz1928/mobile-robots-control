import cv2


class Extractor:
    def __init__(self, analyser):
        self.analyser = analyser

    def extract(self, image, blob_coordinates):
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
