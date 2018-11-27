import wiringpi


class WS2811:
    def __init__(self, rgb, spi_ch=1, spi_speed=2000000):
        self._verify_color(rgb)
        self.rgb = {
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2]
        }
        self.spi_ch = spi_ch
        self.spi_speed = spi_speed
        wiringpi.wiringPiSetupGpio()
        wiringpi.wiringPiSPISetup(self.spi_ch, self.spi_speed)

    def __call__(self):
        self.send_color_via_spi()

    def __setitem__(self, key, value):
        if type(value) is int and value in range(0, 256) and key in ['r,g,b']:
            self.rgb[key] = value
        else:
            raise ValueError("value must be from range 0-255 and keys must be from 'r','g','b'")

    @staticmethod
    def _verify_color(rgb):
        if len(rgb) != 3:
            raise ValueError("Length of color must be 3, found {}".format(len(rgb)))
        for color in rgb:
            if color not in range(256):
                raise ValueError("Diode colors must be an iterable structure [r,g,b] for rgb in ranges 0,255")
        return True

    def send_color_via_spi(self):
        values = [self.rgb['r'], self.rgb['g'], self.rgb['b']]
        wiringpi.wiringPiSPIDataRW(self.spi_ch, bytes(values))

    def change_color(self, rgb):
        self._verify_color(rgb)
        self.rgb['r'] = rgb[0]
        self.rgb['g'] = rgb[1]
        self.rgb['b'] = rgb[2]
        self.send_color_via_spi()

