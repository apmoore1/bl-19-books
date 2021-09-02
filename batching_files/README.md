## Extracting and batching all 1890 file names

### Extracting

To do this run the following script:

``` bash
python filtering_files.py --decade 1890 ./id_date_meta_data.json DIRECTORY_TO_BOOKS ./1890_file_names.txt
```

This will then output all the relative file names to all books from the 1890's on each new line to the [./1890_file_names.txt file](./1890_file_names.txt). This file contain *14,281* file names.

To extract all files and not filter, so that you can then more efficiently batch these files, run the following:

```bash
python filtering_files.py ./book_data.json DIRECTORY_TO_BOOKS ./all_file_names.txt
```

``` bash
python batch_files.py 300 DIRECTORY_TO_BOOKS ./all_file_names.txt ../all_books
```
63985/300 = 213.28 creating 214 folders.

### Batching

As we now have a list of filenames we can batch these files into folders of files where each folder contain no more than *N* files. This batching into separate folders will come in useful when it comes to processing these files, as each computer/node can process a folder of files and the more node's we have the faster all of the files will be processed, ideally we would have *M* nodes whereby *M* equals the number of folders we have batched the files into. When processing these on Lancaster's HEC we will request off the HEC as many nodes as possible at one time up to *M* nodes.

```
python batch_files.py 300 DIRECTORY_TO_BOOKS ./1890_file_names.txt ../1890_books
```

As expected this has created 48 sub folders (14281/300 = 47.6), when processing on the HEC we will hope to get 48 nodes (*M=48*). For reference `../1890_books` folder now contains 17GB of JSON.

## Extracting and batching all 1890 and English file names

### Extracting

First we need to combine the [id_date_meta_data data](./id_date_meta_data), with the combined results from language identifiying the 1890 books, which is stored in [../HEC_Processing/1890_files/language_identification/language_results_1890.json](../HEC_Processing/1890_files/language_identification/language_results_1890.json). As we need a file that is in the following format:

``` json
[{"identifier": "004157071", "date": "1862", "language": "English"}]
```

Run the following to get a combined `date` and `language` meta data file called [./id_date_language_meta_data.json](./id_date_language_meta_data.json):

``` bash
python combine_meta_data_and_language.py ./id_date_meta_data.json ../HEC_Processing/1890_files/language_identification/language_results_1890.json ./id_date_language_meta_data.json
```

To do this run the following script

``` bash
python filtering_files.py --language=english ./id_date_language_meta_data.json DIRECTORY_TO_BOOKS ./1890_english_file_names.txt
```

### batching

```
python batch_files.py 300 DIRECTORY_TO_BOOKS ./1890_english_file_names.txt ../1890_english_books
```

As expected this has created 39 sub folders (11419/300 = 38.06), when processing on the HEC we will hope to get 39 nodes (*M=39*). For reference `../1890_english_books` folder now contains 13GB of JSON.

## ID, Date, Meta data file (./id_date_meta_data.json)

**NOTE** the command below does not need running again as the [./id_date_meta_data.json file](./id_date_meta_data.json) has already been created and stored in this repository. The note below is just describing why and how it was created.

The command below creates the file [./id_date_meta_data.json](./id_date_meta_data.json) contains a JSON Array, where each element in the Array is an Object with two keys: 1. `identifier` and 2. `date` (date of book's publication). Each Object element in the Array represents one book from the the British Library 19th Century Book metadata, NOTE the array contains all the books in the original meta data **apart** from those small percentage of books that do not have a published date. This was created so that we can store it in the GitHub repository, and use it instead of the whole original British Library 19th Century Book metadata file.

``` bash
python extract_id_date_meta_data.py ../book_data.json ./id_date_meta_data.json
```


## Testing

The following scripts have been fully tested:

1. [./filtering_files.py](./filtering_files.py).
2. [./batch_files.py](./batch_files.py).

To run the test:

``` bash
python -m pytest
```