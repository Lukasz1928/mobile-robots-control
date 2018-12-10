import wiringpi


class WS2811:
    def __init__(self, spi_ch=1, spi_speed=2000000):
        self.spi_ch = spi_ch
        self.spi_speed = spi_speed
        self.rgb = [0, 0, 0]
        wiringpi.wiringPiSetupGpio()
        wiringpi.wiringPiSPISetup(self.spi_ch, self.spi_speed)

    def send_color_via_spi(self):
        wiringpi.wiringPiSPIDataRW(self.spi_ch, bytes(self.rgb))

    def set_diode_color(self, rgb):
        self._verify_color(rgb)
        self.rgb = rgb
        self.send_color_via_spi()

    @staticmethod
    def _verify_color(rgb):
        if len(rgb) != 3:
            raise ValueError("Length of color must be 3, found {}".format(len(rgb)))
        for color in rgb:
            if color not in range(256):
                raise ValueError("Diode colors must be an iterable structure [r,g,b] for rgb in ranges 0,255")
