
## ID, Date, Meta data file (./id_date_meta_data.json)

**NOTE** the command below does not need running again as the [./id_date_meta_data.json file](./id_date_meta_data.json) has already been created and stored in this repository. The note below is just describing why and how it was created.

The command below creates the file [./id_date_meta_data.json](./id_date_meta_data.json) contains a JSON Array, where each element in the Array is an Object with two keys: 1. `identifier` and 2. `date` (date of book's publication). Each Object element in the Array represents one book from the the British Library 19th Century Book metadata, NOTE the array contains all the books in the original meta data **apart** from those small percentage of books that do not have a published date. This was created so that we can store it in the GitHub repository, and use it instead of the whole original British Library 19th Century Book metadata file. This file will come in useful in at least testing the code within the [./filtering_files_by_decade.py script](./filtering_files_by_decade.py)

``` bash
python extract_id_date_meta_data.py ../book_data.json ./id_date_meta_data.json
```


## Testing

The [./filtering_files_by_decade.py script](./filtering_files_by_decade.py) has been fully tested. To run the test:

``` bash
python -m pytest
```