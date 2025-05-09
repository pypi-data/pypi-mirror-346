"""
Hyrax has several built-in datasets that you can use for astronomical data. For many uses, these datasets
can be configured out-of-the box for a given  project.

:doc:`FitsImageDataSet <fits_image_dataset/index>` is a generic container for fits image cutout data
indexed by a user-provided catalog file. It attempts to cover common usage paradigms such as multiple images
of the same object differentiated by telescope filter; however, extending the class as a custom dataset
may be more well fit to advanced usage.

:doc:`LSSTDataset <lsst_dataset/index>` Is a alpha-quality container for LSST cutout images, currently
limited to ``deep_coadd`` type images, and restricted to run only on a Rubin observatory RSP environment
where `LSST Pipeline <https://pipelines.lsst.io/>`_ tools and a
`data butler <https://pipelines.lsst.io/modules/lsst.daf.butler/index.html>`_ with the appropriate images
are available.

:doc:`HSCDataSet <hsc_data_set/index>` Works similarly to FitsImageDataSet, but is specialized to
`Hyper Suprime-Cam (HSC) <https://hsc-release.mtk.nao.ac.jp/doc/index.php/data/>`_ cutout images downloaded
with the hyrax ``download`` verb. It contains additional integrity checks and is tightly integrated with
the ``download`` and ``rebuild_manifest`` verbs. In future this class and the downloader may become a
separate package.

:doc:`HyraxCifarDataSet <hyrax_cifar_data_set/index>` and
:doc:`HyraxCifarIterableDataSet <hyrax_cifar_data_set/index>` give access to the standard
`CIFAR10 <https://www.cs.toronto.edu/~kriz/cifar.html>`_ labeled image dataset, automatically downloading the
dataset if it is not present. These datasets are useful for testing hyrax and occasionally individual models,
but they are not astronomical datasets.

Each of these datasets can be used a starting point for a Custom Dataset by inheriting your custom dataset
from e.g. `FitsImageDataSet`, or you can make an entirely custom dataset following the
:ref:`custom dataset instructions <custom-dataset-instructions>` and/or
:doc:`custom dataset example notebook </pre_executed/custom_dataset>`.

The remaining classes in this module exist primarily for Hyrax interface purposes:

:doc:`InferenceDataset <inference_dataset/index>` is a dataset class that represents an ``infer`` or ``umap``
result, and may be returned from those verbs to provide data access

:doc:`HyraxDataset <data_set_registry/index>` is a base class for all datasets in Hyrax and must be within
the inheretence hierarchy of all custom datasets. It is not usable on it's own, but provides various fall-back
functionality to make custom datasets easier to write. See the
:ref:`custom dataset instructions <custom-dataset-instructions>` and
:doc:`example notebook </pre_executed/custom_dataset>` for more information.

"""

# Remove import sorting, these are imported in the order written so that
# autoapi docs are generated with ordering controlled below.
# ruff: noqa: I001
from .fits_image_dataset import FitsImageDataSet
from .lsst_dataset import LSSTDataset
from .hsc_data_set import HSCDataSet
from .hyrax_cifar_data_set import HyraxCifarDataSet, HyraxCifarIterableDataSet
from .inference_dataset import InferenceDataSet
from .data_set_registry import HyraxDataset
from .hyrax_cifar_data_set import HyraxCifarBase

__all__ = [
    "HyraxCifarDataSet",
    "FitsImageDataSet",
    "HyraxCifarIterableDataSet",
    "HSCDataSet",
    "InferenceDataSet",
    "HyraxDataset",
    "LSSTDataset",
    "HyraxCifarBase",
]
