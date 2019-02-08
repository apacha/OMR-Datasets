import argparse
import json
import os
from glob import glob

from lxml import etree
from tqdm import tqdm


class EdiromAnnotationConverter:
    def convert_annotations_to_one_json_file_per_image(dataset_directory: str, dataset: str):
        if len(glob(f'{dataset_directory}/{dataset}/*.xml')) == 0:
            print(f"Could not find MEI (XML) files in {dataset_directory}/{dataset}/ directory.")

        for source in glob(f'{dataset_directory}/{dataset}/*.xml'):
            base = os.path.splitext(source)[0]
            os.makedirs(base, exist_ok=True)
            xml = etree.parse(source).getroot()

            # Extract bar annotations
            for surface in tqdm(xml.xpath('//*[local-name()="surface"]'),
                                desc=f"Creating json annotations for {base} subset"):
                image_path = os.path.join(base, surface[0].get('target').split('/')[-1])
                size = (int(surface[0].get('width')), int(surface[0].get('height')))

                json_path = os.path.splitext(image_path)[0] + '.json'

                system_measures = []
                for zone in surface.xpath('./*[local-name()="zone"][@type="measure"]'):
                    left = int(zone.get('ulx'))
                    top = int(zone.get('uly'))
                    right = int(zone.get('lrx'))
                    bottom = int(zone.get('lry'))

                    data = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                    system_measures.append(data)

                # Currently, the dataset only has system measure annotation, so we leave the other two types empty
                stave_measures = []
                staves = []
                with open(json_path, 'w') as file:
                    json.dump({'width': size[0], 'height': size[1], 'system_measures': system_measures,
                               'stave_measures': stave_measures, 'staves': staves}, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads a dataset from the Edirom system')
    parser.add_argument('-dataset', dest='dataset', type=str, required=True,
                        help='Must be either "Bargheer" or "FreischuetzDigital"')
    parser.add_argument("--dataset_directory", type=str, default="../data",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    if flags.dataset not in ["Bargheer", "FreischuetzDigital"]:
        raise Exception("Invalid dataset specified. Must be either 'Bargheer' or 'FreischuetzDigital'")

    EdiromAnnotationConverter.convert_annotations_to_one_json_file_per_image(flags.dataset_directory, flags.dataset)
