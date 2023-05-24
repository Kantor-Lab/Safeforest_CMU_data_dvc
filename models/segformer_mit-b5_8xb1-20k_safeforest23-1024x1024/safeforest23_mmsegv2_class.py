# Copyright (c) OpenMMLab. All rights reserved.
from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset


@DATASETS.register_module()
class Safeforest23Dataset(BaseSegDataset):
    """Safeforest 2023 dataset.
    """
    METAINFO = dict(
        classes = (
            "Dry Grass",
            "Green Grass",
            "Dry Shrubs",
            "Green Shrubs",
            "Canopy",
            "Wood Pieces",
            "Litterfall",
            "Timber Litter",
            "Live Trunks",
            "Bare Earth",
            "People",
            "Sky",
            "Blurry",
            "Obstacles",
        ),
        palette=[
            [128, 64, 128],
            [244, 35, 232],
            [70, 70, 70],
            [102, 102, 156],
            [190, 153, 153],
            [153, 153, 153],
            [250, 170, 30],
            [220, 220, 0],
            [107, 142, 35],
            [152, 251, 152],
            [70, 130, 180],
            [220, 20, 60],
            [255, 0, 0],
            [0, 0, 142]])

    def __init__(self,
                 img_suffix='_rgb.png',
                 seg_map_suffix='_segmentation.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)
