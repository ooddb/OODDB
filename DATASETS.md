# Datasets

We report here extra details for each dataset, including some visual examples and the expected storage format/layout on disk.

**Table summary**:

| | n. images | n. classes (ID, OOD) | n. domains | image type |
|:-:|:-:|:-:|:-:|:-:|
| [DomainNet](#domainnet) | ~154k | 100 (50, 50) | 6 | object-centric |
| [DTD](#dtd) | ~6k | 47 (23, 24) | 1 | textures |
| [PatternNet](#patternnet) | ~30k | 38 (19, 19) | 1 | aerial pictures |
| [Stanford Cars](#stanford-cars) | ~16k | 196 (98, 98) | 1 | fine-grained cars |
| [SUN](#sun) | ~101k | 397 (198, 199) | 1 | scenes |

## DomainNet

[Original paper](https://arxiv.org/pdf/1812.01754.pdf)\
[Official website](http://ai.bu.edu/M3SDA/)\
Download links:
[clipart](http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/clipart.zip),
[infograph](http://csr.bu.edu/ftp/visda/2019/multi-source/infograph.zip),
[painting](http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/painting.zip),
[quickdraw](http://csr.bu.edu/ftp/visda/2019/multi-source/quickdraw.zip),
[real](http://csr.bu.edu/ftp/visda/2019/multi-source/real.zip),
[sketch](http://csr.bu.edu/ftp/visda/2019/multi-source/sketch.zip)

DomainNet contains object-centric images divided into 345 categories across 6 different domains (Clipart, Infograph, Painting, Quickdraw, Real, Sketch).
For our benchmark, we selected the 100 classes having the smallest semantic overlap with ImageNet-1k (using the [Natural Language Toolkit](https://www.nltk.org/)) for a total of 153,696 images.
For each *data order*, we randomly selected 50 categories as ID and the other 50 as OOD.\
We provide train splits formed by samples belonging to either a single domain (`<domain>_train`) or all of them, minus the target one (`no_<domain>_train`).
Every test split is built from a single domain instead (`<domain>_test`).

Considering the presence of 6 different domains, the benchmark provides the following numbers of different settings for DomainNet:
- **intra-domain**: 6 (one for each domain)
- **single-source cross-domain**: 30 (one for each pair of different train-test domains)
- **multi-source cross-domain**: 6 (one for each target domain)

Each setting includes 3 different configurations, corresponding to the 3 *data orders*.

**Expected format**

The root directories for the 6 different domains are expected to be located under the same parent directory, which has to be speficied either in `~/.ooddb/config.json` or at run-time to the `Dataset` class.

- For Quickdraw, the expeced image file format is:\
  `<root_dir>/quickdraw/<class_name>/<img_id>.png`\
  where `<class_name>` refers to the natural name of the category (e.g., `book`).
- For all the other domains, the expected format is:\
  `<root_dir>/<domain>/<class_name>/<domain>_<class_id>_<img_id>.jpg`\
  where `<domain>` is the lowercase domain name and `<class_id>` is the original class index (a 3-digit integer). 


## DTD

[Original paper](https://www.robots.ox.ac.uk/~vgg/publications/2014/Cimpoi14/cimpoi14.pdf)\
[Official website](https://www.robots.ox.ac.uk/~vgg/data/dtd/)\
[Download link](https://www.robots.ox.ac.uk/~vgg/data/dtd/download/dtd-r1.0.1.tar.gz)

DTD (*Describable Textures Dataset*) contains 5,640 images of textures belonging to 47 different classes.
For each *data order*, we select 23 random classes as ID and the other 24 as OOD.
For every train-test split, we follow the first fold provided by the original authors for their cross-validation strategy, merging train and validation data.

**Expected format**

The expected image file format is:\
`<root_dir>/images/<class_name>/<class_name>_<img_id>.jpg`.

## PatternNet

[Original paper](https://faculty.ucmerced.edu/snewsam/papers/Zhou_ISPRS18_Patternet.pdf)\
[Official website](https://sites.google.com/view/zhouwx/dataset#h.p_Tgef10WTuEFr)\
[Download link](https://nuisteducn1-my.sharepoint.com/:u:/g/personal/zhouwx_nuist_edu_cn/EYSPYqBztbBBqS27B7uM_mEB3R9maNJze8M1Qg9Q6cnPBQ?e=MSf977)

PatternNet is a dataset of high-resolution aerial pictures, designed for remote sensing image retrieval.
It consists of 38 category containing 800 samples each, for a total of 30,400 images.
For each *data order* we selected 19 classes as ID and the others as OOD, following
the train-test splits proposed by the original authors.

**Expected format**

The expected image file format is:\
`<root_dir>/images/<class_name>/<short_class_name><img_id>.jpg`.

## Stanford Cars

[Original paper](https://ai.stanford.edu/~jkrause/papers/fgvc13.pdf)\
[Kaggle](https://www.kaggle.com/datasets/jessicali9530/stanford-cars-dataset) (official website was removed)\
[Kaggle download link](https://www.kaggle.com/datasets/jessicali9530/stanford-cars-dataset/download?datasetVersionNumber=2)

Stanford Cars is a large-scale, fine-grained dataset of car images.
It contains 16,185 pictures divided into 196 classes.
We selected 98 random categories as ID for each *data order* and we followed the
train-test split proposed by the original authors.

**Expected format**

The expected image file format is:\
`<root_dir>/cars_<split>/<img_id>.jpg`\
where `<split>` is either `train` or `test`.

## SUN

[Original paper](https://vision.princeton.edu/projects/2010/SUN/paper.pdf)\
[Official website](https://vision.princeton.edu/projects/2010/SUN/)\
[Download link](http://vision.princeton.edu/projects/2010/SUN/SUN397.tar.gz)

SUN (*Scene UNderstanding*) is a large-scale dataset designed for scene understanding.
It includes over 130k images divided into 899 categories, of which 397 are considered *well-sampled*. In this benchmark, we use a total of 100,883 pictures belonging to these
397 classes, picking 198 of them as ID for each *data order* and following the original train-test split.

**Expected format**

The expected image file format is:\
`<root_dir>/<class_name_initial>/<class_name>/sun_<img_id>.jpg`.
