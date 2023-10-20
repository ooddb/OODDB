from __future__ import annotations

import json
import os
from typing import Callable

from pkg_resources import resource_filename

_ROOT_DIRS_CONFIG_FILE = "~/.ooddb/config.json"

_DEFAULT_ROOT_DIRS_CONFIG = {
    "domainnet": "~/data/DomainNet",
    "dtd": "~/data/DTD",
    "patternnet": "~/data/PatternNet",
    "stanford_cars": "~/data/Stanford_Cars",
    "sun": "~/data/SUN397",
}


def _get_filename_map_func(
    dataset: str, split: str
) -> Callable[[str | None, str | int, str | None], tuple[str]]:
    if dataset == "domainnet":
        return lambda cls_name, file_id, domain: (
            domain,
            cls_name.split(",")[0],
            f"{file_id}.png"
            if domain == "quickdraw"
            else f"{domain}_{cls_name.split(',')[1]}_{file_id:0>6}.jpg",
        )
    elif dataset == "dtd":
        return lambda cls_name, file_id, _: (
            "images",
            cls_name,
            f"{cls_name}_{file_id:0>4}.jpg",
        )
    elif dataset == "patternnet":
        return lambda cls_name, file_id, _: (
            "images",
            cls_name,
            f"{'wastewaterplant' if cls_name == 'wastewater_treatment_plant' else cls_name.replace('_', '')}{file_id:0>3}.jpg",
        )
    elif dataset == "stanford_cars":
        cars_split = f"cars_{split}"
        return lambda cls_name, file_id, _: (
            cars_split,
            f"{file_id:0>5}.jpg",
        )
    elif dataset == "sun":
        return lambda cls_name, file_id, _: (
            cls_name[0],
            cls_name,
            f"sun_{file_id}.jpg",
        )
    else:
        raise ValueError(f"unknown dataset {dataset}")


def _parse_cls_key(cls_key: str) -> tuple[int, str, str | None]:
    fields = cls_key.split(";")
    cls_id = int(fields[0])
    cls_name = fields[1]
    domain = fields[2] if len(fields) == 3 else None
    return cls_id, cls_name, domain


def _get_natural_cls_name(dataset: str, cls_name: str) -> str:
    if dataset == "sun":
        cls_name = " ".join(reversed(cls_name.split("/")))
    elif dataset == "domainnet":
        cls_name = cls_name.split(",")[0]
    return cls_name.replace("_", " ")


def get_dataset_split_info(
    dataset: str, split: str, data_order: int
) -> tuple[list[str], list[int], dict[int, str]]:
    """Supply necessary information for the desired dataset split

    Args:
        dataset (str): The name of the desired dataset
        split (str): The name of the desired split
        data_order (int): The data order. Must be a value between
            0 and 2 (inclusive)

    Returns:
        A tuple containing the list of the img files relative paths,
        a list of the img labels and a dict mapping each class_id to its name
    """
    filename_mapper = _get_filename_map_func(dataset, split)

    split_file = resource_filename(
        "OODDB", os.path.join("splits", dataset, f"{split}_o{data_order}.json")
    )

    if not os.path.exists(split_file):
        raise ValueError(f"unknown split {split}_o{data_order} for dataset {dataset}")

    with open(split_file, "r") as f:
        dataset_dict: dict[str, list[str | int]] = json.load(f)

    filenames = []
    labels = []
    class_idx_to_name = {}

    for cls_key, file_ids in dataset_dict.items():
        cls_id, cls_name, domain = _parse_cls_key(cls_key)

        natural_cls_name = _get_natural_cls_name(dataset, cls_name)
        dict_natural_cls_name = class_idx_to_name.setdefault(cls_id, natural_cls_name)
        if natural_cls_name != dict_natural_cls_name:
            print(
                f"WARNING: duplicate class_id {cls_id} for {dataset}/{split}/{data_order}",
                f"({dict_natural_cls_name}, {natural_cls_name})",
            )

        for file_id in file_ids:
            filenames.append(os.path.join(*filename_mapper(cls_name, file_id, domain)))
            labels.append(cls_id)

    return filenames, labels, class_idx_to_name


def get_root_dir(dataset: str) -> str:
    """Provide the dataset root location on disk

    The location is read from the config file ~/.ooddb/ooddb.json
    (the file is created if it doesn't exist yet).

    Args:
        dataset (str): The dataset name

    Returns:
        The path to the dataset root directory
    """
    config_file = os.path.expanduser(_ROOT_DIRS_CONFIG_FILE)

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            root_dirs_config = json.load(f)
    else:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "+w") as f:
            f.write(json.dumps(_DEFAULT_ROOT_DIRS_CONFIG, indent=4))
        root_dirs_config = _DEFAULT_ROOT_DIRS_CONFIG

    if dataset not in root_dirs_config:
        raise RuntimeError(f"config file {config_file} missing entry for dataset {dataset}")

    return root_dirs_config[dataset]
