import os
import shutil
from glob import glob
from pathlib import Path

from omrdatasettools.CapitanImageGenerator import CapitanImageGenerator


class TestCapitanImageGenerator:
    def test_download_extract_and_draw_bitmaps(self, tmp_path):
        # Arrange
        image_generator = CapitanImageGenerator()
        data_directory = tmp_path / "capitan_raw"
        data_path = data_directory / "BimodalHandwrittenSymbols" / "data"
        data_path.parent.mkdir(parents=True, exist_ok=True)
        test_data = (Path(__file__).parent / "testdata" / "capitan_testdata.txt").read_text()
        data_path.write_text(test_data)

        # Act
        symbols = image_generator.load_capitan_symbols(data_directory)
        image_generator.draw_capitan_stroke_images(symbols, "temp/capitan_stroke", [3])
        image_generator.draw_capitan_score_images(symbols, "temp/capitan_score")

        # Assert
        all_stroke_images = [y for x in os.walk("temp/capitan_stroke") for y in glob(os.path.join(x[0], '*.png'))]
        all_score_images = [y for x in os.walk("temp/capitan_score") for y in glob(os.path.join(x[0], '*.png'))]
        assert len(all_stroke_images) == 3
        assert len(all_score_images) == 3

        # Cleanup
        shutil.rmtree("temp", ignore_errors=True)
