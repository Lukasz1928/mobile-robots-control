import cv2


def read_image(i):
    image = cv2.imread('tests/resources/localization/diode_detector/{}.jpg'.format(i))
    return image
