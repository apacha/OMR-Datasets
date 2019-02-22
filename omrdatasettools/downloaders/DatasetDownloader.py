import os
import shutil
import urllib.parse as urlparse
import urllib.request as urllib2
from zipfile import ZipFile
from abc import ABC, abstractmethod

from tqdm import tqdm


class DatasetDownloader(ABC):
    """ The abstract base class for classes that download a specific dataset """

    @abstractmethod
    def download_and_extract_dataset(self,
                                     destination_directory: str):
        """ Starts the download of the dataset and extracts it into the directory specified in the constructor
            :param destination_directory: The root directory, into which the data will be placed.
        """
        pass

    @abstractmethod
    def get_dataset_download_url(self) -> str:
        """ Returns the URL, where this dataset can be downloaded from directy """
        pass

    @abstractmethod
    def get_dataset_filename(self) -> str:
        """ Returns the filename for the ZIP-file that will be downloaded for this dataset """
        pass

    @staticmethod
    def copytree(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                DatasetDownloader.copytree(s, d)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    def extract_dataset(self, absolute_path_to_folder: str, dataset_filename: str = None):
        if dataset_filename is None:
            dataset_filename = self.get_dataset_filename()

        archive = ZipFile(dataset_filename, "r")
        archive.extractall(absolute_path_to_folder)
        archive.close()

    def clean_up_temp_directory(self, temp_directory):
        print("Deleting temporary directory {0}".format(temp_directory))
        shutil.rmtree(temp_directory, ignore_errors=True)

    def download_file(self, url, destination_filename=None) -> str:
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
