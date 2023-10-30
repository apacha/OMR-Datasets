from pathlib import Path

import pytest

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset

LARGE_DATASET_REASON = "Downloads a large dataset"

SKIP_LARGE_TESTS = True
""" Global flag to enable/disable large dataset download tests """


class TestDownloader:

    def test_download_correct_url_resolution(self):
        dataset = OmrDataset.Audiveris
        url = dataset.get_dataset_download_url()
        assert url == "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudiverisOmrDataset.zip"

    def test_filename_extraction(self):
        dataset = OmrDataset.Audiveris
        filename = dataset.get_dataset_filename()
        assert filename == "AudiverisOmrDataset.zip"

    @pytest.mark.parametrize(
        ["dataset", "expected_number_of_samples", "target_glob_expression"],
        [
            (OmrDataset.Audiveris, 4, "*.png"),
            (OmrDataset.Capitan, 1, "data"),
            (OmrDataset.Baro, 212, "*.txt"),
            (OmrDataset.Fornes, 4094, "*.bmp"),
            (OmrDataset.Edirom_Bargheer, 9, "*.xml"),
            (OmrDataset.Edirom_FreischuetzDigital, 15, "*.xml"),
            (OmrDataset.Homus_V1, 15200, "*.txt"),
            (OmrDataset.Homus_V2, 15200, "*.txt"),
            # number_of_samples_with_staff_lines + number_of_samples_without_staff_lines + extra_files
            (OmrDataset.MuscimaPlusPlus_V1, 140 + 140 + 1, "*.xml"),
            (OmrDataset.MuscimaPlusPlus_V1, 140, "*.png"),
            # number_of_samples_with_staff_lines + extra_files
            (OmrDataset.MuscimaPlusPlus_V2, 140 + 1, "*.xml"),
            (OmrDataset.MuscimaPlusPlus_V2, 140, "*.png"),
            (OmrDataset.MuscimaPlusPlus_MeasureAnnotations, 144, "*.json"),
            (OmrDataset.OpenOmr, 706, "*.png"),
            (OmrDataset.Printed, 213, "*.png"),
            (OmrDataset.Rebelo1, 7940, "*.png"),
            (OmrDataset.Rebelo2, 7307, "*.png"),
            (OmrDataset.DeepScores_V1_Extended_100_Pages, 200, "*.png"),
            (OmrDataset.ChoiAccidentals, 2955, "*.jpg"),
            (OmrDataset.OpenScoreLieder, 1356, "*.mscx"),
            (OmrDataset.OpenScoreStringQuartets, 106, "*.mscx"),
            # Only run the following tests, if you have time to kill or before a new release
            pytest.param(OmrDataset.AudioLabs_v1, 43, "*.csv",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.AudioLabs_v2, 129, "*.csv",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.CvcMuscima_WriterIdentification, 3000, "*.png",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.DeepScores_V1_Extended, 3408, "*.png",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.DeepScores_V2_Dense, 5142, "*.png",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.CvcMuscima_StaffRemoval, 36000, "*.png",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.CvcMuscima_MultiConditionAligned, 10000, "*.png",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.MScoreLib_All, 4721, "*.mxl",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.MScoreLib_Prokofiev, 1153, "*.mxl",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
            pytest.param(OmrDataset.MScoreLib_Scriabin, 825, "*.mxl",
                         marks=pytest.mark.skipif(SKIP_LARGE_TESTS, reason=LARGE_DATASET_REASON)),
        ]
    )
    def test_download_of_all_dataset(
            self,
            dataset: OmrDataset,
            expected_number_of_samples: int,
            target_glob_expression: str,
            tmp_path: Path):
        # Arrange
        downloader = Downloader()
        destination_path = tmp_path / "output"
        download_path = tmp_path / "download"

        # Act
        downloader.download_and_extract_dataset(dataset, destination_path, download_path)

        # Assert
        all_files = list(tmp_path.rglob(target_glob_expression))
        actual_number_of_files = len(all_files)
        assert expected_number_of_samples == actual_number_of_files
        assert (download_path / dataset.get_dataset_filename()).exists()
