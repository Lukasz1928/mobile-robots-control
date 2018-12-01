import cv2
from unittest import TestCase
import numpy as np
from parameterized import parameterized
from mrc.localization.color.utils.color_converter import ColorConverter
from tests.test_utils.read_image import read_image


class TestColorConverterGrayscale(TestCase):
    def setUp(self):
        self.converter = ColorConverter()

        self.imageBGR = read_image('localization/color/utils/color_conversion/gray/source.png')
        self.imageRGB = cv2.cvtColor(self.imageBGR, cv2.COLOR_BGR2RGB)
        self.expected_grayscale = read_image('localization/color/utils/color_conversion/gray/gray.png')[:, :, 0]

    def test_BGR_to_Grayscale(self):
        grayscale = self.converter.convert_to_grayscale(self.imageBGR, 'BGR')
        self.assertTrue(np.array_equal(grayscale, self.expected_grayscale))

    def test_RGB_to_Grayscale(self):
        grayscale = self.converter.convert_to_grayscale(self.imageRGB, 'RGB')
        self.assertTrue(np.array_equal(grayscale, self.expected_grayscale))

    def test_BGR_to_Grayscale_special(self):
        grayscale = self.converter.convert_to_grayscale(self.imageBGR, 'BGR')
        self.assertTrue(np.array_equal(grayscale, self.expected_grayscale))

    def test_RGB_to_Grayscale_special(self):
        grayscale = self.converter.convert_to_grayscale(self.imageBGR, 'BGR')
        self.assertTrue(np.array_equal(grayscale, self.expected_grayscale))


class TestColorConverterBinary(TestCase):
    def setUp(self):
        self.converter = ColorConverter()

        self.imageBGR = read_image('localization/color/utils/color_conversion/binary/source.png')
        self.imageRGB = cv2.cvtColor(self.imageBGR, cv2.COLOR_BGR2RGB)
        self.expected_images = [read_image('localization/color/utils/color_conversion/binary/{}.png'.format(i))[:, :, 0] for i in
                                range(9)]

    @parameterized.expand([[i] for i in range(9)])
    def test_BGR_to_binary(self, i):
        binary = self.converter.convert_to_binary(self.imageBGR, i / 8 * 255, 'BGR')
        self.assertTrue(np.array_equal(binary, self.expected_images[i]))

    @parameterized.expand([[i] for i in range(9)])
    def test_RGB_to_binary(self, i):
        binary = self.converter.convert_to_binary(self.imageRGB, i / 8 * 255, 'RGB')
        self.assertTrue(np.array_equal(binary, self.expected_images[i]))
