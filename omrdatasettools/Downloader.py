import os
import shutil
import urllib
import urllib.parse as urlparse
import urllib.request as urllib2
from glob import glob
from zipfile import ZipFile

from lxml import etree
from tqdm import tqdm

from omrdatasettools.OmrDataset import OmrDataset


class Downloader:
    """ The class for downloading OMR datasets. It downloads the selected dataset from Github and extracts it to
        a specified directory.
    """

    def download_and_extract_dataset(self, dataset: OmrDataset, destination_directory: str):
        """ Starts the download of the dataset and extracts it into the specified directory.

        Examples
        --------
        >>> from omrdatasettools import Downloader, OmrDataset
        >>> downloader = Downloader()
        >>> downloader.download_and_extract_dataset(OmrDataset.HOMUS_V2, "data")

        """
        self.download_and_extract_custom_dataset(dataset.name, dataset.get_dataset_download_url(),
                                                 dataset.get_dataset_filename(), destination_directory)

        if dataset is OmrDataset.Fornes:
            self.__fix_capital_file_endings(os.path.join(os.path.abspath(destination_directory), "Music_Symbols"))

        if dataset in [OmrDataset.MuscimaPlusPlus_V1, OmrDataset.MuscimaPlusPlus_V2]:
            self.__download_muscima_pp_images(dataset, destination_directory)

    def download_and_extract_custom_dataset(self, dataset_name: str, dataset_url: str, dataset_filename: str,
                                            destination_directory: str):
        """ Starts the download of a custom dataset and extracts it into the specified directory.

        Examples
        --------
        >>> from omrdatasettools import Downloader
        >>> downloader = Downloader()
        >>> downloader.download_and_extract_custom_dataset("MyNewOmrDataset", "https://example.org/dataset.zip", "dataset.zip", "data/MyNewOmrDataset")

        """
        if not os.path.exists(dataset_filename):
            print("Downloading {0} dataset...".format(dataset_name))
            self.download_file(dataset_url, dataset_filename)

        print("Extracting {0} dataset...".format(dataset_name))
        self.extract_dataset(os.path.abspath(destination_directory), dataset_filename)

    def download_images_from_mei_annotation(self, dataset: OmrDataset, dataset_directory: str, base_url: str):
        """ Crawls the images of an Edirom dataset, if provided with the respective URL. To avoid repetitive crawling,
            this URL has to be provided manually. If you are interested in these datasets, please contact the authors.

            Examples
            --------
            >>> from omrdatasettools import Downloader, OmrDataset
            >>> downloader = Downloader()
            >>> downloader.download_and_extract_dataset(OmrDataset.Edirom_Bargheer, "data/Bargheer")
            >>> downloader.download_images_from_mei_annotation(OmrDataset.Edirom_Bargheer, "data/Bargheer", "INSERT_DATASET_URL_HERE")

            or

            >>> downloader.download_and_extract_dataset(OmrDataset.Edirom_FreischuetzDigital, "data/Freischuetz")
            >>> downloader.download_images_from_mei_annotation(OmrDataset.Edirom_FreischuetzDigital, "data/Freischuetz", "INSERT_DATASET_URL_HERE")
            """
        if dataset not in [OmrDataset.Edirom_Bargheer, OmrDataset.Edirom_FreischuetzDigital]:
            raise Exception("Only supported for edirom datasets")

        if len(glob(f'{dataset_directory}/*.xml')) == 0:
            print(
                f"Could not find MEI (XML) files in {dataset_directory}/ directory. Can't download images.")

        for source in glob(f'{dataset_directory}/*.xml'):
            base = os.path.splitext(source)[0]
            os.makedirs(base, exist_ok=True)
            print("Downloading dataset for " + base)
            self.__download_edirom_images(base, base_url, source)

    def __download_edirom_images(self, base, base_url, source):
        xml = etree.parse(source).getroot()

        for graphic in tqdm(xml.xpath('//*[local-name()="graphic"]'), desc="Downloading images"):
            url = graphic.get('target')
            filename = os.path.basename(url)
            width = graphic.get('width')
            if os.path.exists(os.path.join(base, filename)):
                pass  # Skipping download, because it has been downloaded already
            else:
                urllib.request.urlretrieve(f"{base_url}/{url}?dw={width}&amp;mo=fit", os.path.join(base, filename))

    def __download_muscima_pp_images(self, dataset: OmrDataset, destination_directory: str):
        # Automatically download the images and measure annotations with the MUSCIMA++ dataset
        muscima_pp_images_filename = dataset.dataset_file_names()["MuscimaPlusPlus_Images"]
        self.download_file(dataset.dataset_download_urls()["MuscimaPlusPlus_Images"], muscima_pp_images_filename)
        absolute_path_to_temp_folder = os.path.abspath('MuscimaPpImages')
        self.extract_dataset(absolute_path_to_temp_folder, muscima_pp_images_filename)
        if dataset is OmrDataset.MuscimaPlusPlus_V1:
            target_folder = os.path.join(os.path.abspath(destination_directory), "v1.0", "data", "images")
        if dataset is OmrDataset.MuscimaPlusPlus_V2:
            target_folder = os.path.join(os.path.abspath(destination_directory), "v2.0", "data", "images")
        self.copytree(os.path.join(absolute_path_to_temp_folder, "fulls"), target_folder)
        self.clean_up_temp_directory(absolute_path_to_temp_folder)

    def __fix_capital_file_endings(self, absolute_path_to_temp_folder):
        image_with_capital_file_ending = [y for x in os.walk(absolute_path_to_temp_folder) for y in
                                          glob(os.path.join(x[0], "*.BMP"))]
        for image in image_with_capital_file_ending:
            os.rename(image, image[:-3] + "bmp")

    @staticmethod
    def copytree(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                Downloader.__copytree(s, d)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    @staticmethod
    def extract_dataset(absolute_path_to_folder: str, dataset_filename: str):
        archive = ZipFile(dataset_filename, "r")
        archive.extractall(absolute_path_to_folder)
        archive.close()

    @staticmethod
    def clean_up_temp_directory(temp_directory):
        print("Deleting temporary directory {0}".format(temp_directory))
        shutil.rmtree(temp_directory, ignore_errors=True)

    @staticmethod
    def download_file(url, destination_filename=None) -> str:
        u = urllib2.urlopen(url)
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)
        if not filename:
            filename = 'downloaded.file'
        if destination_filename:
            filename = destination_filename

        filename = os.path.abspath(filename)

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
            print("Downloading: {0} Bytes: {1} into {2}".format(url, file_size, filename))

            with tqdm(total=file_size, desc="Downloading (bytes)") as progress_bar:
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    if file_size:
                        progress_bar.update(len(buffer))
            print()

        return filename
