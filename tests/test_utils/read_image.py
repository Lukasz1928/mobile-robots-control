import cv2


def read_image(name):
    image = cv2.imread('tests/resources/{}'.format(name))
    return image
