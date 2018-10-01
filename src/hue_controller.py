from phue import Bridge, PhueException
import name_converter
from rgbxy import Converter
from name_converter import clean_name
import logging

saturation_val = 0
logging.basicConfig(level=logging.INFO,filename="hue_log.log",
                    format="%(asctime)s:%(levelname)s:%(message)s"	)
class HueController:

    def __init__(self):
        self.bridge = None
        self.light = None
        self.name_to_color = name_converter.NameConverter()

    def connect(self):
        if self.light is not None:
            return

        self.bridge = Bridge('10.76.100.161')
        self.bridge.connect()
        logging.info("Server has connected to the bridge")

        self.light = self.bridge.lights[1]

    def set_color(self, color_name):
        try:
            self.connect()
        except PhueException:
            logging.info("Server was unable to connect to Hue Light")
            return "I'm sorry, but I cannot connect to the Hue Light." \
                   "Please try again later."

        rgb_values = self.name_to_color.convert(color_name)

        if rgb_values is None:
            logging.info("Color " + color_name + " was not recognized.")
            return "I'm sorry, but I don't recognize " \
                   "the color {}".format(color_name)

        (r, g, b) = rgb_values
        converter = Converter()
        print(r, " ", g, " ", b)
        if r == 255 and b == 255 and g == 255:
            saturation_val = 0
            [x, y] = converter.rgb_to_xy(r, g, b)
        else:
            saturation_val = 255
            correction_value = 1.3
            r = ((r / 255) ** (1 / correction_value))
            g = ((g / 255) ** (1 / correction_value))
            b = ((b / 255) ** (1 / correction_value))
            [x, y] = converter.rgb_to_xy(r, g, b)

        try:
            self.light.xy = (x, y)
            self.light.saturation = saturation_val
            logging.info("The light was changed to the color {}."\
                .format(clean_name(color_name)))
            return "The light was changed to the color {}."\
                .format(clean_name(color_name))
        except PhueException:
            logging.info("Server was unable to connect to Hue Light.")
            return "I'm sorry, but I cannot connect to the Hue Light." \
                   "Please try again later."
