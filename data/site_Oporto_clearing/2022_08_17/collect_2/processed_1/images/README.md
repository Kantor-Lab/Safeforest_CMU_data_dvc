# left images

Extract images from data/site\_Oporto\_clearing/2022\_08\_17/collect\_2/raw/nuc/*bag on topic /left/camera/image_raw into data/site_Oporto_clearing/2022_08_17/collect_2/processed_1/images

```
python scripts/saving/images.py "data/site_Oporto_clearing/2022_08_17/collect_2/raw/nuc/*bag" data/site_Oporto_clearing/2022_08_17/collect_2/processed_1/images /left/camera/image_raw  --start-index 2 --delta 0.1 --flip-channels --debayer --debayer-mode BG
```

# right images 
```
 python scripts/saving/images.py "data/site_Oporto_clearing/2022_08_17/collect_2/raw/nuc/*bag" data/site_Oporto_clearing/2022_08_17/collect_2/processed_1/images /right/camera/image_raw  --start-index 2 --delta 0.1 --flip-channels --debayer --debayer-mode BG --extension ".png"
```
