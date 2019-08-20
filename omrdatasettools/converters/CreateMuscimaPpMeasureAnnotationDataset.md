# Steps to reproduce the Muscima++ Measure Annotation dataset

1. Copy the [corrected MUSCIMA++ dataset](https://github.com/OMR-Research/muscima-pp/commit/bf9dc5e7c769751db8684aba0dea955105f77e3b) into `data/muscima_pp/v1.0/data/`
2. Run `python converters/MuscimaPpMeasureAnnotationExtractor.py`
3. Run `muscima_staves_json_to_coco_format_converter.py`
4. Run `MuscimaPlusPlusDatasetSplitter.py`