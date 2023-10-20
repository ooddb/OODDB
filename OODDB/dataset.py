from __future__ import annotations

import os
from typing import Any, Callable

import PIL.Image
from torch.utils import data

from .utils import get_dataset_split_info, get_root_dir


class Dataset(data.Dataset):
    """PyTorch Dataset for the OOD Detection Benchmark

    Attributes:
        class_idx_to_name (dict): Dictionary mapping from the class_id (int)
            to its natural name (str).
    """

    def __init__(
        self,
        dataset_name: str,
        split: str,
        order: int,
        root_dir: str | None = None,
        transform: Callable[[PIL.Image.Image], Any] | None = None,
    ):
        """Build a Dataset for the OOD Detection Benchmark

        Args:
            dataset_name (str): The name of the dataset. Supported values are
                "domainnet", "dtd", "patternnet", "stanford_cars" and "sun".
            split (str): The split for the specified dataset. "domainnet" supports
                one among "<domain>_train", "<domain>_test" and "no_<domain>_train",
                with <domain> being one among "clipart", "infograph", "painting",
                "quickdraw", "real" and "sketch".
                All the other datasets only support either "train" or "test".
            order (int): The data order for the specified dataset. Must be a value
                between 0 and 2 (inclusive).
            root_dir (str, optional): The root directory for the dataset. If None,
                the location will be read from the "~/.ooddb/config.json" config
                file (the file will be created with the default values if it doesn't
                exist).
            transform (callable, optional): A transform operation to be applied to a
                PIL Image.
        """
        img_files, labels, class_idx_to_name = get_dataset_split_info(dataset_name, split, order)

        self._img_files = img_files
        self._labels = labels
        self.class_idx_to_name = class_idx_to_name

        self._transform = transform

        self._root_dir = os.path.expanduser(
            root_dir if root_dir is not None else get_root_dir(dataset_name)
        )
        if not os.path.isdir(self._root_dir):
            raise RuntimeError(
                f"root dir {self._root_dir} for dataset {dataset_name} does not exist"
            )

    def __getitem__(self, idx: int) -> tuple[Any, int]:
        img_file = os.path.join(self._root_dir, self._img_files[idx])
        img = PIL.Image.open(img_file).convert("RGB")
        if self._transform is not None:
            img = self._transform(img)
        return img, self._labels[idx]

    def __len__(self) -> int:
        return len(self._img_files)
