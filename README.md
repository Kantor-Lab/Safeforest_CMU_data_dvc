Absolutely! Here's the improved GitHub repo README in Markdown format. Remember to save this as a README.md file within your repository.

**## SafeForest Semantic Segmentation Models**

**Dataset for Wildfire Prevention Research**

This repository provides a forestry dataset captured by UAVs over two distinct locations: Gascola (Pittsburgh, USA) and Coimbra, Portugal. It's designed to support research on wildfire prevention through semantic mapping.

**Get the Dataset**

1. **Request Access:** Complete the brief form here: [https://forms.gle/rHRSgy6vLdwx1Epj8](https://forms.gle/rHRSgy6vLdwx1Epj8) to request access to the Google Drive containing the dataset.

2. **Install DVC:** Download and install Data Version Control (DVC) from [https://dvc.org/doc/install](https://dvc.org/doc/install). 

3. **Download Data:** Use the following DVC commands to pull the dataset:

   ```
   cd path/to/SafeForestfolder/ 
   # Download everything:
   dvc pull -R data -j$(( $(nproc) - 2 )) 
   # Download specific files:
   dvc pull data/site_Coimbra/2023_05_05/collect_04/processed_01/annotations/safeforest23.dvc
   ```

**Using the Data**

If you use this dataset in your research, please cite the following paper:

```
@Article{AndradaMapping2023,
AUTHOR = {Andrada, Maria Eduarda and Russell, David and Arevalo-Ramirez, Tito and Kuang, Winnie and Kantor, George and Yandun, Francisco},
TITLE = {Mapping of Potential Fuel Regions Using Uncrewed Aerial Vehicles for Wildfire Prevention},
JOURNAL = {Forests},
VOLUME = {14},
YEAR = {2023},
NUMBER = {8},
ARTICLE-NUMBER = {1601},
URL = {https://www.mdpi.com/1999-4907/14/8/1601},
ISSN = {1999-4907},
DOI = {10.3390/f14081601}
}
```