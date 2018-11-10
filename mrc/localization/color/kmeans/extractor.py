import cv2


class Extractor:
    def __init__(self, analyser):
        self.image = None
        self.blob_coordinates = None
        self.analyser = analyser
        self.analysis = None

    def extract(self, image, blob_coordinates):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.blob_coordinates = blob_coordinates
        return [self._execute_analysis(chunk) for chunk in self._chop_blobs()]

    def _execute_analysis(self, chunk):
        self.analysis = self.analyser.analyse_chunk(chunk)
        max_value = -1
        final_color = None
        for key in self.analysis.keys():
            if self.analysis[key] > max_value:
                max_value = self.analysis[key]
                final_color = key
        return final_color

    def _chop_blobs(self):
        result = []
        for ((x, y), r) in self.blob_coordinates:
            x, y, r = [int(cord) for cord in (x, y, r)]
            result.append(self.image[y - 2 * r:y + 2 * r, x - 2 * r:x + 2 * r])
        return result
