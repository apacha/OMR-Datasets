import argparse
import os
from glob import glob
from typing import List
from tqdm import tqdm

from omrdatasettools.image_generators.CapitanSymbol import CapitanSymbol
from omrdatasettools.image_generators.ExportPath import ExportPath
from omrdatasettools.image_generators.HomusSymbol import HomusSymbol


class CapitanImageGenerator:
    def create_capitan_images(self, raw_data_directory: str,
                              destination_directory: str,
                              stroke_thicknesses: List[int]) -> None:
        """
        Creates a visual representation of the Capitan strokes by parsing all text-files and the symbols as specified
        by the parameters by drawing lines that connect the points from each stroke of each symbol.

        :param raw_data_directory: The directory, that contains the raw capitan dataset
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """
        symbols = self.load_capitan_symbols(raw_data_directory)
        self.draw_capitan_stroke_images(symbols, destination_directory, stroke_thicknesses)
        self.draw_capitan_score_images(symbols, destination_directory)

    def load_capitan_symbols(self, raw_data_directory: str) -> List[CapitanSymbol]:
        data_path = os.path.join(raw_data_directory, "BimodalHandwrittenSymbols", "data")
        with open(data_path) as file:
            data = file.read()

        symbol_strings = data.splitlines()
        symbols = []
        for symbol_string in tqdm(symbol_strings, desc="Loading symbols from strings"):
            symbol = CapitanSymbol.initialize_from_string(symbol_string)
            symbols.append(symbol)

        return symbols

    def draw_capitan_stroke_images(self, symbols: List[CapitanSymbol],
                                   destination_directory: str,
                                   stroke_thicknesses: List[int]) -> None:
        """
        Creates a visual representation of the Capitan strokes by drawing lines that connect the points
        from each stroke of each symbol.

        :param symbols: The list of parsed Capitan-symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """

        total_number_of_symbols = len(symbols) * len(stroke_thicknesses)
        output = "Generating {0} images with {1} symbols in {2} different stroke thicknesses ({3})".format(
            total_number_of_symbols, len(symbols), len(stroke_thicknesses), stroke_thicknesses)

        print(output)
        print("In directory {0}".format(os.path.abspath(destination_directory)), flush=True)

        progress_bar = tqdm(total=total_number_of_symbols, mininterval=0.25, desc="Rendering strokes")
        capitan_file_name_counter = 0
        for symbol in symbols:
            capitan_file_name_counter += 1
            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = "capitan-{0}-{1}-stroke".format(symbol.symbol_class,
                                                                              capitan_file_name_counter)

            for stroke_thickness in stroke_thicknesses:
                export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension,
                                         'png', stroke_thickness)
                symbol.draw_capitan_stroke_onto_canvas(export_path, stroke_thickness, 0)
                progress_bar.update(1)

        progress_bar.close()

    def draw_capitan_score_images(self, symbols: List[CapitanSymbol],
                                  destination_directory: str) -> None:
        """
        Draws the image data contained in each symbol

        :param symbols: The list of parsed Capitan-symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """

        total_number_of_symbols = len(symbols)
        output = "Generating {0} images from Capitan symbols".format(len(symbols))

        print(output)
        print("In directory {0}".format(os.path.abspath(destination_directory)), flush=True)

        progress_bar = tqdm(total=total_number_of_symbols, mininterval=0.25, desc="Rendering images")
        capitan_file_name_counter = 0
        for symbol in symbols:
            capitan_file_name_counter += 1
            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = "capitan-{0}-{1}-score".format(symbol.symbol_class,
                                                                             capitan_file_name_counter)

            export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension, 'png')
            symbol.draw_capitan_score_bitmap(export_path)
            progress_bar.update(1)

        progress_bar.close()

    @staticmethod
    def add_arguments_for_homus_image_generator(parser: argparse.ArgumentParser):
        parser.add_argument("-s", "--stroke_thicknesses", dest="stroke_thicknesses", default="3",
                            help="Stroke thicknesses for drawing the generated bitmaps. May define comma-separated list"
                                 " of multiple stroke thicknesses, e.g. '1,2,3'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/capitan_raw",
        help="The directory, where the raw HOMUS dataset can be found (the text-files that contain the strokes)")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")

    image_generator = CapitanImageGenerator()
    image_generator.add_arguments_for_homus_image_generator(parser)

    flags, unparsed = parser.parse_known_args()

    image_generator.create_capitan_images(flags.raw_dataset_directory, flags.image_dataset_directory,
                                          [int(s) for s in flags.stroke_thicknesses.split(',')])
