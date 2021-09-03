# Analysis of British Library 19th Century Book corpus

The [book corpus](https://data.bl.uk/digbks/db14.html) and it's [meta data](https://data.bl.uk/digbks/DB21.html) cover the years of 1510 to 1940 and have around 49,500 books. 

## Setup

### Python installation:

Tested using Python `3.6.7` but should work with Python >=`3.6.1`. Install the pip requirements: 

``` bash
pip install -r requirements.txt
```

If you are [processing the text of the book corpus](#book-corpus-ocr-text-processing) rather than [exploring the meta data](#meta-data-analysis) you will need to download the English spaCy model like so:

``` bash
python -m spacy download en_core_web_sm
```

### Meta data:

[The British Library 19th Century Book metadata](https://data.bl.uk/digbks/DB21.html) can be found in this repository [./book_data.zip](./book_data.zip) due to it be only 13MB. This file needs to be unzip into a file called `./book_data.json`.

In the meta data analysis notebook, [./meta_analysis.ipynb](./meta_analysis.ipynb), we use [GeoNames](https://www.geonames.org/) to resolve place names, if you would like to use run this notebook it does require downloading the [geonames allCountries.zip file](http://download.geonames.org/export/dump/) and then unzip it (this file is around 1.6GB). Then run the following Python script:

``` bash
python geonames_name_only.py
```

This script extracts all country and city names from GeoNames name list including all alternative names and saves just the names to the file `./CountriesNamesAlt.txt` (this file will be around 245MB).

### Book corpus (OCR text)

The [book corpus](https://data.bl.uk/digbks/db14.html) can be downloaded and un-compressed like so (**WARNING** this is a **~10.5GB downloaded** and once uncompressed it is about **~122GB** but this reduces down to **81GB** once you have deleted the *dig19cbooksjsontext* tar file leaving you with the *json* folder of OCR book texts):

``` bash
curl -O https://data.bl.uk/digbks/dig19cbooksjsontext.bz2
bzip2 -d dig19cbooksjsontext.bz2
tar -xvf dig19cbooksjsontext
```

Creates a directory `json` which contains `63,985` files (**81GB**):

``` bash
find json/ -type f | wc -l
```

## Meta Data Analysis

All of the meta data analysis of The British Library 19th Century Books can be found in the [./meta_analysis.ipynb](./meta_analysis.ipynb) notebook. 

### Searching

If you would like to search the meta data you can use the [./meta_data_viewer.py](./meta_data_viewer.py) program. Whereby it will print out the meta data for a book given that books nine digit identifier e.g.:
``` bash
python meta_data_viewer.py 000741339
```
Will print out:
```python
publisher : “Times of India” Office
title : ['Typical Pictures of Indian Natives: being reproductions from specially-prepared hand-coloured photographs. With descriptive letterpress by F. M. Coleman']
flickr_url_to_book_images : http://www.flickr.com/photos/britishlibrary/tags/sysnum000741339
place : Bombay
authors : {'creator': ['COLEMAN, F. M.']}
date : 1807
identifier : 000741339
```

The program expects that the meta data to be found at `./book_data.json`, but if you have saved it else where you can specify the file location like so:
```bash
python meta_data_viewer.py 000741339 ./book_data.json
```

For more information about the program read the help guide:
```bash
python meta_data_viewer.py --help
```

## Book corpus (OCR text) Processing

We have assumed that you have downloaded the book corpus, see the [Book corpus (OCR text) setup section above](#book-corpus-ocr-text), and that the book corpus top level directory, `json`, is at a file path we denote `DIRECTORY_TO_BOOKS`. This `DIRECTORY_TO_BOOKS` could be at `/home/json` or any other file path **but** it should never be checked into this git repository due to it's size. 

### json directory format

The `json` directory is structured based on the books' identifier string. Each book has a nine digit unique identifier, which in python is represented as a String, for instance the book `Typical Pictures of Indian Natives: being reproductions from specially-prepared hand-coloured photographs. With descriptive letterpress by F. M. Coleman` is identified by the following nine digit string `000741339`. The `json` directory has  48 sub-directories each being 4 digits long e.g. `0038` this 4 digits states that all book whose identifier start with those 4 digits are in that sub-directory. In the case of `000741339` it will be in sub-directory `0007`. Files in those directory have the following pattern `uniqueIdentifier_volumneNumber_text.json` whereby `uniqueIdentifier` is the identifier and `volumeNumber` is the volume number of the book. In the case of `000741339` as it only has one volume all of the text data will be stored at the following file:

`json/0007/000741339_01_text.json`

**If** had `000741339` two volumes the second volume text would be at `json/0007/000741339_02_text.json`

#### Concrete example

For a more concrete example the book with the identifier `011837920` contains two volumes, of which we can find this out through the meta data using the meta data search tool:

``` bash
python meta_data_viewer.py 011837920 ./book_data.json
publisher : Kegan Paul
title : ['Life in the Mofussil, or, The civilian in Lower Bengal', 'Civilian in Lower Bengal']
flickr_url_to_book_images : http://www.flickr.com/photos/britishlibrary/tags/sysnum011837920
place : enk
authors : {'creator': ['Graham, George.']}
date : 1878
pdf : {'1': 'lsidyv3919f5e7', '2': 'lsidyv3919fd07'}
identifier : 011837920
```
As the meta data contains the key `pdf` with values `1` and `2` this indicates that the book has two volumes. Knowing this we know that this books text data will be at the following two files:
```bash
json/0118/011837920_01_text.json
json/0118/011837920_02_text.json
```

**Note** if the key `pdf` does not exist then you can use the `imgs` key instead e.g.
``` bash
python meta_data_viewer.py -rm 'datefield' -rm 'shelfmarks' -rm 'edition' -rm 'issuance' -rm 'corporate' 000741339 ./book_data.json 

imgs : {'0': {'000071': ['11000834745'], '000099': ['11000891803'], '000075': ['11001140313'], '000095': ['11000789065'], '000079': ['11000864954'], '000091': ['11000896406'], '000059': ['11000949503'], '000111': ['11000695075'], '000016': ['11219715495'], '000010': ['11001417834'], '000039': ['11001014233'], '000012': ['11001292025', '11001377336', '11219716895'], '000051': ['11000934415'], '000119': ['11001453614', '11219837423'], '000035': ['11000676935'], '000055': ['11000983144'], '000018': ['11001148703'], '000031': ['11000833886'], '000014': ['11219712374'], '000067': ['11000820884'], '000063': ['11000886536'], '000087': ['11000983615'], '000083': ['11001017755'], '000115': ['11001289265'], '000007': ['11001418734'], '000022': ['11000915306'], '000013': ['11001516523'], '000027': ['11000915765'], '000107': ['11001018004'], '000043': ['11001057394'], '000103': ['11000785326'], '000047': ['11000816065'], '000008': ['11000688195'], '000053': ['11000929054']}}
publisher : “Times of India” Office
title : ['Typical Pictures of Indian Natives: being reproductions from specially-prepared hand-coloured photographs. With descriptive letterpress by F. M. Coleman']
flickr_url_to_book_images : http://www.flickr.com/photos/britishlibrary/tags/sysnum000741339
place : Bombay
authors : {'creator': ['COLEMAN, F. M.']}
date : 1807
identifier : 000741339
```

### File format

Each of these json files is made up of one JSON Array (Python list), each element/entry in the array is another JSON Array which represents a page within the book that the json file represents. This page array contains only two entries:

1. A page number, represented as a Number/integer.
2. The text that is on that page, represented as a String. This String can sometimes be empty e.g. "".

Example of the file format is below (taken from the first 6 pages of "Report on the Kolar Gold Field and its southern extension" by P. (Percy) Bosworth-Smith, 1889, book id `011834197`):

JSON
```
[[1, ""], [2, ""], [3, ""], [4, ""], [5, "REPORT ON THE KOLAR GOLD FIELD AND ITS SOUTHERN EXTENSION, IN WHICH THE AURIFEROUS ROCKS ARE TRACED FROM THE MYSORE STATE INTO THE MADRAS PRESIDENCY. WITH MAPS AND SKETCHES. BY P. BOSWORTH-SMITR^Esq., F.G.S., ASSOCIATE Or THE ROYAL SCHOOL OF MINES (BESSEMER MEDALLIST), AND GOVERNMENT MINERALOGIST TO THE MADRAS PRESIDENCY. MADRAS: PRINTED BY THE SUPERINTENDENT, GOVERNMENT PRESS. 1889."], [6, ""]
```

### Processing speed

It takes around 95-100 seconds to process 3.7MB of data, of which there is 81GB of data. It can process this data at around 8000 Words per second. Based on file size 3.7MB is around 22,000 times smaller than the whole corpus. Based on this 100 seconds multiplied by 22,000 is roughly 611.1 hours which is around 25.5 days.

When processing the 1890 books (~14280 books) the [large FastText language identification model](https://fasttext.cc/docs/en/language-identification.html) managed to process a book in 1.2 seconds.


### Processing pipeline

As we are going to run various NLP tools on Lancaster's High End Computing (HEC) cluster we need to know some statistics on runtime performance of these tools, more specifically the [spaCy models](https://spacy.io/models/en) for the main NLP pipeline e.g. tokenization, Part Of Speech (POS) tagging etc and the [FastText models](https://fasttext.cc/docs/en/language-identification.html) for language identification. We need to know how much time and memory each model will take on a text. Knowing how long it will take (time) will allow us to determine roughly how long it will take to process all of the texts. Knowing the memory requirement is important as the HEC requires us to state up front before submitting a script to run how much memory is required to run the script.

The breakdown of the performance of different models can be found at:

1. For the 4 English Spacy models: [./benchmarking_spacy](./benchmarking_spacy/). In this analysis we also found how long the longest page is, based on number of characters, roughly 11,000 words. Even though these benchmarks are a good guide for a better estimation on the time it would take to run Spacy on the whole British Library corpus see the `More Real World Benchmarking` section in [./spacy_processing](./spacy_processing). License of all spacy models is [MIT](https://opensource.org/licenses/MIT).
2. For the FastText language identification small and large models: [./benchmarking_fasttext](./benchmarking_fasttext). License for all tested FastText models is [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).

Based on these performances we are going to use:

1. Medium Spacy model for the NLP pipeline.
2. Large FastText model for the language identification.

In this project as we are only focusing on the English Language we are first going to process the texts using the Language Identification model and then the NLP pipeline.

#### Language ID

In this project we are focusing on English text's therefore we are first going to process the text with the language identification model to find the English texts. For more details on how we processed the text using the language identification model see the [./language_identification folder](./language_identification). 

#### NLP Pipeline

Once we have extracted all of the English text's we ran them through the Spacy NLP pipeline. For more details on how we processed the text using the Spacy pipeline see the [./spacy_processing folder](./spacy_processing folder).