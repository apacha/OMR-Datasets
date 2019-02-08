import argparse
from glob import glob
import os
import urllib.request

from lxml import etree
from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader
from tqdm import tqdm


class EdiromDatasetDownloader(DatasetDownloader):
    """ Loads and extracts an Edirom dataset.
        All rights reserved
    """

    def __init__(self, dataset: str):
        if dataset not in ["Bargheer", "FreischuetzDigital"]:
            raise Exception("Invalid dataset specified. Must be either 'Bargheer' or 'FreischuetzDigital'")
        self.dataset = dataset

    def get_dataset_download_url(self) -> str:
        if self.dataset == "Bargheer":
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Bargheer.zip"
        elif self.dataset == "FreischuetzDigital":
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/FreischuetzDigital.zip"

    def get_dataset_filename(self) -> str:
        if self.dataset == "Bargheer":
            return "Bargheer.zip"
        elif self.dataset == "FreischuetzDigital":
            return "FreischuetzDigital.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print(f"Downloading {self.dataset} Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print(f"Extracting {self.dataset} Dataset...")
        self.extract_dataset(destination_directory)

    def download_images_from_mei_annotation(self, dataset_directory: str, base_url: str):
        if len(glob(f'{dataset_directory}/{self.dataset}/*.xml')) == 0:
            print(
                f"Could not find MEI (XML) files in {dataset_directory}/{self.dataset}/ directory. Can't download images.")

        for source in glob(f'{dataset_directory}/{self.dataset}/*.xml'):
            base = os.path.splitext(source)[0]
            os.makedirs(base, exist_ok=True)
            print("Downloading dataset for " + base)
            self._download_images(base, base_url, source)

    def _download_images(self, base, base_url, source):
        xml = etree.parse(source).getroot()

        for graphic in tqdm(xml.xpath('//*[local-name()="graphic"]'), desc="Downloading images"):
            url = graphic.get('target')
            filename = os.path.basename(url)
            width = graphic.get('width')
            if os.path.exists(os.path.join(base, filename)):
                pass  # Skipping download, because it has been downloaded already
            else:
                urllib.request.urlretrieve(f"{base_url}/{url}?dw={width}&amp;mo=fit", os.path.join(base, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads a dataset from the Edirom system')
    parser.add_argument('-dataset', dest='dataset', type=str, required=True,
                        help='Must be either "Bargheer" or "FreischuetzDigital"')
    parser.add_argument('-url', dest='url', type=str, required=True,
                        help='URL where to download the dataset from. Must be provided manual to prevent automatic '
                             'crawling. Please contact the authors if you want to know the URLs.')
    parser.add_argument("--dataset_directory", type=str, default="../data",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    if flags.dataset not in ["Bargheer", "FreischuetzDigital"]:
        raise Exception("Invalid dataset specified. Must be either 'Bargheer' or 'FreischuetzDigital'")

    dataset_downloader = EdiromDatasetDownloader(flags.dataset)
    dataset_downloader.download_and_extract_dataset(os.path.join(flags.dataset_directory, flags.dataset))
    dataset_downloader.download_images_from_mei_annotation(flags.dataset_directory, flags.url)
