# Analysis of British Library 19th Century Book corpus

The [book corpus](https://data.bl.uk/digbks/db14.html) and it's [meta data](https://data.bl.uk/digbks/DB21.html) cover the years of 1510 to 1940 and have around 49,500 books. 

## Setup
Tested using Python `3.6.7` but should work with Python >=`3.6.1`. Install the pip requirements: `pip install -r requirements.txt`

To resolve the place names download the [geonames allCountries.zip file](http://download.geonames.org/export/dump/) and then unzip it (this file is around 1.6GB). Then run the following Python script:

``` bash
python geonames_name_only.py
```

This script extracts all country and city names from geonames name list including all alternative names and saves just the names to the file `./CountriesNamesAlt.txt` (this file will be around 245MB).

[The British Library 19th Century Book metadata](https://data.bl.uk/digbks/DB21.html) can be found in this repository [./book_data.json](./book_data.json) due to it be only 12.5MB.

## Analysis

All of the meta data analysis of The British Library 19th Century Books can be found in the [./meta_analysis.ipynb](./meta_analysis.ipynb) notebook. 