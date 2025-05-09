[![workflow pypi badge](https://img.shields.io/pypi/v/pycoeus.svg?colorB=blue)](https://pypi.python.org/project/pycoeus/) [![Documentation Status](https://readthedocs.org/projects/pycoeus/badge/?version=latest)](https://pycoeus.readthedocs.io/en/latest/?badge=latest) [![build](https://github.com/DroneML/pycoeus/actions/workflows/build.yml/badge.svg)](https://github.com/DroneML/pycoeus/actions/workflows/build.yml)

![icon](https://github.com/user-attachments/assets/a3da006f-b762-4248-9266-defa3e1d02ca)

# Pycoeus

Segment (georeferenced) raster data in an interactive fashion. Retrain models in seconds. Only small amounts of labeled data necessary because of our use of pretrained base models as feature extractors. Pycoeus can be used as a standalone commandline tool or as the backend for the QGIS plugin called CoeusAI.

The project setup is documented in [project_setup.md](devdocs/project_setup.md).

## Typical usage
Let's say you've got the image on the left, along with the labels (superimposed on the image) on the right.

![image](https://github.com/user-attachments/assets/08bcfd85-3042-4550-af8f-a142126e2428)
![image](https://github.com/user-attachments/assets/673f8416-1d1f-420f-9558-100d1d60c181)

You run the commandline tool as follows, selecting both input image and labels, the path where the output should be, and the type of features to use.

```console
python main.py --input image.tif --labels labels.tif --predictions output.tif
```

The resulting output looks like:

![image](https://github.com/user-attachments/assets/46d6629d-65df-4e4d-81f1-07bfef38ca57)

_To test this with our testdata, run:_
```console
python src/pycoeus/main.py --input tests/test_data/test_image.tif -l tests/test_data/test_image_labels.tif -p output.tif
```

## Installation

There are 2 ways to install pycoeus. Either run:
```console
pip install pycoeus
```

Or run:
```console
git clone git@github.com:DroneML/pycoeus.git
cd pycoeus
python -m pip install .
```

## Logging
The application writes logs to the 'logs' dir, which will be created if it doesn't exist yet. Messages printed to the screen (```stdout```) are stored in ```info.log``` for later reference. More detailed information, such as input data shapes and value distributions, are written to ```debug.log```.

## Train a feature extraction model

To train a feature extraction model run the script "train_model.py" in this repo:
```bash
python ./src/pycoeus/utils/train_model.py -r ../monochrome_flair_1_toy_dataset_flat/ --train_set_limit 10
```
This assumes a 'flat', grayscale, version of the FLAIR1 dataset is present at the selected root location.
```
root
- train
    - input
        - IMG_061946_0.tif
        - IMG_061946_1.tif
        - ...
    - labels
        - MSK_061946_0.tif
        - ...    
```
Use the script 'monochromize.py' to create greyscale (single band) tifs for every multiband tif in a source folder:
```bash
python ./src/pycoeus/utils/monochromize.py -i ../flair_1_toy_dataset/ -o ../monochrome_flair_1_toy_dataset/
```

## Credits

This package was created with [Copier](https://github.com/copier-org/copier) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
