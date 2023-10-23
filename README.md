# OOD Detection Benchmark

This repository is meant to provide a simple way to access the OOD Detection Benchmark: a comprehensive benchmark suite designed to evaluate machine learning models performing Out-Of-Distribution Detection, with a specific focus on its semantic aspect.

<!-- [[Paper]]() -->
[[Website]](https://ooddb.github.io)

## Setup

### Download the datasets

First, download the required datasets and make sure they're stored with their default layouts, as reported below:
- **DomainNet** (downloads:
  [clipart](http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/clipart.zip),
  [infograph](http://csr.bu.edu/ftp/visda/2019/multi-source/infograph.zip),
  [painting](http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/painting.zip),
  [quickdraw](http://csr.bu.edu/ftp/visda/2019/multi-source/quickdraw.zip),
  [real](http://csr.bu.edu/ftp/visda/2019/multi-source/real.zip),
  [sketch](http://csr.bu.edu/ftp/visda/2019/multi-source/sketch.zip)):\
  The root directories for the 6 different domains are expected to be located under the same parent folder, which has to be speficied either in `~/.ooddb/config.json` or at run-time to the `Dataset` class (see below):
  - For Quickdraw, the expected image file format is:\
    `<root_dir>/quickdraw/<class_name>/<img_id>.png`\
    where `<class_name>` refers to the natural name of the category (e.g., `book`).
  - For all the other domains, the expected format is:\
    `<root_dir>/<domain>/<class_name>/<domain>_<class_id>_<img_id>.jpg`\
    where `<domain>` is the lowercase domain name and `<class_id>` is the original class index (a 3-digit integer). 
- **DTD**
  ([download](https://www.robots.ox.ac.uk/~vgg/data/dtd/download/dtd-r1.0.1.tar.gz)):\
  `<root_dir>/images/<class_name>/<class_name>_<img_id>.jpg`
- **PatternNet**
  ([download](https://nuisteducn1-my.sharepoint.com/:u:/g/personal/zhouwx_nuist_edu_cn/EYSPYqBztbBBqS27B7uM_mEB3R9maNJze8M1Qg9Q6cnPBQ?e=MSf977)):\
  `<root_dir>/images/<class_name>/<short_class_name><img_id>.jpg`
- **Stanford Cars**
  ([download](https://www.kaggle.com/datasets/jessicali9530/stanford-cars-dataset/download?datasetVersionNumber=2)):\
  `<root_dir>/cars_<split>/<img_id>.jpg`\
  where `<split>` is either `train` or `test`
- **SUN**
  ([download](http://vision.princeton.edu/projects/2010/SUN/SUN397.tar.gz)):\
  `<root_dir>/<class_name_initial>/<class_name>/sun_<img_id>.jpg`

### Install the `OODDB` package

You can easily access the benchmark splits by installing the `OODDB` package via pip:
```shell
pip install git+https://github.com/ooddb/OODDB.git
```

By default, the on-disk datasets root folder locations are read from the `~/.ooddb/config.json` file, which is automatically created and populated with the default values if it doesn't exist yet:
```json
{
  "domainnet": "~/data/DomainNet",
  "dtd": "~/data/DTD",
  "patternnet": "~/data/PatternNet",
  "stanford_cars": "~/data/Stanford_Cars",
  "sun": "~/data/SUN397",
}
```
You can specify any value you prefer or overrride the dataset location by providing it at run-time (see [below](#usage)).


## Usage

The `OODDB` package exposes a single `Dataset` class which accepts different dataset and split names
to access the desired data.

Usage example:
```python
from torchvision import transforms
from OODDB import Dataset

dataset = Dataset(
    dataset_name="sun",
    split="train",
    order=0,
    root_dir="~/data/my_folder",
    transform=transforms.ToTensor()
)
```

Specifically, the `Dataset` class accepts the following parameters:
- `dataset_name`: the name of the desired dataset. The supported values are:
  - `domainnet` for DomainNet
  - `dtd` for DTD
  - `patternnet` for PatternNet
  - `stanford_cars` for Stanford Cars
  - `sun` for SUN
- `split`: the name of the desired split.
  - DomainNet accepts `<domain>_train`, `<domain>_test` or `no_<domain>_train`,
    where `<domain>` must be one among `clipart`, `infograph`, `painting`, `quickdraw`, `real` and `sketch`.
  - All the other datasets only accept either `train` or `test`.
- `order`: one of the three *data orders* provided for the selected dataset. Must be a value between 0 and 2 (inclusive). (**WARNING**: each *data order* is not compatible with the others as the class ids differ for each one of them. Use the same `order` value for both the train and test splits.)
- `root_dir`: the dataset root location on disk. If not specified, the value from `~/.ooddb/config.json` will be used.
- `transform`: a function/transform to be applied to a `PIL` `Image`.

For more details, see [dataset.py](./OODDB/dataset.py).

If you prefer to use your own `Dataset` class instead, you can utilize the `OODDB.utils.get_dataset_split_info` function to retrieve the necessary information. Example:
```python
from OODDB.utils import get_dataset_split_info

file_names, labels, class_idx_to_name = get_dataset_split_info(
    dataset="sun",
    split="train",
    data_order=0
)
```

## Benchmark Tracks

The benchmark supports the two following tracks:

### Intra-domain

In this case the train and test samples are drawn from the same visual data distribution.
With the exception of DomainNet, all the datasets exclusively support this setting.
As for the former, you can execute this track by selecting the same domain for
both the train and test data.

Example (DTD):
```python
from OODDB import Dataset

DATASET="dtd"
DATA_ORDER=0

train_dataset = Dataset(DATASET, split="train", order=DATA_ORDER)
test_dataset = Dataset(DATASET, split="test", order=DATA_ORDER)
```

Example (DomainNet Painting):
```python
from OODDB import Dataset

DATASET="domainnet"
DATA_ORDER=0

train_dataset = Dataset(DATASET, split="painting_train", order=DATA_ORDER)
test_dataset = Dataset(DATASET, split="painting_test", order=DATA_ORDER)
```

### Cross-domain

In this case the train and test samples are drawn from different visual data
distributions. This track is only supported by DomainNet and can be further divided
into **_single-source_** (all the train samples belong to the same single domain)
and **_multi-source_** (the train samples are drawn from several different domains, disjoint from the test one). In both cases the test samples belong to a single domain (i.e., both settings are **_single-target_**).

In order to execute this track, do the following:
- **single-source**: select two different domains for the train and test splits.\
  Example (Clipart &rarr; Sketch):
  ```python
  from OODDB import Dataset

  DATASET="domainnet"
  DATA_ORDER=0

  train_dataset = Dataset(DATASET, split="clipart_train", order=DATA_ORDER)
  test_dataset = Dataset(DATASET, split="sketch_test", order=DATA_ORDER)
  ```
- **multi-source**: select `no_<domain>` for the train split and and `<domain>` for the test one.\
  Example (Quickdraw):
  ```python
  from OODDB import Dataset

  DATASET="domainnet"
  DATA_ORDER=0

  train_dataset = Dataset(DATASET, split="no_quickdraw_train", order=DATA_ORDER)
  test_dataset = Dataset(DATASET, split="quickdraw_test", order=DATA_ORDER)
  ```
